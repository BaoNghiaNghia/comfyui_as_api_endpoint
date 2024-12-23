from pydantic import BaseModel

# Request model for LLM
class LLMRequest(BaseModel):
    positive_prompt: str

# Request model for image generation
class PromptRequest(BaseModel):
    positive_prompt: str
    thumbnail_number: int = 5
    thumb_style: str
    domain: str
    token: str
