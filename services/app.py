#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request, g
from flask_restful import reqparse
from flask_restful import Resource, Api
import kaptan
import os
import MySQLdb
import logging
import json
import logging.config
import sys
from MySQLdb import cursors

from routes.auth import UserLogin
from routes.check import CardCheckReport
from routes.check import ItEquipmentReport

# from flask import Flask, render_template,request,jsonify
# import json
# import jsonschema
#
# app = Flask(__name__)
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

config = kaptan.Kaptan(handler="json")
config.import_config(os.getenv("CONFIG_FILE_PATH", 'config.json'))
environment = config.get('environment')

api = Api(app)
logger = logging.getLogger(__name__)


def connect_db():
    """Connects to the specific database."""
    try:
        db = MySQLdb.connect(host=config.get('dbhost'),  # your host, usually localhost
                         user=config.get("dbuser"),  # your username
                         passwd=config.get("dbpass"),  # your password
                         db=config.get("dbname"), cursorclass=MySQLdb.cursors.DictCursor,sql_mode="STRICT_TRANS_TABLES")  # name of the data base
        return db
    except:
        logger.error('Failed to Connect to the database', exc_info=True)
        sys.exit("not able to connect to database")


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'appdb'):
        g.appdb = connect_db()
    return g.appdb

@app.before_request
def before_request():
    g.appdb = get_db()
    setEmailRequirements()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'appdb'):
        g.appdb.close()

@app.before_first_request
def setup_logging(default_path='logconf.json', default_level=logging.INFO, env_key='LOG_CFG_PATH'):
    """Setup logging configuration"""
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

def setEmailRequirements():
    if not hasattr(g, 'config'):
        g.config = config

api.add_resource(UserLogin, '/api/auth/login', endpoint = 'auth')
api.add_resource(CardCheckReport, '/api/route/check/cardCheckReport', endpoint = 'cardCheckReport')
api.add_resource(ItEquipmentReport, '/api/route/check/itEquipmentReport', endpoint = 'itEquipmentReport')


@app.route('/api')
def index():
    # same result even with Flask-MySQL - We need to use the Index to Get
    # Values and Map to OrderedDict to create JSON.
    logger.info('Entered into Get /api Call')
    logger.debug(request.headers.get('User-Agent'))
    logger.info('Exiting from Get /api Call')
    return jsonify({"status": "success", "response": "API is up at the URL"})

#,ssl_context='adhoc'
if __name__ == '__main__':
    app.run(host=config.get("host"), debug=config.get("debug"))
#
# if __name__ == '__main__':
#     app.run(host='localhost', debug=True, port=5050)
