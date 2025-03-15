from models.area_model import Area, AreaOut
from bson import ObjectId
from config.database import area_collection, city_collection, state_collection
from fastapi.responses import JSONResponse
from fastapi import HTTPException, APIRouter

async def addArea(area:Area):
    savedArea = await area_collection.insert_one(area.dict())
    return JSONResponse(content={"message:":"Area Added Successfully"},status_code=201)

async def getArea():
    areas = await area_collection.find().to_list()

    for area in areas:
        if "city_id" in area and isinstance(area["city_id"],ObjectId):
            area["city_id"] = str(area["city_id"])

        city = await city_collection.find_one({"_id":ObjectId(area["city_id"])})
        if city:
            area["_id"] =str(area["_id"])
            area["city"] = city
            
        # state = await state_collection.find_one({"_id":ObjectId(city["state_id"])})
        # if state:
        #     state["_id"] = str(state["_id"])
        #     city["state"] = state

    return [AreaOut(**area) for area in areas]

async def deleteArea(areaId:str):
    result = await area_collection.delete_one({"_id":ObjectId(areaId)})
    print("after delete result",result)
    if result.deleted_count == 1:
        return JSONResponse(status_code=200,content={"message":"Area deleted successfully"})
    else:
        raise HTTPException(status_code=404,detail="Area not found")




