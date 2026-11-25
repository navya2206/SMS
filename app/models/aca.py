
# app/models/academics.py

from enum import Enum
from datetime import datetime, date, timezone
from typing import Optional

from sqlalchemy import UniqueConstraint, CheckConstraint
from sqlmodel import SQLModel, Field, Relationship

from app.models.users import User


# ----------------------------------------
# Student Status
# ----------------------------------------

class StudentStatus(str, Enum):
    active = "active"
    detained = "detained"
    graduated = "graduated"
    dropped = "dropped"


# ----------------------------------------
# Department Table
# ----------------------------------------

class Department(SQLModel, table=True):

    __tablename__ = "department"

    id: int | None = Field(default=None, primary_key=True)

    code: str = Field(
        unique=True,
        index=True,
        max_length=10
    )

    name: str = Field(max_length=100)

    intake: int = Field(default=120)

    hod_user_id: int | None = Field(
        default=None,
        foreign_key="user.id"
    )


# ----------------------------------------
# Batch Table
# ----------------------------------------

class Batch(SQLModel, table=True):

    __tablename__ = "batch"

    __table_args__ = (
        CheckConstraint(
            "end_year = start_year + 4",
            name="check_batch_duration"
        ),
    )

    id: int | None = Field(default=None, primary_key=True)

    department_id: int = Field(
        foreign_key="department.id"
    )

    start_year: int

    end_year: int


# ----------------------------------------
# Section Table
# ----------------------------------------

class Section(SQLModel, table=True):

    __tablename__ = "section"

    __table_args__ = (
        CheckConstraint(
            "current_year BETWEEN 1 AND 4",
            name="check_section_year"
        ),
        CheckConstraint(
            "current_semester BETWEEN 1 AND 8",
            name="check_section_semester"
        ),
    )

    id: int | None = Field(default=None, primary_key=True)

    batch_id: int = Field(
        foreign_key="batch.id"
    )

    name: str = Field(max_length=5)

    current_year: int

    current_semester: int

    capacity: int = Field(default=60)


# ----------------------------------------
# Mentor Group Table
# ----------------------------------------

class MentorGroup(SQLModel, table=True):

    __tablename__ = "mentor_group"

    id: int | None = Field(default=None, primary_key=True)

    section_id: int = Field(
        foreign_key="section.id"
    )

    name: str = Field(max_length=100)

    mentor_user_id: int = Field(
        foreign_key="user.id"
    )

    capacity: int = Field(default=30)


# ----------------------------------------
# Student Table
# ----------------------------------------

class Student(SQLModel, table=True):

    __tablename__ = "student"

    id: int | None = Field(default=None, primary_key=True)

    user_id: int = Field(
        unique=True,
        foreign_key="user.id"
    )

    roll_number: str = Field(
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

    batch_id: int = Field(
        foreign_key="batch.id"
    )

    section_id: int = Field(
        foreign_key="section.id"
    )

    mentor_group_id: Optional[int] = Field(
        default=None,
        foreign_key="mentor_group.id"
    )

    quota: str = Field(max_length=30)

    admission_year: int

    status: StudentStatus = Field(
        default=StudentStatus.active
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    # Relationships for easier template access

    user: User = Relationship()

    department: Department = Relationship()

    section: Section = Relationship()

    mentor_group: Optional[MentorGroup] = Relationship()


# ----------------------------------------
# Subject Table
# ----------------------------------------

class Subject(SQLModel, table=True):

    __tablename__ = "subject"

    id: int | None = Field(default=None, primary_key=True)

    code: str = Field(
        max_length=30,
        index=True
    )

    name: str = Field(max_length=150)

    department_id: int = Field(
        foreign_key="department.id"
    )

    year: int

    semester: int

    credits: int


# ----------------------------------------
# Teaching Assignment Table
# ----------------------------------------

class TeachingAssignment(SQLModel, table=True):

    __tablename__ = "teaching_assignment"

    id: int | None = Field(default=None, primary_key=True)

    subject_id: int = Field(
        foreign_key="subject.id"
    )

    section_id: int = Field(
        foreign_key="section.id"
    )

    teacher_user_id: int = Field(
        foreign_key="user.id"
    )


# ----------------------------------------
# Roll Counter Table
# ----------------------------------------

class RollCounter(SQLModel, table=True):

    __tablename__ = "roll_counter"

    __table_args__ = (
        UniqueConstraint(
            "department_id",
            "admission_year",
            name="uq_roll_counter_department_year"
        ),
    )

    id: int | None = Field(default=None, primary_key=True)

    department_id: int = Field(
        foreign_key="department.id"
    )

    admission_year: int

    last_serial: int = Field(default=0)
