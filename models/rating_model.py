from pydantic import BaseModel,Field,validator,conint
from typing import List,Optional,Any,Dict
from bson import ObjectId

class Rating(BaseModel):
    comments:str
    rating: int
    offer_id:str

class RatingOut(Rating):
    id:str = Field(alias="_id")
    offer:Optional[Dict[str,Any]]=None

    @validator("id",pre=True,always=True)
    def convert_objectid(cls,v):
        if isinstance(v,ObjectId):
            return str(v)
        return v
    
    @validator("offer",pre=True,always=True)
    def convert_offer(cls,v):
        if isinstance(v,dict) and "_id" in v:
            v["_id"] = str(v["_id"])
        return v
