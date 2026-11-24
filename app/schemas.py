
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Literal


# Allowed ticket values
Priority = Literal["low", "medium", "high"]
Status = Literal["open", "in_progress", "closed"]

# Allowed user roles
UserRole = Literal["customer", "support_agent"]


# Data received when creating a ticket
class TicketCreate(BaseModel):
    subject: str
    description: str
    priority: Priority = "medium"

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "examples": [
                {
                    "subject": "Login Issue",
                    "description": "Unable to login to my account.",
                    "priority": "medium"
                }
            ]
        }
    )


# Data returned when displaying a ticket
class TicketResponse(BaseModel):
    id: int
    subject: str
    description: str
    status: Status
    priority: Priority
    created_by_id: int
    assigned_to_id: int | None
    created_at: datetime | None
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


# Data received when updating a ticket
class TicketUpdate(BaseModel):
    subject: str | None = None
    description: str | None = None
    priority: Priority | None = None
    status: Status | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "priority": "high",
                    "status": "closed"
                }
            ]
        }
    )


# Data received when assigning a ticket
class TicketAssign(BaseModel):
    assigned_to_id: int


# Data received when registering a user
class UserCreate(BaseModel):
    name: str
    email: str
    password: str

    model_config = ConfigDict(extra="forbid")


# Data returned when displaying a user
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: UserRole

    model_config = ConfigDict(from_attributes=True)


# Data received during login
class LoginRequest(BaseModel):
    email: str
    password: str


# Data returned after successful login
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
