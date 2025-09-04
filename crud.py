from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas
from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, password_hash=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_ticket(db: Session, ticket: schemas.TicketCreate, user_id: int):
    db_ticket = models.Ticket(**ticket.dict(), user_id=user_id)
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

def get_tickets(db: Session, user: models.User):
    if user.role == "admin":
        return db.query(models.Ticket).all()
    return db.query(models.Ticket).filter(models.Ticket.user_id == user.id).all()

def get_ticket(db: Session, ticket_id: int):
    return db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()

def update_ticket(db: Session, ticket_id: int, ticket_update: schemas.TicketUpdate):
    db_ticket = get_ticket(db, ticket_id)
    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    update_data = ticket_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_ticket, key, value)
    db_ticket.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

def create_asset(db: Session, asset: schemas.AssetCreate):
    db_asset = models.Asset(**asset.dict())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

def get_assets(db: Session):
    return db.query(models.Asset).all()

def create_log(db: Session, action: str, user_id: int = None):
    db_log = models.Log(action=action, user_id=user_id)
    db.add(db_log)
    db.commit()

def get_performance_stats(db: Session):
    
    avg_resolution = db.query(func.avg(models.Ticket.updated_at - models.Ticket.created_at)).filter(models.Ticket.status == "closed").scalar()
    tickets_per_tech = db.query(models.Ticket.assigned_to, func.count(models.Ticket.id)).group_by(models.Ticket.assigned_to).all()
    return {
        "avg_resolution_time": str(avg_resolution) if avg_resolution else "N/A",
        "tickets_per_technician": {tech: count for tech, count in tickets_per_tech}
    }