from models.restaurant_model import Restaurant,RestaurantOut
from bson import ObjectId
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from config.database import restaurant_collection,area_collection,city_collection,state_collection

async def addRestaurant(restaurant:Restaurant):
    savedRestaurant = await restaurant_collection.insert_one(restaurant.dict())
    return JSONResponse(content={"message:":"Restaurant Added Successfully"},status_code=201)

async def getRestaurant():
    restaurants = await restaurant_collection.find().to_list()

    for restaurant in restaurants:
        restaurant["_id"] = str(restaurant["_id"])

        if "area_id" in restaurant:
            try:
                area = await area_collection.find_one({"_id": ObjectId(restaurant["area_id"])})
                if area:
                    area["_id"] = str(area["_id"])
                    restaurant["area"] = area
            except:
                restaurant["area"] = None  # Handle invalid ObjectId
        
        if "city_id" in restaurant:
            try:
                city = await city_collection.find_one({"_id": ObjectId(restaurant["city_id"])})
                if city:
                    city["_id"] = str(city["_id"])
                    restaurant["city"] = city
            except:
                restaurant["city"] = None  # Handle invalid ObjectId

        if "state_id" in restaurant:
            try:
                state = await state_collection.find_one({"_id": ObjectId(restaurant["state_id"])})
                if state:
                    state["_id"] = str(state["_id"])
                    restaurant["state"] = state
            except:
                restaurant["state"] = None  # Handle invalid ObjectId

    return [RestaurantOut(**restaurant) for restaurant in restaurants]

async def deleteRestaurant(restaurantId:str):
    result = await restaurant_collection.delete_one({"_id":ObjectId(restaurantId)})
    print("after delete result",result)
    if result.deleted_count == 1:
        return JSONResponse(status_code=200,content={"message":"Restaurant deleted successfully"})
    else:
        raise HTTPException(status_code=404,detail="Restaurant not found")