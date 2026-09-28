from pydantic import BaseModel


class PromptRequest(BaseModel):
    prompt: str
    character: str = "Hero"
    setting: str = "forest"
    tone: str = "dramatic"
    style: str = "comic book"
