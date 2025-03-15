from models.rating_model import Rating,RatingOut
from bson import ObjectId
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException, Depends, status
from config.database import rating_collection,offer_collection

async def addRating(rating:Rating):
    savedRating= await rating_collection.insert_one(rating.dict())
    return JSONResponse(content={"message":"Rating Added Successfully"},status_code=201)

async def getRating():
    ratings = await rating_collection.find().to_list()

    for rating in ratings:
        # if "offer_id" in rating and isinstance(rating["offer_id"],ObjectId):
        #     rating["offer_id"]=str(rating["offer_id"])

        #     offer = await offer_collection.find_one({"_id":ObjectId(rating["offer_id"])})
        #     if offer:
        #         rating["_id"] = str(offer["_id"])
        #         rating["offer"] = offer

        if "offer_id" in rating:
            try:
                offer = await offer_collection.find_one({"_id": ObjectId(rating["offer_id"])})
                if offer:
                    offer["_id"] = str(offer["_id"])
                    rating["offer"] = offer
            except:
                rating["offer"] = None  # Handle invalid ObjectId

    return[RatingOut(**rating)for rating in ratings]

async def deleteRating(ratingId:str):
    result = await rating_collection.delete_one({"_id":ObjectId(ratingId)})
    print("after delete result",result)
    if result.deleted_count == 1:
        return JSONResponse(status_code=200,content={"message":"Rating deleted successfully"})
    else:
        raise HTTPException(status_code=404,detail="Rating not found")
