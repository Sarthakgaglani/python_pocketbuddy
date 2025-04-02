from models.offer_model import Offer, OfferOut
from bson import ObjectId
from config.database import offer_collection, locations_collection, restaurant_collection
from fastapi import HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
import shutil
import os
from datetime import datetime
from utils.cloudinary_util import upload_image
from typing import Optional
from uuid import uuid4

UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def create_offer(offer: Offer):
    try:
        offer_data = offer.dict()
        offer_data["location_id"] = ObjectId(offer_data["location_id"])
        offer_data["restaurant_id"] = ObjectId(offer_data["restaurant_id"])
        offer_data["StartDate"] = datetime.fromisoformat(offer_data["StartDate"]) if offer_data["StartDate"] else None
        offer_data["EndDate"] = datetime.fromisoformat(offer_data["EndDate"]) if offer_data["EndDate"] else None

        await offer_collection.insert_one(offer_data)
        return JSONResponse(content={"message": "Offer created successfully"}, status_code=201)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {str(e)}")


async def create_Offer_withFile(
    OfferName: str = Form(...),
    Description: str = Form(...),
    Discount: float = Form(...),
    StartDate: datetime = Form(...),
    EndDate: datetime = Form(...),
    location_id: str = Form(...),
    restaurant_id: str = Form(...),
    FoodType: str = Form(...),
    image: UploadFile = File(...)
):
    try:
        file_ext = image.filename.split(".")[-1]
        file_path = os.path.join(UPLOAD_DIR, f"{ObjectId()}.{file_ext}")

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        image_url = await upload_image(file_path)

        


        offer_data = {
            "OfferName": OfferName,
            "Description": Description,
            "Discount": Discount,
            "StartDate": StartDate,
            "EndDate": EndDate,
            "location_id": ObjectId(location_id),
            "restaurant_id": ObjectId(restaurant_id),
            "FoodType": FoodType,
            "image_url": image_url
        }
        print(offer_data)
        insertedOffer = await offer_collection.insert_one(offer_data)
        return JSONResponse(content={"message": "Offer created successfully"}, status_code=201)

    except Exception as e:
        print(f"An error occured:{str(e)}")
        raise HTTPException(status_code=500, detail=f"Error occurred: {str(e)}")






async def get_offers():
    try:
        offers = await offer_collection.find().to_list(None)  
        
        def convert_objectid_to_str(data):
            if isinstance(data,ObjectId):
                return str(data)
            elif isinstance(data,dict):
                return {k:convert_objectid_to_str(v) for k,v in data.items()}
            elif isinstance(data,list):
                return [convert_objectid_to_str(i) for i in data]
            return data

        for off in offers:
            off["_id"] = str(off["_id"])
            off["restaurant_id"] = str(off["restaurant_id"])
            off["location_id"] = str(off["location_id"])
            
            restaurant = await restaurant_collection.find_one({"_id": ObjectId(off["restaurant_id"])})
            if restaurant:
                off["restaurant" ] = convert_objectid_to_str(restaurant)
                
            location = await locations_collection.find_one({"_id": ObjectId(off["location_id"])})
            if location:
                off["location"] = convert_objectid_to_str(location)
                

        return [OfferOut(**offer) for offer in offers]

    except Exception as e:
        print(f"Error fetching offers: {str(e)}")  
        raise HTTPException(status_code=500, detail="Error while fetching offers")

async def delete_offer(offerId: str):
    result = await offer_collection.delete_one({"_id": ObjectId(offerId)})
    print("after delete result", result)
    if result.deleted_count == 1:
        return JSONResponse(status_code=200, content={"message": "Offer deleted successfully"})
    else:
        raise HTTPException(status_code=404, detail="Offer not found")

async def get_offerBy_Id(offerId:str):
    try:
        offers = await offer_collection.find_one({"_id": ObjectId(offerId)})
        if not offers:
            raise HTTPException(status_code=404, detail="Offer not found")
        
        offers["_id"] = str(offers["_id"])

        if "restaurant_id" in offers:
            restaurant = await restaurant_collection.find_one({"_id": ObjectId(offers["restaurant_id"])})
            if restaurant:
                restaurant["_id"] = str(restaurant["_id"])
                offers["restaurant"] = restaurant
            else:
                offers["restaurant"] = None

        if "location_id" in offers:
            location = await locations_collection.find_one({"_id": ObjectId(offers["location_id"])})
            if location:
                location["_id"] = str(location["_id"])
                offers["location"] = location
            else:
                offers["location"] = None
            
        return OfferOut(**offers)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid offer ID: {e}")
    
async def update_offer(
    
    
    offerID: str,
    OfferName: str = Form(...),
    Description: str = Form(...),
    Discount: float = Form(...),
    StartDate: datetime = Form(...),
    EndDate: datetime = Form(...),
    location_id: str = Form(...),
    restaurant_id: str = Form(...),
    FoodType: str = Form(...),
    image: UploadFile = File(...)
    ):
    existing_offer = offer_collection.find_one({"_id": ObjectId(offerID)})
    if not existing_offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    try:
        file_ext = image.filename.split(".")[-1]
        file_path = os.path.join(UPLOAD_DIR, f"{ObjectId()}.{file_ext}")

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        image_url = await upload_image(file_path)

        


        offer_data = {
            "OfferName": OfferName,
            "Description": Description,
            "Discount": Discount,
            "StartDate": StartDate,
            "EndDate": EndDate,
            "location_id": ObjectId(location_id),
            "restaurant_id": ObjectId(restaurant_id),
            "FoodType": FoodType,
            "image_url": image_url
        }
        print(offer_data)
        insertedOffer = await offer_collection.update_one({"_id": ObjectId(offerID)}, {"$set": offer_data})
        return JSONResponse(content={"message": "Offer updated successfully"}, status_code=201)

    except Exception as e:
        print(f"An error occured:{str(e)}")
        raise HTTPException(status_code=500, detail=f"Error occurred: {str(e)}")

# async def update_offer(offerID: str, offer_data: Offer):
#     """Update an existing offer with JSON input"""
    
#     # Check if offer exists
#     existing_offer = await offer_collection.find_one({"_id": ObjectId(offerID)})
#     if not existing_offer:
#         raise HTTPException(status_code=404, detail="Offer not found")

#     # Convert input to dictionary and remove None values
#     update_data = {k: v for k, v in offer_data.dict().items() if v is not None}

#     # Convert ObjectId fields
#     if "location_id" in update_data:
#         update_data["location_id"] = ObjectId(update_data["location_id"])
#     if "restaurant_id" in update_data:
#         update_data["restaurant_id"] = ObjectId(update_data["restaurant_id"])

#     # Convert date strings to datetime objects
#     if "StartDate" in update_data and isinstance(update_data["StartDate"], str):
#         update_data["StartDate"] = datetime.fromisoformat(update_data["StartDate"])
#     if "EndDate" in update_data and isinstance(update_data["EndDate"], str):
#         update_data["EndDate"] = datetime.fromisoformat(update_data["EndDate"])

#     # Update the offer in the database
#     await offer_collection.update_one({"_id": ObjectId(offerID)}, {"$set": update_data})

#     # Fetch and return the updated offer
#     updated_offer = await offer_collection.find_one({"_id": ObjectId(offerID)})
#     if updated_offer:
#         updated_offer["_id"] = str(updated_offer["_id"])
#         updated_offer["restaurant_id"] = str(updated_offer["restaurant_id"])
#         updated_offer["location_id"] = str(updated_offer["location_id"])

#         return {"message": "Offer updated successfully", "updated_offer": updated_offer}

#     raise HTTPException(status_code=500, detail="Error updating offer")