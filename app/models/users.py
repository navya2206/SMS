
# app/models/users.py

from enum import Enum
from datetime import datetime

from sqlmodel import SQLModel, Field


class Role(str, Enum):
    management = "management"
    hod = "hod"
    mentor = "mentor"
    trainer = "trainer"
    student = "student"


class User(SQLModel, table=True):

    __tablename__ = "user"

    id: int | None = Field(default=None, primary_key=True)

    username: str = Field(
        unique=True,
        index=True,
        max_length=100
    )

    full_name: str = Field(max_length=150)

    email: str = Field(max_length=150)

    password_hash: str

    role: Role

    department_id: int | None = Field(
        default=None,
        foreign_key="department.id"
    )

    is_active: bool = Field(default=True)

    must_change_password: bool = Field(default=False)

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )
