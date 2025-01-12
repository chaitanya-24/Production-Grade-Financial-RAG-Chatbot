from typing import Dict, Any
from app.models.prompt import PromptStrategy
from app.prompts.templates import PROMPT_TEMPLATES

class PromptStrategyManager:
    @staticmethod
    def apply_strategy(strategy: PromptStrategy, **kwargs) -> str:
        if strategy == PromptStrategy.SIMPLE:
            return PROMPT_TEMPLATES["rag_base"].template.format(**kwargs)
            
        elif strategy == PromptStrategy.CHAIN_OF_THOUGHT:
            return PROMPT_TEMPLATES["chain_of_thought"].template.format(**kwargs)
            
        elif strategy == PromptStrategy.FEW_SHOT:
            return PROMPT_TEMPLATES["few_shot"].template.format(**kwargs)
            
        elif strategy == PromptStrategy.SELF_REFLECTION:
            base_response = PROMPT_TEMPLATES["chain_of_thought"].template.format(**kwargs)
            return f"{base_response}\nProvide a refined answer based on the context."
            
        return PROMPT_TEMPLATES["rag_base"].template.format(**kwargs)