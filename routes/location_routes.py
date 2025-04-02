from fastapi import APIRouter
from controllers.location_controller import addLocation,getAllLocations,deleteLocation,getLocationById
from models.location_model import Location, LocationOut
from typing import List

router = APIRouter(prefix="/locations")  # Removed 'tags' parameter

@router.post("/locations/")
async def post_location(location: Location):
    return await addLocation(location)

@router.get("/getLocations/")
async def get_locations():
    return await getAllLocations()

@router.delete("/location/{locationId}")
async def delete_location(locationId:str):
    return await deleteLocation(locationId)


@router.get("/getlocationById/{locationId}")
async def get_location_by_location_id(locationId:str):
    return await getLocationById(locationId)
