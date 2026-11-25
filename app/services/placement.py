from sqlmodel import Session, select, func
from app.models.aca import Batch, Section, MentorGroup, Student

def get_or_create_batch(session, department, admission_year):
    batch = session.exec(select(Batch).where(Batch.department_id == department.id, Batch.start_year == admission_year)).first()
    if not batch:
        batch = Batch(department_id=department.id, start_year=admission_year, end_year=admission_year + 4); session.add(batch); session.flush()
    return batch

def _count(session, model, field, value):
    return session.exec(select(func.count()).select_from(model).where(field == value)).one()

def pick_section(session, batch):
    sections = session.exec(select(Section).where(Section.batch_id == batch.id).order_by(Section.name)).all()
    for section in sections:
        if _count(session, Student, Student.section_id, section.id) < section.capacity: return section
    name = chr(ord('A') + len(sections))
    section = Section(batch_id=batch.id, name=name, current_year=1, current_semester=1); session.add(section); session.flush(); return section

def pick_mentor_group(session, section):
    groups = session.exec(select(MentorGroup).where(MentorGroup.section_id == section.id)).all()
    available = [g for g in groups if _count(session, Student, Student.mentor_group_id, g.id) < g.capacity]
    return min(available, key=lambda g: _count(session, Student, Student.mentor_group_id, g.id), default=None)
