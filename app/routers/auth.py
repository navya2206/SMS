from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import Session, select
from app.database import get_session
from app.deps import get_current_user
from app.main import templates
from app.models.users import User
from app.security import create_access_token, hash_password, verify_password

router = APIRouter()

def destination(user: User) -> str:
    return {"management": "/management", "hod": "/hod", "mentor": "/mentor", "trainer": "/trainer", "student": "/student"}.get(user.role.value, "/login")

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login", response_class=HTMLResponse)
def login(request: Request, username: str = Form(...), password: str = Form(...), session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == username)).first()
    if not user or not verify_password(password, user.password_hash):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Wrong username or password"}, status_code=401)
    response = RedirectResponse("/change-password" if user.must_change_password else destination(user), status_code=303)
    response.set_cookie("access_token", create_access_token(user.id, user.role.value), httponly=True, samesite="lax")
    return response

@router.get("/change-password", response_class=HTMLResponse)
def change_password_page(request: Request, user: User = Depends(get_current_user)):
    return templates.TemplateResponse("change_password.html", {"request": request, "user": user})

@router.post("/change-password", response_class=HTMLResponse)
def change_password(request: Request, new_password: str = Form(...), confirm_password: str = Form(...), user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    if len(new_password) < 8 or new_password != confirm_password:
        return templates.TemplateResponse("change_password.html", {"request": request, "user": user, "error": "Passwords must match and contain at least 8 characters."}, status_code=400)
    user.password_hash = hash_password(new_password)
    user.must_change_password = False
    session.add(user); session.commit()
    return RedirectResponse(destination(user), status_code=303)

@router.get("/logout")
def logout():
    response = RedirectResponse("/login", status_code=303)
    response.delete_cookie("access_token")
    return response
