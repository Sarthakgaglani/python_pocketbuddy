from models.city_model import City, CityOut
from bson import ObjectId
from fastapi.responses import JSONResponse
from fastapi import APIRouter,HTTPException
from config.database import city_collection,state_collection


async def addCity(city:City):
    savedCity = await city_collection.insert_one(city.dict())
    return JSONResponse(content={"message:":"City Added Successfully"},status_code=201)

async def getCity():
    cities = await city_collection.find().to_list()

    for city in cities:
        if "state_id" in city and isinstance(city["state_id"],ObjectId):
            city["state_id"] = str(city["state_id"])
        
        state = await state_collection.find_one({"_id":ObjectId(city["state_id"])})
        if state:
            state["_id"] = str(city["_id"])
            city["state"] = state

    return [CityOut(**city) for city in cities] 

async def deleteCity(cityId:str):
    result = await city_collection.delete_one({"_id":ObjectId(cityId)})
    print("after delete result",result)
    if result.deleted_count == 1:
        return JSONResponse(status_code=200,content={"message":"City deleted successfully"})
    else:
        raise HTTPException(status_code=404,detail="City not found")