
# app/models/registration.py

from enum import Enum
from datetime import datetime, date
from typing import Optional

from sqlmodel import SQLModel, Field


# ----------------------------------------
# Registration Status
# ----------------------------------------

class RegistrationStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    correction = "correction"


# ----------------------------------------
# Registration Table
# ----------------------------------------

class Registration(SQLModel, table=True):

    __tablename__ = "registration"

    id: int | None = Field(default=None, primary_key=True)

    reference_no: str = Field(
        unique=True,
        index=True,
        max_length=30
    )

    full_name: str = Field(max_length=150)

    dob: date

    gender: str = Field(max_length=20)

    phone: str = Field(max_length=15)

    email: str = Field(max_length=150)

    parent_name: str = Field(max_length=150)

    department_id: int = Field(
        foreign_key="department.id"
    )

    quota: str = Field(max_length=30)

    entrance_rank: Optional[int] = Field(default=None)

    tenth_percent: float

    inter_percent: float

    photo_path: Optional[str] = Field(default=None)

    marks_memo_path: Optional[str] = Field(default=None)

    id_proof_path: Optional[str] = Field(default=None)

    status: RegistrationStatus = Field(
        default=RegistrationStatus.pending
    )

    hod_remarks: Optional[str] = Field(default=None)

    submitted_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    decided_at: Optional[datetime] = Field(default=None)

    decided_by_user_id: Optional[int] = Field(
        default=None,
        foreign_key="user.id"
    )

    student_id: Optional[int] = Field(
        default=None,
        foreign_key="student.id"
    )
