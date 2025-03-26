from fastapi import FastAPI
from app.api.routes.endpoint import model_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(router=model_router)
