from mongo import db
from bson.json_util import dumps, loads
from bson.objectid import ObjectId
import face_recognition
from utils import load_image_from_request

collection = db['users']

async def create_user(name, image):
    print('create_user')

    image_np = await load_image_from_request(image)
    face_encoding_np = face_recognition.face_encodings(image_np)[0]
    face_encoding = face_encoding_np.tolist()

    new_user_dict = {
    "name": name,
    "face_encoding": face_encoding
    }

    result = collection.insert_one(new_user_dict)
    user_id = str(result.inserted_id)

    return {
    "_id": user_id
    }

def read_users():
    print('read_users')
    users_cursor = collection.find()
    user_list = list(users_cursor)
    return user_list

def read_user(user_id):
    print('read_user')
    user = collection.find_one({"_id": ObjectId(user_id)})
    return user

def update_user(user_id):
    print('update_user')
    return 'Not implemented'


def delete_user(user_id):
    collection.delete_one({"_id": ObjectId(user_id)})
