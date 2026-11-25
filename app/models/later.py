
# app/models/later.py

from enum import Enum
from datetime import datetime, date
from typing import Optional

from sqlalchemy import UniqueConstraint, CheckConstraint
from sqlmodel import SQLModel, Field

from app.models.users import Role


# ----------------------------------------
# Attendance Status
# ----------------------------------------

class AttendanceStatus(str, Enum):
    present = "present"
    absent = "absent"
    late = "late"


# ----------------------------------------
# Exam Type
# ----------------------------------------

class ExamType(str, Enum):
    mid1 = "mid1"
    mid2 = "mid2"
    internal = "internal"
    semester = "semester"


# ----------------------------------------
# Leave Status
# ----------------------------------------

class LeaveStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


# ----------------------------------------
# Attendance Table
# ----------------------------------------

class Attendance(SQLModel, table=True):

    __tablename__ = "attendance"

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "date",
            "period",
            name="uq_attendance_student_date_period"
        ),
        CheckConstraint(
            "period BETWEEN 1 AND 7",
            name="check_attendance_period"
        ),
    )

    id: int | None = Field(default=None, primary_key=True)

    student_id: int = Field(
        foreign_key="student.id",
        index=True
    )

    section_id: int = Field(
        foreign_key="section.id"
    )

    date: date

    period: int

    status: AttendanceStatus

    marked_by_user_id: int = Field(
        foreign_key="user.id"
    )


# ----------------------------------------
# Mark Table
# ----------------------------------------

class Mark(SQLModel, table=True):

    __tablename__ = "mark"

    id: int | None = Field(default=None, primary_key=True)

    student_id: int = Field(
        foreign_key="student.id",
        index=True
    )

    subject_id: int = Field(
        foreign_key="subject.id"
    )

    exam_type: ExamType

    max_marks: float

    marks_obtained: float

    entered_by_user_id: int = Field(
        foreign_key="user.id"
    )


# ----------------------------------------
# Exam Table
# ----------------------------------------

class Exam(SQLModel, table=True):

    __tablename__ = "exam"

    id: int | None = Field(default=None, primary_key=True)

    name: str = Field(max_length=150)

    department_id: int = Field(
        foreign_key="department.id"
    )

    year: int

    semester: int

    start_date: date

    end_date: date

    is_published: bool = Field(default=False)


# ----------------------------------------
# Exam Schedule Table
# ----------------------------------------

class ExamSchedule(SQLModel, table=True):

    __tablename__ = "exam_schedule"

    id: int | None = Field(default=None, primary_key=True)

    exam_id: int = Field(
        foreign_key="exam.id"
    )

    subject_id: int = Field(
        foreign_key="subject.id"
    )

    exam_date: date

    session: str = Field(max_length=5)

    room: str = Field(max_length=50)


# ----------------------------------------
# Hall Ticket Table
# ----------------------------------------

class HallTicket(SQLModel, table=True):

    __tablename__ = "hall_ticket"

    id: int | None = Field(default=None, primary_key=True)

    exam_id: int = Field(
        foreign_key="exam.id"
    )

    student_id: int = Field(
        foreign_key="student.id"
    )

    ticket_no: str = Field(
        unique=True,
        index=True,
        max_length=50
    )

    is_eligible: bool

    reason: Optional[str] = Field(default=None)

    generated_at: datetime = Field(
        default_factory=datetime.utcnow
    )


# ----------------------------------------
# Leave Request Table
# ----------------------------------------

class LeaveRequest(SQLModel, table=True):

    __tablename__ = "leave_request"

    id: int | None = Field(default=None, primary_key=True)

    student_id: int = Field(
        foreign_key="student.id",
        index=True
    )

    from_date: date

    to_date: date

    reason: str

    status: LeaveStatus = Field(
        default=LeaveStatus.pending
    )

    decided_by_user_id: Optional[int] = Field(
        default=None,
        foreign_key="user.id"
    )


# ----------------------------------------
# Notice Table
# ----------------------------------------

class Notice(SQLModel, table=True):

    __tablename__ = "notice"

    id: int | None = Field(default=None, primary_key=True)

    title: str = Field(max_length=200)

    body: str

    audience: str = Field(max_length=30)

    department_id: Optional[int] = Field(
        default=None,
        foreign_key="department.id"
    )

    section_id: Optional[int] = Field(
        default=None,
        foreign_key="section.id"
    )

    role: Optional[Role] = Field(default=None)

    created_by_user_id: int = Field(
        foreign_key="user.id"
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )
