from flask import Blueprint, jsonify
from . import db
from flask_login import login_required, current_user

main = Blueprint('main', __name__)



@main.route('/')
def home():
    try:
        data = jsonify({"login":current_user.username,"message":" testing under AP093"})
        data.headers.add("Access-Control-Allow-Origin", "*")
        return data
    except:
        #return jsonify({"login":"-----","message":" testing under AP061_78"})
        data = jsonify({"login":"-----","message":" testing under AP061_78"})
        data.headers.add("Access-Control-Allow-Origin", "*")
        return data
