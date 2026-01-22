from fastapi import APIRouter,  HTTPException, Depends, Request
import os
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.db.models import User
from app.auth import get_current_admin
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

admin_router = APIRouter(prefix="/admin")

ADMIN_KEY = os.getenv("ADMIN_KEY")



@admin_router.get("/users")
def list_users(
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    users = db.query(User).all()

    return [
        {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "role": u.role,
            "is_blocked": u.is_blocked
        }
        for u in users
    ]


@admin_router.put("/users/{user_id}/block")
def block_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.role == "admin":
        raise HTTPException(status_code=400, detail="Cannot block admin")

    if user.id == admin.id:
        raise HTTPException(status_code=400, detail="Cannot block yourself")

    if user.is_blocked:
        return {"message": "User already blocked"}

    user.is_blocked = True
    db.commit()

    return {"message": f"User {user_id} blocked"}


@admin_router.put("/users/{user_id}/unblock")
def unblock_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.role == "admin":
        raise HTTPException(status_code=400, detail="Cannot unblock admin")

    if user.id == admin.id:
        raise HTTPException(status_code=400, detail="Cannot unblock yourself")

    if not user.is_blocked:
        return {"message": "User already active"}

    user.is_blocked = False
    db.commit()

    return {"message": f"User {user_id} unblocked"}


@admin_router.put("/users/{user_id}/make-admin")
def make_user_admin(
    user_id: int,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user.role == "admin":
        return {
            "message": "User is already an admin"
        }

    if user.is_blocked:
        raise HTTPException(
            status_code=400,
            detail="Blocked user cannot be promoted to admin"
        )

    user.role = "admin"
    db.commit()

    return {
        "message": f"User {user_id} promoted to admin"
    }

@admin_router.get("/dashboard")
def admin_dashboard(request:Request,
        current_admin = Depends(get_current_admin)):
    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request,
            "current_user": current_admin
        }
    )
