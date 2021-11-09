import face_recognition
import json

known_image = face_recognition.load_image_file("images/biden1.jpg")
known_image_encoding = face_recognition.face_encodings(known_image)[0]

lists = known_image_encoding.tolist()
json_str = json.dumps(lists)

print(json_str)
