from fastapi import APIRouter
from controllers.department_controller import addDepartment,getAllDepartments
from models.department_model import Department,DepartmentOut


#create an object of fastapiRouter
router = APIRouter()

@router.post("/dept/")
async def post_createDepartment(department:Department):
    return await addDepartment(department)

@router.get("/dept/")
async def get_departments():
    return await getAllDepartments()