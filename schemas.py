from pydantic import BaseModel
from datetime import datetime


class TicketBase(BaseModel):
    description: str
    priority: str = "medium"

class TicketCreate(TicketBase):
    pass

class TicketUpdate(BaseModel):
    status: str | None = None
    assigned_to: int | None = None
    priority: str | None = None

class TicketOut(TicketBase):
    id: int
    status: str
    escalation_level: int
    assigned_to: int | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AssetBase(BaseModel):
    name: str
    status: str = "available"
    location: str

class AssetCreate(AssetBase):
    assigned_to: int | None = None
    ticket_id: int | None = None

class AssetOut(AssetBase):
    id: int
    assigned_to: int | None
    ticket_id: int | None

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str
    role: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str