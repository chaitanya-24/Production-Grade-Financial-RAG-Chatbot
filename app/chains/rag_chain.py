from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.schema.messages import HumanMessage, AIMessage
from typing import Dict, Any, List, Optional, Union
from pathlib import Path

from app.core.llm import get_llm
from app.core.vectorstore import get_vectorstore
from app.models.response import ChatResponse
from app.models.prompt import PromptStrategy
from app.prompts.strategies import PromptStrategyManager
from app.loaders.file_loader import FileLoader
from app.loaders.text_splitter import DocumentSplitter

class RAGChain:
    def __init__(self, prompt_strategy: PromptStrategy = PromptStrategy.CHAIN_OF_THOUGHT):
        self.vectorstore = get_vectorstore()
        self.llm = get_llm()
        self.memory = ConversationBufferMemory(
            return_messages=True,
            memory_key="chat_history",
            output_key="answer"
        )
        self.prompt_strategy = prompt_strategy
        self.strategy_manager = PromptStrategyManager()
        self.file_loader = FileLoader()
        self.document_splitter = DocumentSplitter()

        # Initialize prompt with selected strategy
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.strategy_manager.apply_strategy(
                self.prompt_strategy,
                context="{context}",
                chat_history="{chat_history}",
                question="{question}"
            ))
        ])

        # Build the RAG chain
        self.retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        )
        
        self.chain = (
            {
                "context": self.retriever | self._format_docs,
                "chat_history": self._get_chat_history,
                "question": RunnablePassthrough()
            }
            | self.prompt
            | self.llm
            | StrOutputParser()
            | self._format_response
        )

    def _format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def _get_chat_history(self, _):
        # return self.memory.load_memory_variables({})["chat_history"]
        memory_vars = self.memory.load_memory_variables({})
        messages = memory_vars.get("chat_history", [])
        formatted_messages = []
        
        for message in messages:
            if isinstance(message, HumanMessage):
                formatted_messages.append(f"Human: {message.content}")
            elif isinstance(message, AIMessage):
                formatted_messages.append(f"Assistant: {message.content}")
                
        return "\n".join(formatted_messages)

    def _format_response(self, answer: str) -> ChatResponse:
        """
        Format the response to ensure clean output
        """
        # Remove any step-by-step reasoning markers
        clean_answer = answer
        
        # Remove numbered steps if present
        import re
        clean_answer = re.sub(r'\d+\.\s+[\*\-]\s*', '', clean_answer)
        clean_answer = re.sub(r'\d+\.\s+', '', clean_answer)
        
        # Remove markers like "Final Answer:" or "Reasoning:"
        markers_to_remove = [
            "Final Answer:",
            "Reasoning:",
            "Let's approach this systematically:",
            "Key Pieces of Information:",
            "Intermediate Conclusions:"
        ]
        
        for marker in markers_to_remove:
            clean_answer = clean_answer.replace(marker, "")
        
        # Clean up multiple newlines
        clean_answer = re.sub(r'\n\s*\n', '\n\n', clean_answer)
        clean_answer = clean_answer.strip()
        
        # Extract source documents if present
        source_docs = []
        if "Sources:" in clean_answer:
            main_content, sources = clean_answer.split("Sources:")
            clean_answer = main_content.strip()
            source_docs = [s.strip() for s in sources.split(",")]
        
        return ChatResponse(
            answer=clean_answer,
            source_documents=source_docs,
            confidence_score=0.85  # You can adjust this based on your needs
        )
    
    async def chat(self, message: str) -> ChatResponse:
        """
        Process a chat message and maintain conversation history
        """
        # Get response from chain
        response = await self.chain.ainvoke(message)
        
        # Save the interaction to memory
        self.memory.save_context(
            {"input": message},
            {"answer": response.answer}
        )
        
        return response

    async def ingest_documents(self, file_paths: List[Union[str, Path]]) -> None:
        """
        Ingest documents into the vectorstore.
        """
        all_documents = []
        
        # Load and process documents
        for file_path in file_paths:
            try:
                documents = self.file_loader.load(file_path)
                split_documents = self.document_splitter.split_documents(documents)
                all_documents.extend(split_documents)
            except Exception as e:
                print(f"Error processing file {file_path}: {str(e)}")
                continue
                
        if all_documents:
            await self.vectorstore.aadd_documents(all_documents)