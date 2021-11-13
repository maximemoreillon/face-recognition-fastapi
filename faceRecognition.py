import face_recognition
import json
from controllers.users import read_users
from fastapi import HTTPException

def recognize(img):

    # Get users
    users = read_users()

    # Get the encodings of the users
    # TODO: check if user has face encoding
    known_encodings = list(map((lambda x: x["face_encoding"]), users))

    try:
        face_encoding = face_recognition.face_encodings(img)[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid image")

    results = face_recognition.compare_faces(known_encodings, face_encoding)

    try:
        found_index = results.index(True)
    except Exception as e:
        raise HTTPException(status_code=404, detail="No match found")

    found_user = users[found_index]

    return found_user
