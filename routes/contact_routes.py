from fastapi import APIRouter
from controllers.contact_controller import addContact,getContact,deleteContact
from models.contact_model import Contact,ContactOut


router = APIRouter()

@router.post("/contact")
async def post_contact(contact:Contact):
    return await addContact(contact)

@router.get("/contact")
async def get_contact():
    return await getContact()

@router.delete("/contact/{contactId}")
async def delete_contact(contactId: str):
    return await deleteContact(contactId)