
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from bson import ObjectId

class Contact(BaseModel):
   
    Address: str
    city_id: str
    area_id: str
    FoodType: str
    Latitude: float
    Longitude: float

class ContactOut(Contact):
    id: str = Field(alias="_id")
    city: Optional[Dict[str, Any]] = None
    area: Optional[Dict[str, Any]] = None

    @validator("id", pre=True, always=True)
    def convert_objectId(cls, v):
        return str(v) if isinstance(v, ObjectId) else v

    @validator("city", pre=True, always=True)
    def convert_city(cls, v):
        if isinstance(v, dict) and "_id" in v:
            v["_id"] = str(v["_id"])
        return v or None  # ✅ Ensure return is not empty

    @validator("area", pre=True, always=True)
    def convert_area(cls, v):
        if isinstance(v, dict) and "_id" in v:
            v["_id"] = str(v["_id"])
        return v or None  # ✅ Ensure return is not empty
