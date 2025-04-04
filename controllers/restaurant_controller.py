from models.restaurant_model import Restaurant,RestaurantOut
from bson import ObjectId
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from config.database import restaurant_collection,area_collection,city_collection,state_collection

async def addRestaurant(restaurant:Restaurant):
    savedRestaurant = await restaurant_collection.insert_one(restaurant.dict())
    return JSONResponse(content={"message:":"Restaurant Added Successfully"},status_code=201)


# async def getAllRestaurant():
#     restaurants = await restaurant_collection.find().to_list()
#     if len(restaurants) == 0:
#         return JSONResponse(status_code=404,content={"message":"No Restaurants Found"})
#     return [RestaurantOut(**restaurant) for restaurant in restaurants] 

async def getAllRestaurant():
    restaurants = await restaurant_collection.find().to_list() 
    if len(restaurants) == 0:
        return JSONResponse(status_code=404,content={"message":"No Restaurants Found"})
    return [RestaurantOut(**restaurant) for restaurant in restaurants]

 


async def getRestaurantById(restaurant_id: str):
    try:
        restaurant = await restaurant_collection.find_one({"_id": ObjectId(restaurant_id)})
        
        if not restaurant:
            raise HTTPException(status_code=404, detail="Restaurant not found")

        restaurant["_id"] = str(restaurant["_id"])

        # Fetch related area
        if "area_id" in restaurant:
            area = await area_collection.find_one({"_id": ObjectId(restaurant["area_id"])})

            if area:
                area["_id"] = str(area["_id"])
                restaurant["area"] = area
            else:
                restaurant["area"] = None

        # Fetch related city
        if "city_id" in restaurant:
            city = await city_collection.find_one({"_id": ObjectId(restaurant["city_id"])})

            if city:
                city["_id"] = str(city["_id"])
                restaurant["city"] = city
            else:
                restaurant["city"] = None

        # Fetch related state
        if "state_id" in restaurant:
            state = await state_collection.find_one({"_id": ObjectId(restaurant["state_id"])})

            if state:
                state["_id"] = str(state["_id"])
                restaurant["state"] = state
            else:
                restaurant["state"] = None

        return RestaurantOut(**restaurant)

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid restaurant ID: {e}")

async def deleteRestaurant(restaurantId:str):
    result = await restaurant_collection.delete_one({"_id":ObjectId(restaurantId)})
    print("after delete result",result)
    if result.deleted_count == 1:
        return JSONResponse(status_code=200,content={"message":"Restaurant deleted successfully"})
    else:
        raise HTTPException(status_code=404,detail="Restaurant not found")