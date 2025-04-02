from models.cont_model import Cont,ContOut
from bson import ObjectId
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException
from config.database import cont_collection

async def addCont(cont:Cont):
    savedCont= await cont_collection.insert_one(cont.dict())
    return JSONResponse(content={"message":"Added successfully"},status_code=201)

async def getCont():
    conts = await cont_collection.find().to_list()
    if len(conts) == 0:
        return JSONResponse(status_code=404,content={"message":"No states Found"})
    
    return [ContOut(**cont) for cont in conts]

async def deleteCont(contId:str):
    result = await cont_collection.delete_one({"_id":ObjectId(contId)})
    print("after delete result",result)
    if result.deleted_count == 1:
        return JSONResponse(status_code=200,content={"message":"Contact us deleted successfully"})
    else:
        raise HTTPException(status_code=404,detail="Contact us not found")