from crypt import methods
from flask import Blueprint, jsonify, request
from flask_login import login_required
from ..model import vehicleDetails
from sqlalchemy import text,select
from .. import db

import json
ownerGPSauth = Blueprint("ownerGPSauth",__name__)

######################    current gps location      ####################################

@ownerGPSauth.route("/api/gpsLocationCurrent/")

def gpsLocationCurrent():

    result=db.session.execute(text("SELECT * FROM vehicle_details"))
    result = result.mappings().all()
    
    try:
        return jsonify({"gpsLocation":str(result[-1]['gpsPointCurr_'])}),201   #last gps point that vehicle left
    except:
        return "No Data found",200

@ownerGPSauth.route("/api/vehicle/sendVehicleDetails/" , methods = ['POST'])
#@login_required

def sendVehicleDetails():
    gpsPointCurr_ = request.json.get('gpsPoint')

    details_ = vehicleDetails(gpsPointCurr_=gpsPointCurr_)

    db.session.add(details_)
    db.session.commit()   # add the details to the database
        
    return jsonify({'request': "Success"}), 201



@ownerGPSauth.route("/api/sendRFSDetails/",methods=['POST'])
def sendRFSDetails():
    data = request.json
    
#    data = request.json.get('rfsData')
    f = open('apiCenter/ownerSide/RFSdata.txt','w+')
    json_object = json.dumps(data, indent = 4)
    f.write(json_object)
    f.close()
    return "Ok",200



@ownerGPSauth.route("/api/requestRFSDetails/")
def requestRFSDetails():
    f = open('apiCenter/ownerSide/RFSdata.txt','r+')
    data = json.load(f)
    f.close()
    #data = json.dump(data)
    data = jsonify(data)
    #print(type(data))
    
    data.headers.add("Access-Control-Allow-Origin", "*")
    return data

