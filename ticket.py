from fastapi import APIRouter

router = APIRouter()
@router.get("/tickets")
def get_tickets():
    return {"message": "Ticket list"}