from fastapi import APIRouter
from utils.get_data import get_recomendations
from models.search import RecomendationsRequest

router = APIRouter(prefix="/api")

@router.post("/generate_recomendations/")
async def generate_recomandations(request: RecomendationsRequest):
    return await get_recomendations(request.data1, request.data2)
