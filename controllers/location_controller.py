from models.location_model import Location, LocationOut
from bson import ObjectId
from config.database import locations_collection
from fastapi import HTTPException
from fastapi.responses import JSONResponse

async def addLocation(location: Location):
    savedLocation = await locations_collection.insert_one(location.dict(exclude_none=True))
    
    if not savedLocation.inserted_id:
        raise HTTPException(status_code=500, detail="Failed to add location")

    return JSONResponse(content={"message": "Location added successfully"}, status_code=201)

async def getAllLocations():
    Locations = await locations_collection.find().to_list(length=100)
    
    for loc in Locations:
        loc["id"] = str(loc["_id"])
        loc.setdefault("open_timing", None)
        loc.setdefault("close_timing", None)
    
    return [LocationOut(**loc) for loc in Locations]



async def getLocationById(location_id:str):
    result = await locations_collection.find_one({"_id":ObjectId(location_id)})
    print(result)    
    return LocationOut(**result)



async def deleteLocation(locationId: str):
    result = await locations_collection.delete_one({"_id": ObjectId(locationId)})
    print("after delete result", result)
    if result.deleted_count == 1:
        return JSONResponse(status_code=200, content={"message": "Location deleted successfully"})
    else:
        raise HTTPException(status_code=404, detail="Location not found")

