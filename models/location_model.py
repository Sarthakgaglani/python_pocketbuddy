from pydantic import BaseModel,Field,validator
from typing import List,Optional,Dict,Any
from bson import ObjectId

class Location(BaseModel):
    Location:str
    title:str
    category:str
    description:str
    timing:str
    is_active:bool

class LocationOut(Location):
    id:str = Field(alias="_id")

    @validator("id",pre=True,always=True)
    def convert_objectId(cls,v):
        if isinstance(v,ObjectId):
            return str(v)
        if isinstance(v, str) and ObjectId.is_valid(v):
            return v
        raise ValueError("Invalid ObjectId format")
    
    @validator("is_active",pre=True,always=True)
    def convert_is_active(cls,v):
        if v == 1:
            return True
        return False
    

