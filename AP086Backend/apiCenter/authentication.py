from flask import Blueprint, abort, jsonify, request, url_for
from itsdangerous import json
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user
from .model import User

auth = Blueprint('auth',__name__)

################################     signup    ####################################
@auth.route("/signup/"  , methods = ['POST'])
def singUp():

    username = request.json.get('username')
    password = request.json.get('password')


    if User.query.filter_by(username=username).first() is not None:
        return jsonify({"Reason ":str(username)+" already found under same role"})

    user = User(username = username,password=generate_password_hash(password, method='sha256'))
    # add the new user to the database
    db.session.add(user)
    db.session.commit()
    return jsonify({ 'request': "success" ,"username" : username}), 201
    #return "User added successfully"

#################################   login   #####################################
@auth.route("/Login/"  , methods = ['POST'])
def logIn():
    print(request.data)
    username = request.json.get('username')
    password = request.json.get('password')


    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"request":"failed","Reason":"Double check role/username/password before submit"}),201
    else:
        login_user(user, remember=True)
        return jsonify({"request":"success"}),201

################################   logout   ######################################
@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    return jsonify({"request":"successfull"})


