from pydantic import BaseModel,Field,validator,EmailStr
from typing import List,Dict,Optional,Any
from bson import ObjectId

class Cont(BaseModel):
    name:str
    email:EmailStr
    message:str

class ContOut(Cont):
    id:str = Field (alias="_id")

    @validator("id",pre=True,always=True)
    def convert_objectId(cls,v):
        if isinstance(v,ObjectId):
            return str(v)
        return v