from sqlmodel import Session, select
from app.models.aca import Department, RollCounter

def next_roll_number(session: Session, department: Department, admission_year: int) -> str:
    counter = session.exec(select(RollCounter).where(RollCounter.department_id == department.id, RollCounter.admission_year == admission_year)).first()
    if not counter:
        counter = RollCounter(department_id=department.id, admission_year=admission_year)
        session.add(counter); session.flush()
    counter.last_serial += 1
    # A counter avoids duplicate numbers when students are approved concurrently.
    session.add(counter); session.flush()
    return f"{admission_year % 100:02d}{department.code}{counter.last_serial:03d}"
