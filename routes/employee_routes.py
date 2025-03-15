from fastapi import APIRouter
from controllers.employee_controller import createEmployee,getAllEmployee
from models.employee_model import Employee,EmployeeOut

router = APIRouter()

@router.post("/emp/")
async def post_employee(employee:Employee):
    return await createEmployee(employee)

@router.get('/emp/')
async def get_employee():
    return await getAllEmployee()