from models.user_model import User,UserOut,UserLogin
from bson import ObjectId
from config.database import user_collection,role_collection
from fastapi import HTTPException
from fastapi.responses import JSONResponse
import bcrypt
from utils.send_mail import send_mail


async def addUser(user:User):
    user.role_id = ObjectId(user.role_id)
    print("after type cast",user.role_id)
    result = await user_collection.insert_one(user.dict())
    send_mail(user.email,"User created","User created successfully")
    return JSONResponse(status_code=200,content={"message":"User created successfully"})

async def getAllUsers():
    users = await user_collection.find().to_list()

    for user in users:
        if "role_id" in user and isinstance(user["role_id"], ObjectId):
            user["role_id"] = str(user["role_id"])
        

        role = await role_collection.find_one({"_id": ObjectId(user["role_id"])})  
        
        if role:
            role["_id"] = str(role["_id"])  # Convert role _id to string
            user["role"] = role

    return [UserOut(**user) for user in users]

async def loginUser(request:UserLogin):
#async def loginUser(email:str,password:str):
    #norma; password : plain text --> encr
    
    foundUser = await user_collection.find_one({"email":request.email})
    print(":foundUser",foundUser)
    
    foundUser["_id"] = str(foundUser["_id"])
    foundUser["role_id"] = str(foundUser["role_id"])
    
    if foundUser is None:
        raise HTTPException(status_code=404,detail="User not found")
    #compare password
    if "password" in foundUser and bcrypt.checkpw(request.password.encode(),foundUser["password"].encode()):
        #database role.. roleid
        role = await role_collection.find_one({"_id":ObjectId(foundUser["role_id"])})
        foundUser["role"] = role
        return {"message":"user login success","user":UserOut(**foundUser)}
    else:
        raise HTTPException(status_code=404,detail="Invalid password")
    
async def deleteUser(userId:str):
    result = await user_collection.delete_one({"_id":ObjectId(userId)})
    print("after delete result",result)
    if result.deleted_count == 1:
        return JSONResponse(status_code=200,content={"message":"User deleted successfully"})
    else:
        raise HTTPException(status_code=404,detail="User not found")
    