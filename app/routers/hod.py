from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import Session, select
from app.database import get_session
from app.deps import require_role
from app.main import templates
from app.models.registration import Registration, RegistrationStatus
from app.models.users import Role, User
from app.services.approval import approve_registration

router = APIRouter()

@router.get("/hod/registrations", response_class=HTMLResponse)
def registrations(request: Request, status: str | None = None, user: User = Depends(require_role(Role.hod)), session: Session = Depends(get_session)):
    rows = session.exec(select(Registration).where(Registration.department_id == user.department_id).order_by(Registration.id.desc())).all()
    if status: rows = [row for row in rows if row.status.value == status]
    return templates.TemplateResponse("hod/registrations.html", {"request": request, "user": user, "rows": rows})

@router.get("/hod/registrations/{registration_id}", response_class=HTMLResponse)
def detail(request: Request, registration_id: int, user: User = Depends(require_role(Role.hod)), session: Session = Depends(get_session)):
    registration = session.get(Registration, registration_id)
    if not registration or registration.department_id != user.department_id: return HTMLResponse("Not found", status_code=404)
    return templates.TemplateResponse("hod/detail.html", {"request": request, "user": user, "registration": registration})

@router.post("/hod/registrations/{registration_id}/approve", response_class=HTMLResponse)
def approve(request: Request, registration_id: int, user: User = Depends(require_role(Role.hod)), session: Session = Depends(get_session)):
    registration = session.get(Registration, registration_id)
    if not registration or registration.department_id != user.department_id: return HTMLResponse("Not found", status_code=404)
    try: result = approve_registration(session, registration, user)
    except (ValueError, PermissionError) as exc: return HTMLResponse(str(exc), status_code=400)
    return templates.TemplateResponse("hod/result.html", {"request": request, "user": user, "registration": registration, "result": result})

def decide(registration_id, user, session, status, remarks):
    registration = session.get(Registration, registration_id)
    if not registration or registration.department_id != user.department_id: return HTMLResponse("Not found", status_code=404)
    if not remarks.strip(): return HTMLResponse("Remarks are required", status_code=400)
    if registration.status != RegistrationStatus.pending: return HTMLResponse("This registration has already been decided", status_code=400)
    registration.status = status; registration.hod_remarks = remarks; session.add(registration); session.commit()
    return RedirectResponse("/hod/registrations", status_code=303)

@router.post("/hod/registrations/{registration_id}/reject")
def reject(registration_id: int, remarks: str = Form(...), user: User = Depends(require_role(Role.hod)), session: Session = Depends(get_session)): return decide(registration_id, user, session, RegistrationStatus.rejected, remarks)

@router.post("/hod/registrations/{registration_id}/correction")
def correction(registration_id: int, remarks: str = Form(...), user: User = Depends(require_role(Role.hod)), session: Session = Depends(get_session)): return decide(registration_id, user, session, RegistrationStatus.correction, remarks)
