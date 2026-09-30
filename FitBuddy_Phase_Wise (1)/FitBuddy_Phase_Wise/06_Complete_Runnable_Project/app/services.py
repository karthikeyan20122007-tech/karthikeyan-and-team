from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import Plan, User
from .schemas import UserInput


def save_user(db: Session, data: UserInput) -> User:
    user = db.scalar(select(User).where(User.user_id == data.user_id))
    if user is None:
        user = User(user_id=data.user_id, name=data.name, age=data.age, weight=data.weight, goal=data.goal, intensity=data.intensity)
        db.add(user)
    else:
        user.name, user.age, user.weight, user.goal, user.intensity = data.name, data.age, data.weight, data.goal, data.intensity
    db.commit()
    db.refresh(user)
    return user


def save_plan(db: Session, user_id: str, original_plan: str, nutrition_tip: str) -> Plan:
    plan = Plan(user_id=user_id, original_plan=original_plan, nutrition_tip=nutrition_tip)
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan


def get_latest_plan(db: Session, user_id: str) -> Plan | None:
    return db.scalar(select(Plan).where(Plan.user_id == user_id).order_by(Plan.created_at.desc()).limit(1))


def update_plan(db: Session, plan: Plan, updated_plan: str, feedback: str) -> Plan:
    plan.updated_plan = updated_plan
    plan.feedback = feedback
    db.commit()
    db.refresh(plan)
    return plan


def get_user(db: Session, user_id: str) -> User | None:
    return db.scalar(select(User).where(User.user_id == user_id))


def get_all_users(db: Session) -> list[User]:
    return list(db.scalars(select(User).order_by(User.created_at.desc())).all())


def delete_user(db: Session, user_id: str) -> bool:
    user = get_user(db, user_id)
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True
