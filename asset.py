from fastapi import APIRouter

router = APIRouter()
@router.get("/assets")
def get_assets():
    return {"message": "Asset list"}