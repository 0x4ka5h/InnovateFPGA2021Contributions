from flask_login import UserMixin
from flask import Blueprint, abort, jsonify, request, url_for
from .. import db
from sqlalchemy import text,select
from ..model import TestingValues,TypeTest


data = Blueprint('data',__name__)

################################     signup    ####################################
@data.route("/sendType"  , methods = ['POST'])
def sendType():
    type_ = request.json.get('type_')
    
    add= TypeTest(type_=type_)
    db.session.add(add)
    db.session.commit()
    return jsonify({'request':'successfull'})

@data.route("/requestType/")
def requestType():

    result=db.session.execute(text("SELECT * FROM type_test"))
    result = result.mappings().all()

    print(result)

    return ({'type':str(result[-1]['type_'])})




@data.route("/sendDetails"  , methods = ['POST'])
def sendDetails():
    type_ = request.json.get('type_')
    ph = request.json.get('ph')
    turbidity = request.json.get('turbidity')
    TDS = request.json.get('TDS')
    DO = request.json.get('DO')
    conductivity = request.json.get('conductivity')
    temp = request.json.get('temp')
    decision = request.json.get('decision')
    
    add= TestingValues(type_=type_,ph=ph,turbidity=turbidity,TDS=TDS,DO=DO,\
        conductivity=conductivity,temp=temp,decision=decision)

    db.session.add(add)
    db.session.commit()
    return jsonify({'request':'successfull'})


@data.route("/requestDetails/")
def requestDetails():
    
    result=db.session.execute(text("SELECT * FROM testing_values"))
    result = result.mappings().all()
    print(dict(result[-1]))
    return dict(result[-1])
    #jsonify(result[-1])





