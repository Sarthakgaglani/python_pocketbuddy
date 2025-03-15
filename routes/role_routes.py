from fastapi import APIRouter
from models.role_model import Role,RoleOut
from controllers.role_controller import getAllRoles,addRole,deleteRole,getRoleById

router = APIRouter()

@router.get("/roles/")
async def get_roles():
    return await getAllRoles() #promise
#{name:"",descr:""}

@router.post("/role/")
async def post_role(role:Role):
    return await addRole(role)


@router.delete("/role/{roleId}")
async def delete_role(roleId:str):
    return await deleteRole(roleId)

@router.get("/role/{roleId}")
async def get_role_byId(roleId:str):
    return await getRoleById(roleId)