from pydantic import BaseModel,Field,validator
from typing import List,Optional,Dict,Any
from bson import ObjectId

class Location(BaseModel):
    Location:str
    description:str
    open_timing:Optional[str]= None
    close_timing:Optional[str]=None
    

class LocationOut(Location):
    id:str = Field(alias="_id")

    @validator("id",pre=True,always=True)
    def convert_objectId(cls,v):
        if isinstance(v,ObjectId):
            return str(v)
        if isinstance(v, str) and ObjectId.is_valid(v):
            return v
        raise ValueError("Invalid ObjectId format")
    
    
    

