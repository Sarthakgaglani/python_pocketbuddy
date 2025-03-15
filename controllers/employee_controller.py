from models.employee_model import Employee,EmployeeOut
from bson import ObjectId
from config.database import department_collection,employee_collection

async def createEmployee(employee:Employee):
    
    employee.department_id = ObjectId(employee.department_id)
    result = await employee_collection.insert_one(employee.dict())
    return {"message":"employee created with department.."}

async def getAllEmployee():
    employess = await employee_collection.find().to_list(length=None)
    
    for employee in employess:
        if "department_id" in employee and isinstance(employee["department_id"],ObjectId):
            employee["department_id"] = str(employee["department_id"])
        
        department = await department_collection.find_one({"_id":ObjectId(employee["department_id"])})            
        if department:
            department["_id"]= str(department["_id"])
            employee["department"]= department
        
    return [EmployeeOut(**emp) for emp in employess]        
    
        
    
    