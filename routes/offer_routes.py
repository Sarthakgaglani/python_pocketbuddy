# # # from fastapi import APIRouter
# # # from controllers.offer_controller import addOffer,getOffers
# # # from models.offer_model import Offer,OfferOut
# # # from bson import ObjectId

# # # router = APIRouter()

# # # @router.post("/postoffer/")
# # # async def post_offer(offer:Offer):
# # #     return await addOffer(offer)

# # # @router.get("/getoffers/")
# # # async def get_Offers():
# # #     return await getOffers()

# # from fastapi import APIRouter, UploadFile, File, Form
# # from controllers.offer_controller import addOffer,getOffers
# # from fastapi.staticfiles import StaticFiles

# # router = APIRouter()

# # # Mount the uploads directory so images can be accessed
# # router.mount("/static", StaticFiles(directory="uploads"), name="static")

# # @router.post("/postoffer/")
# # async def post_offer(
# #     name: str = Form(...),
# #     discount: float = Form(...),
# #     restaurant_id: str = Form(...),
# #     image: UploadFile = File(...)
# # ):
# #     return await addOffer(name, discount, restaurant_id, image)

# # @router.get("/getoffers/")
# # async def get_Offers():
# #     return await getOffers()


# from fastapi import APIRouter, UploadFile, File, Form
# from models.offer_model import Offer,OfferOut
# from controllers.offer_controller import create_offer,create_Offer_withFile

# router = APIRouter()
# @router.post("/postoffer/")
# async def post_offer(offer:Offer):
#     print(offer)
#     return await create_offer(offer)

# @router.post("/create_offer_withFile/")
# async def create_offer(offer:Offer):
#     print(offer)
#     return await create_Offer_withFile(offer)

from fastapi import APIRouter, UploadFile, File, Form, Depends
from models.offer_model import Offer, OfferOut
from controllers.offer_controller import create_offer, create_Offer_withFile,getoffers,deleteOffer
from datetime import datetime
router = APIRouter()

@router.post("/postoffer/")
async def create_offer(offer: Offer):
    print(offer)
    return await create_offer(offer)

@router.post("/create_Offer_withFile/")
async def create_offer(
    OfferName: str = Form(...),
    Description: str = Form(...),
    Discount: float = Form(...),
    StartDate: datetime =Form(...),
    EndDate: datetime =Form(...),
    location_id:str=Form(...),
    restaurant_id: str = Form(...),
    FoodType:str=Form(...),
    image: UploadFile = File(...)
):
    return await create_Offer_withFile(
        OfferName, Description, Discount, StartDate,EndDate,location_id, restaurant_id,FoodType, image)

@router.get("/getoffers/")
async def get_offers():
    return await getoffers()

@router.delete("/offer/{offerId}")
async def delete_offer(offerId:str):
    return await deleteOffer(offerId)

