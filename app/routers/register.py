from datetime import date
from pathlib import Path
import uuid
from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import Session, select
from app.config import settings
from app.database import get_session
from app.main import templates
from app.models.aca import Department
from app.models.registration import Registration, RegistrationStatus

router = APIRouter()
UPLOAD_ROOT = Path("app/static/uploads/registrations")
ALLOWED = {".jpg", ".jpeg", ".png", ".pdf"}

def page(request, departments, **extra):
    return templates.TemplateResponse("register/form.html", {"request": request, "departments": departments, **extra})

@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request, session: Session = Depends(get_session)):
    return page(request, session.exec(select(Department).order_by(Department.code)).all())

def validate_upload(upload: UploadFile, name: str) -> str | None:
    suffix = Path(upload.filename or "").suffix.lower()
    if suffix not in ALLOWED:
        return f"{name} must be JPG, PNG, or PDF."
    if upload.size and upload.size > 2 * 1024 * 1024:
        return f"{name} must be 2 MB or smaller."
    return None

@router.post("/register")
async def submit_registration(request: Request, full_name: str = Form(...), dob: date = Form(...), gender: str = Form(...), phone: str = Form(...), email: str = Form(...), parent_name: str = Form(...), department_id: int = Form(...), quota: str = Form(...), entrance_rank: int | None = Form(None), tenth_percent: float = Form(...), inter_percent: float = Form(...), photo: UploadFile = File(...), marks_memo: UploadFile = File(...), id_proof: UploadFile = File(...), session: Session = Depends(get_session)):
    departments = session.exec(select(Department).order_by(Department.code)).all()
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    errors = []
    if len(phone) != 10 or not phone.isdigit(): errors.append("Phone must contain exactly 10 digits.")
    if not 0 <= tenth_percent <= 100 or not 0 <= inter_percent <= 100: errors.append("Percentages must be between 0 and 100.")
    if age < 16: errors.append("Student must be at least 16 years old.")
    for upload, label in ((photo, "Photo"), (marks_memo, "Marks memo"), (id_proof, "ID proof")):
        error = validate_upload(upload, label)
        if error: errors.append(error)
    if errors: return page(request, departments, error=" ".join(errors))
    reference = f"REG-{settings.ADMISSION_YEAR}-{(session.exec(select(Registration).order_by(Registration.id.desc())).first().id + 1 if session.exec(select(Registration).order_by(Registration.id.desc())).first() else 1):05d}"
    folder = UPLOAD_ROOT / reference; folder.mkdir(parents=True, exist_ok=True)
    paths = {}
    for key, upload in (("photo", photo), ("marks_memo", marks_memo), ("id_proof", id_proof)):
        target = folder / f"{key}{Path(upload.filename).suffix.lower()}"
        target.write_bytes(await upload.read()); paths[key] = str(target)
    registration = Registration(reference_no=reference, full_name=full_name, dob=dob, gender=gender, phone=phone, email=email, parent_name=parent_name, department_id=department_id, quota=quota, entrance_rank=entrance_rank, tenth_percent=tenth_percent, inter_percent=inter_percent, photo_path=paths["photo"], marks_memo_path=paths["marks_memo"], id_proof_path=paths["id_proof"])
    session.add(registration); session.commit()
    return RedirectResponse(f"/register/done/{reference}", status_code=303)

@router.get("/register/done/{reference_no}", response_class=HTMLResponse)
def registration_done(request: Request, reference_no: str):
    return templates.TemplateResponse("register/done.html", {"request": request, "reference_no": reference_no})

@router.get("/register/status", response_class=HTMLResponse)
def registration_status(request: Request, reference_no: str | None = None, session: Session = Depends(get_session)):
    registration = session.exec(select(Registration).where(Registration.reference_no == reference_no)).first() if reference_no else None
    department = session.get(Department, registration.department_id) if registration else None
    return templates.TemplateResponse("register/status.html", {"request": request, "registration": registration, "department": department, "reference_no": reference_no or ""})
