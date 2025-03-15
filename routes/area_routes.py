from fastapi import APIRouter,HTTPException
from controllers.area_controller import addArea,getArea,deleteArea
from models.area_model import Area,AreaOut
from bson import ObjectId

router = APIRouter()

@router.post("/area/")
async def post_area(area:Area):
    return await addArea(area)

@router.get("/area/")
async def get_area():
    return await getArea()

@router.delete("/area/{areaId}")
async def delete_area(areaId:str):
    return await deleteArea(areaId)