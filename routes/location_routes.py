from fastapi import APIRouter
from controllers.location_controller import addLocation,getLocations,deleteLocation
from models.location_model import Location, LocationOut
from typing import List

router = APIRouter(prefix="/locations")  # Removed 'tags' parameter

@router.post("/", response_model=dict)
async def post_location(location: Location):
    return await addLocation(location)

@router.get("/", response_model=List[LocationOut])
async def get_locations():
    return await getLocations()

@router.delete("/location/{locationId}")
async def delete_location(locationId:str):
    return await deleteLocation(locationId)
