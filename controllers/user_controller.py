from models.user_model import User,UserOut,UserLogin,ResetPasswordReq
from bson import ObjectId
from config.database import user_collection,role_collection
from fastapi import HTTPException
from fastapi.responses import JSONResponse
import bcrypt
from utils.send_mail import send_mail
import jwt
import datetime 

async def addUser(user:User):
    # user.role_id = ObjectId(user.role_id)
    # print("after type cast",user.role_id)
    result = await user_collection.insert_one(user.dict())
    send_mail(user.email,"User created","User created successfully")
    return JSONResponse(status_code=200,content={"message":"User created successfully"})

async def getAllUsers():
    users = await user_collection.find().to_list()
    if len(users)==0:
        return JSONResponse(status_code=404,content={"message":"No States Found"})
    # for user in users:
    #     if "role_id" in user and isinstance(user["role_id"], ObjectId):
    #         user["role_id"] = str(user["role_id"])
        

    #     role = await role_collection.find_one({"_id": ObjectId(user["role_id"])})  
        
    #     if role:
    #         role["_id"] = str(role["_id"])  # Convert role _id to string
    #         user["role"] = role

    return [UserOut(**user) for user in users]

async def loginUser(request:UserLogin):
#async def loginUser(email:str,password:str):
    #norma; password : plain text --> encr
    
    foundUser = await user_collection.find_one({"email":request.email})
    print(":foundUser",foundUser)
    
    foundUser["_id"] = str(foundUser["_id"])
    # foundUser["role_id"] = str(foundUser["role_id"])
    
    if foundUser is None:
        raise HTTPException(status_code=404,detail="User not found")
    #compare password
    if "password" in foundUser and bcrypt.checkpw(request.password.encode(),foundUser["password"].encode()):
        #database role.. roleid
        # role = await role_collection.find_one({"_id":ObjectId(foundUser["role_id"])})
        # foundUser["role"] = role
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


# forgot password
SECRET_KEY = "pocketbuddy"
def generate_token(email:str):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    payload={"sub":email,"exp":expiration}
    token =jwt.encode(payload,SECRET_KEY,algorithm="HS256")
    return token

async def forgotPassword(email:str):
    foundUser = await user_collection.find_one({"email":email})
    if not foundUser:
        raise HTTPException(status_code=404,detail="Email not found")
    
    token = generate_token(email)
    resetLink = f"http://localhost:5173/resetpassword/{token}"
    body =f""" 
    <html>
        <h1>HELLO THIS IS RESET PASSWORD LINK EXPIRES IN 30 MINUTES</h1>
        <a href="{resetLink}">Click here to reset your password</a>
        <p>Thank you</p>
        <p>Team Pocket Buddy</p>
    </html>
        
    """

    subject = "Reset Password"
    send_mail(email,subject,body)
    return {"message":"Reset password link sent to your email"}

async def resetPassword(data:ResetPasswordReq):
    try:
        payload = jwt.decode(data.token,SECRET_KEY,algorithms="HS256")
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=421,detail="Invalid token...")
        
        hashed_password = bcrypt.hashpw(data.password.encode("utf-8"),bcrypt.gensalt())
        await user_collection.update_one({"email":email},{"$set":{"password":hashed_password}})

        return {"message":"Password reset successfully"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=500,detail="jwt token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=500,detail="jwt Invalid token")
        