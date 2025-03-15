from models.state_model import State,StateOut
from bson import ObjectId
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from config.database import state_collection

async def addState(state:State):
    savedState = await state_collection.insert_one(state.dict())
    if savedState:
        return JSONResponse(status_code=201,content={"message:":"State Added Successfully"})
    raise HTTPException(status_code=500,detail="Internal Server Error")

async def getStates():
    states = await state_collection.find().to_list()
    if len(states)==0:
        return JSONResponse(status_code=404,content={"message":"No States Found"})
    
    return [StateOut(**state) for state in states]

async def deleteState(stateId:str):
    result = await state_collection.delete_one({"_id":ObjectId(stateId)})
    print("after delete result",result)
    if result.deleted_count == 1:
        return JSONResponse(status_code=200,content={"message":"State deleted successfully"})
    else:
        raise HTTPException(status_code=404,detail="State not found")