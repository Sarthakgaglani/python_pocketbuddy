from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL ="mongodb://localhost:27017"
DATABASE_NAME = "python"

client = AsyncIOMotorClient(MONGO_URL)
db = client[DATABASE_NAME]
role_collection = db["roles"]
user_collection = db["users"]
department_collection = db["departments"]
employee_collection = db["employees"]
state_collection = db["states"]
city_collection = db["cities"]
area_collection = db["areas"]
locations_collection = db["locations"]
offer_collection = db["offers"]
contact_collection = db["contacts"]
rating_collection= db["ratings"]
restaurant_collection= db["restaurants"]
cont_collection = db["contact_us"]