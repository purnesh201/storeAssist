#!flask/bin/python
# <<<<<<< HEAD
from flask import Flask, jsonify, abort, make_response, request, g , session , render_template , redirect , url_for, flash
# =======
# from flask import Flask, jsonify, abort, make_response, request, g, render_template
# >>>>>>> b645304e2a3e34c546406fcd8fb7015388ccaebb
from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from sqlalchemy.orm import sessionmaker
from tabledef import *

# <<<<<<< HEAD
# from routes.auth import  Loginn
# # =======

# from routes.auth import UserLogin
# from routes.check import CardCheckReport
# from routes.check import ItEquipmentReport
# from routes.accountAPI import account_api



# from flask import Flask, render_template,request,jsonify
# import json
# import jsonschema
#

# app.register_blueprint(account_api)
#
#
# @app.route("/")
# def main():
#    #return "Welcome!"
#
#     return render_template('index.html')
#
#
# @app.route("/snd",methods=['POST'])
# def snd():
#     name=str(request.form['uname'])
#     password=str(request.form['pwd'])
#     fname=str(request.form['fname'])
#     age=str(request.form['age'])
#     if name=="chetna" and password=="123" :
#
#             return render_template('response.html', fname=fname ,age=age)
#     else :
#      return "Login Unsuccessful!! Try correct username and password"

# >>>>>>> b645304e2a3e34c546406fcd8fb7015388ccaebb

# config = kaptan.Kaptan(handler="json")
# config.import_config(os.getenv("CONFIG_FILE_PATH", 'config.json'))
# environment = config.get('environment')

# api = Api(app)
# logger = logging.getLogger(__name__)
app = Flask(__name__)

app.secret_key = os.urandom(24)
'\x8f2\xb0\xa6D\xb0ID;y\xb1\xd9V\x19\xab\xa0\xd6c\\r\x01\x12\x08D'

engine = create_engine('sqlite:///login.db', echo=True)




@app.route('/')
def  main():
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        return "Hello Boss!  <a href='/logout'>Logout</a>"



@app.route('/login', methods=["POST"])
def login():


    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
 
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()

    if result:
        session['logged_in'] = True
        return render_template('response.html')
    else:
        flash('wrong password!')
    return main()

@app.route('/logout', methods=["POST"])
def logout():
    session['logged_in'] = False
    return  render_template('index.html')




# <<<<<<< HEAD
# @app.before_first_request
# def setup_logging(default_path='logconf.json', default_level=logging.INFO, env_key='LOG_CFG_PATH'):
#     """Setup logging configuration"""
#     path = default_path
#     value = os.getenv(env_key, None)
#     if value:
#         path = value
#     if os.path.exists(path):
#         with open(path, 'rt') as f:
#             config = json.load(f)
#         logging.config.dictConfig(config)
#     else:
#         logging.basicConfig(level=default_level)

# def setEmailRequirements():
#     if not hasattr(g, 'config'):
#         g.config = config

# api.add_resource(Loginn, '/api/auth/login', endpoint = 'auth')
# =======
# @app.before_first_request
# def setup_logging(default_path='logconf.json', default_level=logging.INFO, env_key='LOG_CFG_PATH'):
#     """Setup logging configuration"""
#     path = default_path
#     value = os.getenv(env_key, None)
#     if value:
#         path = value
#     if os.path.exists(path):
#         with open(path, 'rt') as f:
#             config = json.load(f)
#         logging.config.dictConfig(config)
#     else:
#         logging.basicConfig(level=default_level)

# def setEmailRequirements():
#     if not hasattr(g, 'config'):
#         g.config = config

# api.add_resource(UserLogin, '/api/auth/login', endpoint = 'UserLogin')
# api.add_resource(Deco, '/api/auth/deco', endpoint = 'Deco')
# >>>>>>> b645304e2a3e34c546406fcd8fb7015388ccaebb
# api.add_resource(CardCheckReport, '/api/route/check/cardCheckReport', endpoint = 'cardCheckReport')
# api.add_resource(ItEquipmentReport, '/api/route/check/itEquipmentReport', endpoint = 'itEquipmentReport')


# <<<<<<< HEAD
# # @app.route('/api')
# # def index():
# #     # same result even with Flask-MySQL - We need to use the Index to Get
# #     # Values and Map to OrderedDict to create JSON.
# #     logger.info('Entered into Get /api Call')
# #     logger.debug(request.headers.get('User-Agent'))
# #     logger.info('Exiting from Get /api Call')
# #     return jsonify({"status": "success", "response": "API is up at the URL"})
# =======
# @app.route('/api')
# def index():
#     # same result even with Flask-MySQL - We need to use the Index to Get
#     # Values and Map to OrderedDict to create JSON.
#     logger.info('Entered into Get /api Call')
#     logger.debug(request.headers.get('User-Agent'))
#     logger.info('Exiting from Get /api Call')
#     return jsonify({"status": "success", "response": "API is up at the URL"})
# >>>>>>> b645304e2a3e34c546406fcd8fb7015388ccaebb

#,ssl_context='adhoc'
if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 8009, debug = True)
#
# if __name__ == '__main__':
#     app.run(host='localhost', debug=True, port=5050)