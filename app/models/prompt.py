from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

class PromptTemplate(BaseModel):
    name: str
    template: str
    input_variables: List[str]
    template_format: str = "f-string"
    validate_template: bool = True

class PromptStrategy(str, Enum):
    SIMPLE = "simple"
    CHAIN_OF_THOUGHT = "chain_of_thought"
    FEW_SHOT = "few_shot"
    ZERO_SHOT = "zero_shot"
    SELF_REFLECTION = "self_reflection"