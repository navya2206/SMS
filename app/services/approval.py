import secrets
import string
from datetime import datetime, timezone
from sqlmodel import Session
from app.config import settings
from app.models.aca import Student
from app.models.registration import Registration, RegistrationStatus
from app.models.users import Role, User
from app.security import hash_password
from app.services.placement import get_or_create_batch, pick_section, pick_mentor_group
from app.services.roll_number import next_roll_number

def approve_registration(session: Session, registration: Registration, hod_user: User) -> dict:
    if registration.status != RegistrationStatus.pending: raise ValueError("Only pending registrations can be approved.")
    if registration.department_id != hod_user.department_id: raise PermissionError("This registration belongs to another department.")
    try:
        department = session.get(__import__('app.models.aca', fromlist=['Department']).Department, registration.department_id)
        batch = get_or_create_batch(session, department, settings.ADMISSION_YEAR); section = pick_section(session, batch); group = pick_mentor_group(session, section)
        roll = next_roll_number(session, department, settings.ADMISSION_YEAR)
        temporary = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(8))
        user = User(username=roll, full_name=registration.full_name, email=registration.email, password_hash=hash_password(temporary), role=Role.student, must_change_password=True)
        session.add(user); session.flush()
        student = Student(user_id=user.id, roll_number=roll, full_name=registration.full_name, dob=registration.dob, gender=registration.gender, phone=registration.phone, email=registration.email, parent_name=registration.parent_name, department_id=registration.department_id, batch_id=batch.id, section_id=section.id, mentor_group_id=group.id if group else None, quota=registration.quota, admission_year=settings.ADMISSION_YEAR)
        session.add(student); session.flush()
        registration.status = RegistrationStatus.approved; registration.decided_at = datetime.now(timezone.utc); registration.decided_by_user_id = hod_user.id; registration.student_id = student.id
        session.add(registration); session.commit()
        return {"roll_number": roll, "temporary_password": temporary, "section": section.name, "mentor_group": group.name if group else None, "mentor_name": None}
    except Exception:
        session.rollback(); raise
