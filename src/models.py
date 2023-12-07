from pydantic import BaseModel

from typing_extensions import Literal
from typing import Optional


class MessageModel(BaseModel):
    role: Literal['system', 'user', 'assistant']
    content: str


class ConfigurationModel(BaseModel):
    model: str
    messages: list[MessageModel]
    
    seed: Optional[int] = 1234
    response_format: Optional[dict] = None
    max_tokens: Optional[int] = None
    temperature: Optional[int] = None
    top_p: Optional[int] = None