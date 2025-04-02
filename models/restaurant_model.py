from pydantic import BaseModel,Field,validator
from typing import List,Optional,Dict,Any
from bson import ObjectId


class Restaurant(BaseModel):
    Name:str
    Category:str
    state: Optional[str]=None
    city: Optional[str]=None
    area: Optional[str] =None
    
    

class RestaurantOut(Restaurant):
    id:str = Field(alias="_id") 
    
    
    
    @validator("id",pre=True,always=True)
    def convert_objectId(cls,v):
        if isinstance(v,ObjectId):
            return str(v)
        return v
    
    
