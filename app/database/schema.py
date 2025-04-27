from datetime import datetime
from pydantic import BaseModel


class GroupCreate(BaseModel):
    address: str
    name: str = ""


class GroupMembersResponse(BaseModel):
    group_id: int
    members: list[str]


class GroupMessageResponse(BaseModel):
    username: str
    message_id: int
    time: datetime
    message_text: str


class GetGroupMessagesResponse(BaseModel):
    messages: list[GroupMessageResponse]