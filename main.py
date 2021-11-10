from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from utils import load_image_from_request
from routes import users as users_router
from faceRecognition import recognize

from bson.json_util import dumps
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
    "application_name": "Face recognition API",
    "author": "Maxime MOREILLON",
    }


app.include_router(users_router.router, prefix="/users")

@app.post("/recognize")
async def predict(image: UploadFile = File (...)):
    img = await load_image_from_request(image)
    user = recognize(img)
    user_json = json.loads(dumps(user))
    return user_json
