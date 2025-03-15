from fastapi import APIRouter
from controllers.user_controller import addUser,getAllUsers,loginUser,deleteUser
from models.user_model import User,UserOut,UserLogin

router = APIRouter()

@router.post("/user/")
async def post_user(user:User):
    return await addUser(user)

@router.get("/users/")
async def get_users():
    return await getAllUsers()

@router.post("/user/login/")
async def login_user(user:UserLogin):
    return await loginUser(user)

@router.delete("/user/{userId}")
async def delete_user(userId:str):
    return await deleteUser(userId)