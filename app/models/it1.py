
# app/models/__init__.py

# User models
from app.models.users import (
    Role,
    User,
)

# Academic models
from app.models.aca import (
    StudentStatus,
    Department,
    Batch,
    Section,
    MentorGroup,
    Student,
    Subject,
    TeachingAssignment,
    RollCounter,
)

# Registration models
from app.models.registration import (
    RegistrationStatus,
    Registration,
)

# Day 2 and Day 3 models
from app.models.later import (
    AttendanceStatus,
    ExamType,
    LeaveStatus,
    Attendance,
    Mark,
    Exam,
    ExamSchedule,
    HallTicket,
    LeaveRequest,
    Notice,
)


__all__ = [
    "Role",
    "User",
    "StudentStatus",
    "Department",
    "Batch",
    "Section",
    "MentorGroup",
    "Student",
    "Subject",
    "TeachingAssignment",
    "RollCounter",
    "RegistrationStatus",
    "Registration",
    "AttendanceStatus",
    "ExamType",
    "LeaveStatus",
    "Attendance",
    "Mark",
    "Exam",
    "ExamSchedule",
    "HallTicket",
    "LeaveRequest",
    "Notice",
]
