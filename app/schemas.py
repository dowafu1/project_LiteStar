from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field

class UserRead(BaseModel):
    id: UUID
    name: str
    surname: str
    created_at: datetime.now
    updated_at: datetime.now

class UserCreate(BaseModel):
    name: str
    surname: str
    password: str

class UserUpdate(BaseModel):
    name: str | None = None
    surname: str | None = None
    password: str | None = None
