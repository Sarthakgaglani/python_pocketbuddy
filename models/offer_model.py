from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from bson import ObjectId
from datetime import datetime

class Offer(BaseModel): 
    OfferName: Optional[str]
    Description: Optional[str]
    Discount: Optional[float]
    StartDate: Optional[datetime]  # Use datetime for proper parsing
    EndDate: Optional[datetime]
    location_id: Optional[str]
    restaurant_id: Optional[str]
    image_url: Optional[str] = None
    FoodType: Optional[str]

    

class OfferOut(BaseModel):
    id: str = Field(alias="_id")
    OfferName: Optional[str]
    Description: Optional[str]
    Discount: Optional[float]
    StartDate: Optional[datetime]
    EndDate: Optional[datetime]
    location_id: Optional[str]
    restaurant_id: Optional[str] 
    image_url: Optional[str] = None
    FoodType: Optional[str]
    restaurant: Optional[Dict[str, Any]] = None
    location: Optional[Dict[str, Any]] = None

    

    

    @validator("id", "location_id", "restaurant_id", pre=True, always=True)
    def convert_objectid_to_str(cls, v):
        return str(v) if isinstance(v, ObjectId) else v

    @validator("location", "restaurant", pre=True, always=True)
    def convert_nested_objectid(cls, v):
        if isinstance(v, dict) and "_id" in v:
            v["_id"] = str(v["_id"])
        return v
    
    # @validator("StartDate", "EndDate", pre=True, always=True)
    # def convert_datetime_to_str(cls, v):
    #     return v.strftime("%m/%d/%Y") if isinstance(v, datetime) else v
