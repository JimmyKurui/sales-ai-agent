from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import api.config.settings
from api.routers import automations
from api.routers import api as api_router
from api.routers import api as api_router, automations, authentication as auth_router
from api.database.mongodb import connect_to_mongo, close_mongo_connection, check_db



app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(api_router.router)
app.include_router(automations.router)

@app.on_event("startup")
async def startup_db_client():
    connect_to_mongo()
    await check_db()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()


@app.get("/")
def read_root():
    return {"message": "Welcome to Gamma's gateway, an AI Sales Agent API hand developed by @JimmyKurui on Github. Gamma is an outbound task agent operating in the Sales Development Representative pipeline with the aim of speeding up prospecting and follow up to bring in qualified leads."}