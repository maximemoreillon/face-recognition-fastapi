from mongo import db
from bson.json_util import dumps, loads
from bson.objectid import ObjectId
import face_recognition
from utils import convert_image
from os import path

import cv2
import numpy as np

collection = db['users']

async def create_user(name, image):


    img_data = await image.read()
    imageRGB = convert_image(img_data)

    # Generate face encoding
    face_encoding_np = face_recognition.face_encodings(imageRGB)[0]
    face_encoding = face_encoding_np.tolist()

    # Save image
    file_location = f"uploads/{image.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(img_data)

    # MongoDB data
    new_user_dict = {
    "name": name,
    "face_encoding": face_encoding,
    "image": image.filename,
    }

    result = collection.insert_one(new_user_dict)
    user_id = str(result.inserted_id)

    print(f'[DB] User {user_id} created')

    return {
    "_id": user_id
    }

def read_users():
    print('[DB] Reading all users')
    users_cursor = collection.find()
    user_list = list(users_cursor)
    return user_list

def read_user(user_id):
    print(f'[DB] Reading user {user_id}')
    user = collection.find_one({"_id": ObjectId(user_id)})
    return user

def read_user_image(user_id):
    print(f'[DB] Reading image of user {user_id}')
    user = read_user(user_id)
    image = user["image"]
    image_path = path.join('uploads',image)
    return image_path

def update_user(user_id):
    print('[DB] update_user')
    return 'Not implemented'


def delete_user(user_id):
    collection.delete_one({"_id": ObjectId(user_id)})
    return {"_id": user_id}
