from fastapi import APIRouter, HTTPException, File, Form, UploadFile
from fastapi.responses import JSONResponse

from bson.json_util import dumps
import json

from controllers import users as user_controller

router = APIRouter()


@router.get("/")
async def read_users():
    users = user_controller.read_users()
    # Not clean
    return json.loads(dumps(users))

@router.post("/")
async def create_user(image: UploadFile = File (...), name: str = Form(...)):
    result = await user_controller.create_user(name, image)
    return result

@router.get("/{user_id}")
async def read_user(user_id: str):
    user = user_controller.read_user(user_id)
    user_json = json.loads(dumps(user))
    return user_json

@router.delete("/{user_id}")
async def delete_user(user_id: str):
    user_controller.delete_user(user_id)
    return {"_id": user_id}

@router.patch("/{user_id}")
async def update_user(user_id: str):
    result = user_controller.update_user()
    return result
