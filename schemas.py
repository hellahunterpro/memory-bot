from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


# Что приходит когда создаём нового человека
class PersonCreate(BaseModel):
    name: str
    category: str = "friends"
    context: str = ""
    avatar_url: str = ""


# Что приходит когда обновляем (все поля опциональные)
class PersonUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    context: Optional[str] = None
    avatar_url: Optional[str] = None


# Что отдаём наружу когда читают
class PersonOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    category: str
    context: str
    avatar_url: str
    created_at: datetime
    updated_at: datetime


# ===== СОБЫТИЯ =====

class EventCreate(BaseModel):
    title: str
    description: str = ""
    event_type: str = "meeting"
    location: str = ""
    occurred_at: Optional[datetime] = None


class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    event_type: Optional[str] = None
    location: Optional[str] = None
    occurred_at: Optional[datetime] = None


class EventOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    event_type: str
    location: str
    occurred_at: datetime
    created_at: datetime


# ===== ИСТОРИИ =====

class StoryCreate(BaseModel):
    title: str
    description: str = ""
    icon: str = "book"
    color: str = "blue"
    status: str = "active"


class StoryUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    status: Optional[str] = None


class StoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    icon: str
    color: str
    status: str
    created_at: datetime
