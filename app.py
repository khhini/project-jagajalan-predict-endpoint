from flask import Flask, request
import numpy as np
import cv2
import re
import base64
from utilities import predict_image

app = Flask(__name__)

@app.route('/', methods=['POST'])
def hello_world():
    req = request.get_json()

    # Prepare Request Data
    im_b64 = re.sub(r'^data:\w+\/\w+;base64,', '', req['foto'])
    im_bytes = base64.b64decode(im_b64)
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
    img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
    cv2.imwrite("input.jpeg", img)

    # Predict Image

    res = predict_image("input.jpeg")

    # Prepare For response
    cv2.imwrite("output.jpeg", res)
    with open("output.jpeg", "rb") as f:
        res = base64.b64encode(f.read())

    # return im_b64
    return 'data:image/jpeg;base64,'+res.decode("utf-8")
