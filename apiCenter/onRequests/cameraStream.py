import base64
from fileinput import filename
import cv2,numpy as np
from sqlalchemy import text
from flask_login import login_required
from flask import Blueprint, jsonify, redirect, request, url_for
from .. import db

cameraStreamauth = Blueprint("cameraStreamauth",__name__,static_url_path='apiCenter/static/')

@cameraStreamauth.route("/api/stream/request/")
def cameraStreamByOwner():

    return url_for("static",filename="test.jpg")
    '''_,encoded = cv2.imencode('.png',image)
    base_encoded = base64.b64encode(encoded)
    baseEncode = base_encoded[1:]
    return "data:image/png;base64,"+str(baseEncode)'''


@cameraStreamauth.route("/api/stream/send/",methods=['POST'])
def cameraStreamFromVehicle():

    imageData = request.json.get('imageData')
    dec = base64.b64decode(imageData)
    nparr = np.fromstring(dec, np.uint8)
    image_ = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cv2.imwrite("apiCenter/static/test.jpg",image_)
    return jsonify({"request":"successfull"}),201