from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2
import face_recognition
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load users from file
# In the future, replace by DB
with open('./users.json') as f:
  users = json.load(f)

@app.get("/")
async def root():
    return {
    "application_name": "Face recognition API",
    "author": "Maxime MOREILLON",
    }


@app.post("/find_match")
async def predict(image: UploadFile = File (...)):

    # This looks like an OK way to load images
    img_data = await image.read()
    nparr = np.frombuffer(img_data, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    imageRGB = cv2.cvtColor(img_np , cv2.COLOR_BGR2RGB)

    # Import face encodings from DB
    known_encodings = list(map((lambda x: x["encoding"]), users))

    try:
        unknown_image_encoding = face_recognition.face_encodings(imageRGB)[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid image")

    results = face_recognition.compare_faces(known_encodings, unknown_image_encoding)

    try:
        found_index = results.index(True)
    except Exception as e:
        raise HTTPException(status_code=404, detail="No match found")


    found_user = users[found_index]

    print(f'Found user: {found_user["name"]}')

    return {
    'name': found_user["name"]
    }
