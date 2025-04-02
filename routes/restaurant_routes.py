from fastapi import APIRouter
from controllers.restaurant_controller import addRestaurant,getAllRestaurant,deleteRestaurant,getRestaurantById
from models.restaurant_model import Restaurant,RestaurantOut

router = APIRouter()

@router.post("/restaurant/")
async def post_restaurant(restaurant:Restaurant):
    return await addRestaurant(restaurant)

@router.get("/getRestaurant/")
async def get_restaurant():  
    return await getAllRestaurant()

@router.delete("/restaurant/{restaurantId}")
async def delete_restaurant(restaurantId: str):
    return await deleteRestaurant(restaurantId)

@router.get("/getRestaurantById/{restaurant_id}")
async def get_restaurant_by_restaurant_id(restaurant_id:str):
    return await getRestaurantById(restaurant_id)
