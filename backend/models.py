from pydantic import BaseModel

# Request model for LLM
class LLMRequest(BaseModel):
    positive_prompt: str

# Request model for image generation
class PromptRequest(BaseModel):
    positive_prompt: str
    poster_number: int = 5
    domain: str
    token: str
