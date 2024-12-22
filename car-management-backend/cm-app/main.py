from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from repo.databaseConfig import engine
from repo.models import Base
from routers.maintenance_router import maintenance_router
from routers.garage_router import garage_router
from routers.car_router import car_router

def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    yield
app = FastAPI(lifespan=lifespan)
# added because of the cross-origin access is blocked
# by third party client
origins = [ "http://localhost:3000",
            "http://192.168.100.3:3000",
            "http://localhost:8088", ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello Mundo"}


app.include_router(garage_router,prefix="/garages", tags=["garage-controller"])
app.include_router(car_router,prefix="/cars", tags=["car-controller"])

app.include_router(maintenance_router,prefix="/maintenance", tags=["maintenance-controller"])