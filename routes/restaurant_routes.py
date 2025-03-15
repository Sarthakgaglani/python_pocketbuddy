from fastapi import APIRouter
from controllers.restaurant_controller import addRestaurant,getRestaurant,deleteRestaurant
from models.restaurant_model import Restaurant,RestaurantOut

router = APIRouter()

@router.post("/restaurant/")
async def post_restaurant(restaurant:Restaurant):
    return await addRestaurant(restaurant)

@router.get("/restaurant/")
async def get_restaurant():
    return await getRestaurant()

@router.delete("/restaurant/{contactId}")
async def delete_restaurant(restaurantId: str):
    return await deleteRestaurant(restaurantId)

