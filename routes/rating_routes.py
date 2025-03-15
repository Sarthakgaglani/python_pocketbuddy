from fastapi import APIRouter
from controllers.rating_controller import addRating,getRating,deleteRating
from models.rating_model import Rating,RatingOut

router = APIRouter()

@router.post("/rating")
async def post_rating(rating:Rating):
    return await addRating(rating)

@router.get("/rating")
async def get_rating():
    return await getRating()

@router.delete("/rating/{ratingId}")
async def delete_rating(ratingId:str):
    return await deleteRating(ratingId)