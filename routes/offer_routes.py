from fastapi import APIRouter, UploadFile, File, Form,HTTPException
from controllers.offer_controller import create_offer, create_Offer_withFile, get_offers, delete_offer,get_offerBy_Id,update_offer
from models.offer_model import Offer
from datetime import datetime
from typing import Optional

from config.database import offer_collection

router = APIRouter()

@router.post("/postoffer/")
async def create_offer(offer: Offer):
    return await create_offer(offer)

@router.post("/create_with_File/")
async def create_offer_with_file(
    OfferName: str = Form(...),
    Description: str = Form(...),
    Discount: float = Form(...),
    StartDate: datetime = Form(...),
    EndDate: datetime = Form(...),
    location_id: str = Form(...),
    restaurant_id: str = Form(...), 
    FoodType: str = Form(...),
    image: UploadFile = File(...),

    
):
    
    # try:
    #     # Convert MM/DD/YYYY format to datetime
    #     parsed_start_date = datetime.strptime(StartDate, "%m/%d/%Y")
    #     parsed_end_date = datetime.strptime(EndDate, "%m/%d/%Y")

        return await create_Offer_withFile(
            OfferName, Description, Discount, StartDate, EndDate, 
            location_id, restaurant_id, FoodType, image
        )
    
    # except ValueError:
    #     return {"error": "Invalid date format. Please use MM/DD/YYYY."}
    
    # return await create_Offer_withFile(OfferName, Description, Discount, StartDate, EndDate, location_id, restaurant_id, FoodType, image)


# @router.post("/create_User_with_File/")
# async def create_offer_with_file(
#     OfferName: str = Form(...),
#     Description: str = Form(...),
#     Discount: float = Form(...),
#     StartDate: datetime = Form(...),
#     EndDate: datetime = Form(...),
#     location_id: str = Form(...),
#     restaurant_id: str = Form(...), 
#     FoodType: str = Form(...),
#     image: UploadFile = File(...)
# ):
#      return await create_UserOffer_withFile(
#             OfferName, Description, Discount, StartDate, EndDate, 
#             location_id, restaurant_id, FoodType, image
#         )


@router.get("/getoffers/")
async def getoffers():
    return await get_offers()



@router.delete("/offer/{offerId}")
async def deleteoffer(offerId: str):
    return await delete_offer(offerId)

@router.get("/get_offerBy_id/{offerId}")
async def getofferbyId(offerId:str):
     return await get_offerBy_Id(offerId)

@router.put("/offer/{offerID}")
async def update_existing_offer(offerID: str, OfferName: str = Form(...),
    Description: str = Form(...),
    Discount: float = Form(...),
    StartDate: datetime = Form(...),
    EndDate: datetime = Form(...),
    location_id: str = Form(...),
    restaurant_id: str = Form(...), 
    FoodType: str = Form(...),
    image: UploadFile = File(...),
   
    ):
    return await update_offer(offerID, OfferName, Description, Discount, StartDate, EndDate, 
            location_id, restaurant_id, FoodType, image )