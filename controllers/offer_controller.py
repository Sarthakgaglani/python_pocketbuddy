from models.offer_model import Offer,OfferOut
from bson import ObjectId
from config.database import offer_collection,locations_collection,restaurant_collection
from fastapi import HTTPException,APIRouter,UploadFile,File,Form
from fastapi.responses import JSONResponse
import shutil
import os
from datetime import datetime
from utils.cloudinary_util import upload_image

UPLOAD_DIR = "uploads/"  # Folder where images will be stored
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def create_offer(offer:Offer):
    print(offer.dict())
    offer.location_id=ObjectId(offer.location_id)
    offer.restaurant_id=ObjectId(offer.restaurant_id)
    savedOffer = await offer_collection.insert_one(offer.dict())
    return JSONResponse(content={"message":"Offer created successfully"},status_code=201)

async def create_Offer_withFile(
    OfferName: str = Form(...),
    Description: str = Form(...),
    Discount: float = Form(...),
    StartDate: datetime = Form(...),
    EndDate: datetime = Form(...),
    location_id: str = Form(...),
    restaurant_id: str = Form(...),
    FoodType:str=Form(...),
    image: UploadFile= File(...)

):
    try:
        os.makedirs(UPLOAD_DIR,exist_ok=True)

        file_ext = image.filename.split(".")[-1]
        file_path = os.path.join(UPLOAD_DIR, f"{ObjectId()}.{file_ext}")
        with open(file_path,"wb") as buffer:
            shutil.copyfileobj(image.file,buffer)
        image_url = await upload_image(file_path)
        offer_data={
            "OfferName":OfferName,
            "Description":Description,
            "Discount":Discount,
            "StartDate":StartDate,
            "EndDate":EndDate,
            "location_id":str(ObjectId(location_id)),

            "restaurant_id":str(ObjectId(restaurant_id)),
            "FoodType":FoodType,
            # "image_url":f"/static/{file.filename}"
            "image_url":image_url
        }
        print(offer_data)
        insertedOffer = await offer_collection.insert_one(offer_data)

        return JSONResponse(
            content={
                "message":"Offer created successfully"
            },
            status_code=201
        )
    except Exception as e:
        print(f"An error occured:{str(e)}")
        raise HTTPException(status_code=500,detail=f"An Error Occured:{str(e)}")

async def getoffers():
    try:
        offers = await offer_collection.find().to_list(None)

        def convert_objectid_to_str(data):
            """Recursively converts ObjectId fields to strings."""
            if isinstance(data, ObjectId):
                return str(data)
            elif isinstance(data, dict):
                return {k: convert_objectid_to_str(v) for k, v in data.items()}
            elif isinstance(data, list):
                return [convert_objectid_to_str(i) for i in data]
            return data
        
        for off in offers:
            off["_id"]= str(off["_id"])
            off["location_id"]= str(off["location_id"])
            off["restaurant_id"]= str(off["restaurant_id"])
            

            restaurant = await restaurant_collection.find_one({"_id":ObjectId(off["restaurant_id"])})
            if restaurant:
                off["restaurant"] = convert_objectid_to_str(restaurant)

            location = await locations_collection.find_one({"_id":ObjectId(off["location_id"])})
            if location:
                off["location"] = convert_objectid_to_str(location)

        return [OfferOut(**offer)for offer in offers]
    

    except Exception as e:
        print(f"An error occured:{str(e)}")
        raise HTTPException(status_code=500,detail="An Error Occured While Fetching Offers")

async def deleteOffer(offerId: str):
    result = await offer_collection.delete_one({"_id": ObjectId(offerId)})
    print("after delete result", result)
    if result.deleted_count == 1:
        return JSONResponse(status_code=200, content={"message": "Offer deleted successfully"})
    else:
        raise HTTPException(status_code=404, detail="Offer not found")