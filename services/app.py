#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request, g

from flask_restful import reqparse
from flask_restful import Resource, Api

import kaptan
import os

from routes.auth import UserLogin
from routes.auth import AddUser

import MySQLdb
import logging
import json
import logging.config
import sys

app = Flask(__name__)

config = kaptan.Kaptan(handler="json")
config.import_config(os.getenv("CONFIG_FILE_PATH", 'config.json'))
environment = config.get('environment')

api = Api(app)
logger = logging.getLogger(__name__)


def connect1_db():
    """Connects to the specific database."""
    try:
        db = MySQLdb.connect(host=config.get('dbhost_1'),  # your host, usually localhost
                         user=config.get("dbuser_1"),  # your username
                         passwd=config.get("dbpass_1"),  # your password
                         db=config.get("dbname_1"), cursorclass=MySQLdb.cursors.DictCursor,sql_mode="STRICT_TRANS_TABLES")  # name of the data base
        return db
    except:
        logger.error('Failed to Connect to the database', exc_info=True)
        sys.exit("not able to connect to database")


def get1_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'appdb'):
        g.appdb = connect1_db()
    return g.appdb

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'appdb'):
        g.appdb.close()

def connect2_db():
    """Connects to the specific database."""
    try:
        db = MySQLdb.connect(host=config.get('dbhost_2'),  # your host, usually localhost
                         user=config.get("dbuser_2"),  # your username
                         passwd=config.get("dbpass_2"),  # your password
                         db=config.get("dbname_2"), cursorclass=MySQLdb.cursors.DictCursor,sql_mode="STRICT_TRANS_TABLES")  # name of the data base
        return db
    except:
        logger.error('Failed to Connect to the database', exc_info=True)
        sys.exit("not able to connect to database")


def get2_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(p, 'appdb'):
        p.appdb = connect2_db()
    return p.appdb

@app.teardown_request
def teardown_request(exception):
    if hasattr(p, 'appdb'):
        p.appdb.close()

def connect3_db():
    """Connects to the specific database."""
    try:
        db = MySQLdb.connect(host=config.get('dbhost_3'),  # your host, usually localhost
                         user=config.get("dbuser_3"),  # your username
                         passwd=config.get("dbpass_3"),  # your password
                         db=config.get("dbname_3"), cursorclass=MySQLdb.cursors.DictCursor,sql_mode="STRICT_TRANS_TABLES")  # name of the data base
        return db
    except:
        logger.error('Failed to Connect to the database', exc_info=True)
        sys.exit("not able to connect to database")


def get3_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(v, 'appdb'):
        v.appdb = connect_db()
    return v.appdb

@app.teardown_request
def teardown_request(exception):
    if hasattr(v, 'appdb'):
        v.appdb.close()

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

api.add_resource(UserLogin, '/api/auth/login', endpoint='auth')
api.add_resource(AddUser, '/api/auth/addUser', endpoint='adduser')


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
