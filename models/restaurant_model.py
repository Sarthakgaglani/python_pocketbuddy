from pydantic import BaseModel,Field,validator
from typing import List,Optional,Dict,Any
from bson import ObjectId


class Restaurant(BaseModel):
    Name:str
    Category:str
    area_id:str
    city_id:str
    state_id:str

class RestaurantOut(Restaurant):
    id:str = Field(alias="_id")
    area: Optional[Dict[str, Any]] = None
    city: Optional[Dict[str, Any]] = None
    state: Optional[Dict[str, Any]] = None

    @validator("id",pre=True,always=True)
    def convert_objectId(cls,v):
        if isinstance(v,ObjectId):
            return str(v)
        return v
    
    @validator("area","city","state",pre=True,always=True)
    def convert_state(cls,v):
        if isinstance(v,dict) and "_id" in v:
            v["_id"] = str(v["_id"])
        return v
