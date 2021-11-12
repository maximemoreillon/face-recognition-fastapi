from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from utils import convert_image
from routes import users as users_router
from faceRecognition import recognize
from mongo import mongodb_url, mongodb_db
from bson.json_util import dumps
import json
import dlib

version = '0.1.6'

print(f'= Face recognition FastAPI v{version} =')

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
    "version": version,
    "mongodb": {"url": mongodb_url, "db": mongodb_db},
    "cuda": {"used": dlib.DLIB_USE_CUDA, "num_devices": dlib.cuda.get_num_devices()}
    }


app.include_router(users_router.router, prefix="/users")

@app.post("/recognize")
async def predict(image: UploadFile = File (...)):

    img_data = await image.read()
    img = convert_image(img_data)

    user = recognize(img)

    print(f'[FR] Recognized face of user {user["name"]}')

    user_json = json.loads(dumps(user))
    return user_json
