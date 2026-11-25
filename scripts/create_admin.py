"""Create the temporary management account used during Day 1 testing."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from sqlmodel import Session, select
from app.database import create_db_and_tables, engine
from app.models.users import Role, User
from app.security import hash_password

create_db_and_tables()
with Session(engine) as session:
    user = session.exec(select(User).where(User.username == "management@college.edu")).first()
    if not user:
        user = User(username="management@college.edu", full_name="College Management", email="management@college.edu", password_hash=hash_password("Admin@123"), role=Role.management)
        session.add(user); session.commit()
    print("Management login: management@college.edu / Admin@123")
