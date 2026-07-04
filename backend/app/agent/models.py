from pydantic import BaseModel


class AgentAction(BaseModel):
    tool: str
    arguments: dict


class AgentResponse(BaseModel):
    success: bool
    response: str
