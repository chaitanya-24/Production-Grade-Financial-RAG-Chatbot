from typing import Dict, Any
from app.models.prompt import PromptTemplate, PromptStrategy

class PromptManager:
    def __init__(self):
        self.templates: Dict[str, PromptTemplate] = {}
        
    def add_template(self, template: PromptTemplate):
        self.templates[template.name] = template
        
    def get_template(self, name: str) -> PromptTemplate:
        return self.templates.get(name)
        
    def format_prompt(self, template_name: str, **kwargs) -> str:
        template = self.get_template(template_name)
        if not template:
            raise ValueError(f"Template {template_name} not found")
            
        return template.template.format(**kwargs)