from fastapi import FastAPI, File, UploadFile,Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from utils import convert_image
from faceRecognition import recognize
from mongo import mongodb_url, mongodb_db
from bson.json_util import dumps
import json
import dlib
from controllers import users as user_controller
from authMiddleware import AuthMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

version = '0.1.7'

print(f'= Face recognition FastAPI v{version} =')

app = FastAPI()

authentication_url = os.getenv('AUTHENTICATION_URL')
if authentication_url:
    print(f'Using ${authentication_url} for authentication')
    app.add_middleware(
        AuthMiddleware,
        options={"url": authentication_url}
    )

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
    "cuda": {"used": dlib.DLIB_USE_CUDA, "num_devices": dlib.cuda.get_num_devices()},
    "auth" : authentication_url,
    }


@app.post("/recognize")
async def predict(image: UploadFile = File (...)):

    img_data = await image.read()
    img = convert_image(img_data)

    user = recognize(img)

    print(f'[FR] Recognized face of user {user["name"]}')

    user_json = json.loads(dumps(user))
    return user_json

@app.get("/users")
async def read_users():
    users = user_controller.read_users()
    # Not clean
    return json.loads(dumps(users))

@app.post("/users")
async def create_user(image: UploadFile = File (...), name: str = Form(...)):
    result = await user_controller.create_user(name, image)
    return result

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    user = user_controller.read_user(user_id)
    # Not clean
    return json.loads(dumps(user))

@app.delete("/users/{user_id}")
async def delete_user(user_id: str):
    result = user_controller.delete_user(user_id)
    return result

@app.patch("/users/{user_id}")
async def update_user(user_id: str):
    result = user_controller.update_user()
    return result

@app.get("/users/{user_id}/image")
async def read_user(user_id: str):
    image_path = user_controller.read_user_image(user_id)
    return FileResponse(image_path)
