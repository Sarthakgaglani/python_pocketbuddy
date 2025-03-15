from models.contact_model import Contact,ContactOut 
from bson import ObjectId
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Depends, HTTPException, status
from config.database import contact_collection, city_collection, area_collection

async def addContact(contact:Contact):
    savedContact= await contact_collection.insert_one(contact.dict())
    return JSONResponse(content={"message":"Contact Added Successfully"},status_code=201)

# async def getContact():
#     contacts = await contact_collection.find().to_list()

#     for contact in contacts:
#         if "city_id" in contact and isinstance(contact["city_id"],ObjectId):
#             contact["city_id"] = str(contact["city_id"])

#             city = await city_collection.find_one({"_id":ObjectId(contact["city_id"])})
#             if city:
#                 city["_id"] = str(city["_id"])
#                 contact["city"] = city
                
#         if "area_id" in contact and isinstance(contact["area_id"],ObjectId):
#             contact["area_id"] = str(contact["area_id"])

#             area =await area_collection.find_one({"_id"})
#             if area:
#                 area["_id"]= str(area["_id"])
#                 contact["area"] = area
#     return [ContactOut(**contact) for contact in contacts]

async def getContact():
    contacts = await contact_collection.find().to_list(length=1000)  # ✅ Added length

    for contact in contacts:
        contact["_id"] = str(contact["_id"])  # ✅ Convert ObjectId to string

        # ✅ Convert city_id to ObjectId before querying
        if "city_id" in contact:
            try:
                city = await city_collection.find_one({"_id": ObjectId(contact["city_id"])})
                if city:
                    city["_id"] = str(city["_id"])
                    contact["city"] = city
            except:
                contact["city"] = None  # Handle invalid ObjectId

        # ✅ Convert area_id to ObjectId before querying
        if "area_id" in contact:
            try:
                area = await area_collection.find_one({"_id": ObjectId(contact["area_id"])})
                if area:
                    area["_id"] = str(area["_id"])
                    contact["area"] = area
            except:
                contact["area"] = None  # Handle invalid ObjectId

    return [ContactOut(**contact) for contact in contacts]
    

async def deleteContact(contactId:str):
    result = await contact_collection.delete_one({"_id":ObjectId(contactId)})
    print("after delete result",result)
    if result.deleted_count == 1:
        return JSONResponse(status_code=200,content={"message":"Contact deleted successfully"})
    else:
        raise HTTPException(status_code=404,detail="Contact not found")

