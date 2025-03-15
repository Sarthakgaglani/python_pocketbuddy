from fastapi import FastAPI
from routes.role_routes import router as role_router
from routes.user_routes import router as user_router
from routes.department_routes import router as department_router
from routes.employee_routes import router as employee_router
from routes.state_routes import router as state_router
from routes.city_routes import router as city_router
from routes.area_routes import router as area_router
from routes.location_routes import router as location_router
from routes.offer_routes import router as offer_router
from routes.contact_routes import router as contact_router
from routes.rating_routes import router as rating_router
from routes.restaurant_routes import router as restaurant_router
#import cors middleware
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(role_router)
app.include_router(user_router)
app.include_router(department_router)
app.include_router(employee_router)
app.include_router(state_router)
app.include_router(city_router)
app.include_router(area_router)
app.include_router(location_router)
app.include_router(offer_router)
app.include_router(contact_router)
app.include_router(rating_router)
app.include_router(restaurant_router)


#routes