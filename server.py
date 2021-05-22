import cv2
from flask import Flask, jsonify, request, render_template
from json import dumps
import numpy as np
from tensorflow import keras
import face_recognition
import os
port = int(os.environ.get("PORT", 5000))

app = Flask(__name__)
rating_model = keras.models.load_model("rating_model.h5")
classifier = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/getEncoding", methods=["POST"])
def Encode():
    image = request.files["image"].read()
    #filename = secure_filename(image.filename)

    img = cv2.imdecode(np.frombuffer(image, dtype=np.uint8), -1)
    # data_sample = data["encoding"]

    # detect MultiScale / faces
    faces = classifier.detectMultiScale(img)

    # get the first face only
    face = faces[0]

    (x, y, w, h) = face
    sub_face = img[y:y+h, x:x+w]

    encoding = face_recognition.face_encodings(sub_face)[0] # Rates only the first face in the image

    return jsonify({"encoding": encoding.tolist()})

@app.route("/rate", methods=["POST"])
def rate():

    image = request.files["image"].read()
    #filename = secure_filename(image.filename)

    img = cv2.imdecode(np.frombuffer(image, dtype=np.uint8), -1)
    # data_sample = data["encoding"]

    # detect MultiScale / faces
    faces = classifier.detectMultiScale(img)

    # get the first face only
    face = faces[0]

    (x, y, w, h) = face
    sub_face = img[y:y+h, x:x+w]

    # get face encoding and predict the rating
    try:
        face_encoding = face_recognition.face_encodings(sub_face)[0]

        x = np.asarray(face_encoding.tolist()).astype("float32").reshape((1, 128))
        x = x.tolist()

        prediction = rating_model.predict(x)

        return jsonify({"rating": str(prediction[0,0]*2)})
    except:
        return jsonify({"error": "Please upload a clearer picture"})
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
