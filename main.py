import os
from fastapi import FastAPI, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from . import models, schemas, crud, auth, notifications
from .routes import user, ticket, asset 
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI(title="IT Helpdesk System")

 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user.router)
app.include_router(ticket.router)
app.include_router(asset.router)

models.Base.metadata.create_all(bind=models.engine)

@app.post("/users/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(auth.get_db)):
    return crud.create_user(db, user)

@app.get("/users/me", response_model=schemas.UserOut)
def get_current_user_info(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(auth.get_db)):
    user = crud.get_user_by_username(db, form_data.username)
    if not user or not auth.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/tickets/", response_model=schemas.TicketOut)
def submit_ticket(ticket: schemas.TicketCreate, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(auth.get_db)):
    new_ticket = crud.create_ticket(db, ticket, current_user.id)
    notifications.send_notification(f"New ticket {new_ticket.id} created")
    crud.create_log(db, f"Ticket {new_ticket.id} created by {current_user.username}")
    return new_ticket

@app.get("/tickets/", response_model=list[schemas.TicketOut])
def read_tickets(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(auth.get_db)):
    return crud.get_tickets(db, current_user)

@app.get("/tickets/{ticket_id}", response_model=schemas.TicketOut)
def read_ticket(ticket_id: int, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(auth.get_db)):
    ticket = crud.get_ticket(db, ticket_id)
    if not ticket or (current_user.role != "admin" and ticket.user_id != current_user.id):
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@app.put("/tickets/{ticket_id}", response_model=schemas.TicketOut)
def update_ticket_status(ticket_id: int, ticket_update: schemas.TicketUpdate, current_user: models.User = Depends(auth.get_current_admin), db: Session = Depends(auth.get_db)):
    updated_ticket = crud.update_ticket(db, ticket_id, ticket_update)
    notifications.send_notification(f"Ticket {ticket_id} updated to {updated_ticket.status}")
    crud.create_log(db, f"Ticket {ticket_id} updated by {current_user.username}")
   
    if (datetime.utcnow() - updated_ticket.created_at).days > 3 and updated_ticket.status != "closed":
        updated_ticket.escalation_level += 1
        db.commit()
        notifications.send_notification(f"Ticket {ticket_id} escalated to level {updated_ticket.escalation_level}")
    return updated_ticket

@app.post("/assets/", response_model=schemas.AssetOut)
def create_asset(asset: schemas.AssetCreate, current_user: models.User = Depends(auth.get_current_admin), db: Session = Depends(auth.get_db)):
    return crud.create_asset(db, asset)

@app.get("/assets/", response_model=list[schemas.AssetOut])
def read_assets(current_user: models.User = Depends(auth.get_current_admin), db: Session = Depends(auth.get_db)):
    return crud.get_assets(db)

@app.get("/stats/")
def get_stats(current_user: models.User = Depends(auth.get_current_admin), db: Session = Depends(auth.get_db)):
    return crud.get_performance_stats(db)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    notifications.websocket_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
          
    except WebSocketDisconnect:
        notifications.websocket_connections.remove(websocket)
        


