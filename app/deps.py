from collections.abc import Callable
from fastapi import Depends, HTTPException, Request
from sqlmodel import Session
from app.database import get_session
from app.models.users import Role, User
from app.security import decode_access_token

def get_current_user(request: Request, session: Session = Depends(get_session)) -> User:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=303, headers={"Location": "/login"})
    try:
        user = session.get(User, int(decode_access_token(token)["sub"]))
    except Exception as exc:
        raise HTTPException(status_code=303, headers={"Location": "/login"}) from exc
    if not user or not user.is_active:
        raise HTTPException(status_code=303, headers={"Location": "/login"})
    return user

def require_role(*roles: Role) -> Callable:
    allowed = {role.value if isinstance(role, Role) else str(role) for role in roles}
    def dependency(user: User = Depends(get_current_user)) -> User:
        if user.role.value not in allowed:
            raise HTTPException(status_code=403, detail="You do not have access to this page.")
        return user
    return dependency
