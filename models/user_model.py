from pydantic import BaseModel,Field,validator
from bson import ObjectId
from typing import Optional, Dict, Any
import bcrypt   #pip install bcrypt



class User(BaseModel):
    firstName:str
    lastName:str
    age:int
   
    role:str
    email:str
    password:str
    
    #10,11,12,13,14,15,16,20,,,25,31
    # @validator("password",pre=True,always=True)
    # def encrypt_password(cls,v):
    #     if v is None:
    #         return None
    #     return bcrypt.hashpw(v.encode("utf-8"),bcrypt.gensalt())
    @validator("password", pre=True, always=True)
    def encrypt_password(cls, v):
        if v is None:
            return None
        if isinstance(v, bytes):  # If already hashed, return it as a string
            return v.decode("utf-8")  
        return bcrypt.hashpw(v.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        


class UserOut(User):
    firstName:Optional[str] = None
    lastName:Optional[str] = None
    age:Optional[int] = None
    id:str = Field(alias="_id")    
    # role:Optional[Dict[str,Any]] = None
    role:Optional[str] = None
    email:Optional[str] = None
    password:Optional[str] = None
    
    @validator("id",pre=True,always=True)
    def convert_objectId(cls,v):
        if isinstance(v,ObjectId):
            return str(v)
        return v
    
    # @validator("role", pre=True, always=True)
    # def convert_role(cls, v):
    #     if isinstance(v, dict) and "_id" in v:
    #         v["_id"] = str(v["_id"])  # Convert role _id to string
    #     return v
    
class UserLogin(BaseModel):
    email:str
    password:str   

class ResetPasswordReq(BaseModel):
    token:str
    password:str
    