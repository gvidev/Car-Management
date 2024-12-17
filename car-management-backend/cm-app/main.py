from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from databaseConfig import engine
from models import Base
from routers.garage_router import garage_router

def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    yield
app = FastAPI(lifespan=lifespan)
# added because of the cross origin access is blocked by third party client
origins = [ "http://192.168.56.1:3000",
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


app.include_router(garage_router,prefix="/garages", tags=["Garage API"])