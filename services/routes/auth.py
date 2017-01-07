from flask_restful import reqparse
from flask_restful import Resource
from flask import  jsonify, abort, make_response, request, g
import MySQLdb
import collections
import logging
import hashlib, uuid
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Resource, Api
import flask_restful
import jwt
from jwt import DecodeError, ExpiredSignature
from datetime import datetime, timedelta
from functools import wraps
from flask import g


from flask_inputs import Inputs
from flask_inputs.validators import JsonSchema
from jsonschema import validate

users = Blueprint('users', __name__)

SECRET_KEY = "some random string"

#schema = UsersSchema()


# JWT AUTh process start
def create_token(user):
    payload = {
        'sub': user['id'],
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(days=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token.decode('unicode_escape')


def parse_token(req):
    token = req.headers.get('Authorization').split()[1]
    return jwt.decode(token, SECRET_KEY, algorithms='HS256')

# Login decorator function


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.headers.get('Authorization'):
            response = jsonify(message='Missing authorization header')
            response.status_code = 401
            return response

        try:
            payload = parse_token(request)
        except:
            response = jsonify(message='Token is invalid')
            response.status_code = 401
            return response
        # except ExpiredSignature:
        #     response = jsonify(message='Token has expired')
        #     response.status_code = 401
        #     return response

        g.user_id = payload['sub']

        return f(*args, **kwargs)

    return decorated_function


apk = Api(users)


class Auth(Resource):

    def post(self):
        data = request.get_json(force=True)
        print(data)
        #email = data['email']
        password = data['password']
        user = {"email":"purnesh.anugolu@gmail.com", "password":"pass", "id":12345}
        if user == None:
            response = make_response(
                jsonify({"message": "invalid username/password"}))
            response.status_code = 401
            return response
        if True:
            token = create_token(user)
            return {'token': token}
        else:
            response = make_response(
                jsonify({"message": "invalid username/password"}))
            response.status_code = 401
            return response

apk.add_resource(Auth, '/jwt/login')


# Adding the login decorator to the Resource class
class Resource(flask_restful.Resource):
    method_decorators = [login_required]


# Any API class now inheriting the Resource class will need Authentication
class User(Resource):

    def get(self):

        results = [1,2,3,4,5]
        #users = schema.dump(results, many=True).data
        return jsonify({"users": results})


apk.add_resource(User, '/jwt/users')


UserLoginSchema = {
    'type': 'object',
    'properties': {
        'userid': {'type': 'string'},
		'password': {'type': 'string'}
    },
	"required": ["password","userid"]
}


class UserLoginSchemaApiInputs(Inputs):
    json = [JsonSchema(schema=UserLoginSchema)]

class UserLogin(Resource):
    def post(self):
        logger = logging.getLogger("UserLogin post")
        logger.info('Entered into UserLogin method')

        inputs = UserLoginSchemaApiInputs(request)
        if not inputs.validate():
            return jsonify(success=False, errors=inputs.errors)

        try:
            user = request.json
            cursor = g.appdb.cursor()
            username = user["userid"]
            password = user["password"]
        except:
            logger.error("variables from url", exc_info=True)
        qury = """ SELECT password FROM user where user_id = %s """
        cursor.execute(qury,(username,))

        saltciphertext = cursor.fetchone()
        salt = saltciphertext["password"][0:32]
        cipher_db = saltciphertext["password"][32:]
        cipher_front = hashlib.sha256(password + salt).hexdigest()

        query = """ SELECT u.id, u.user_id as user_id, u.email, r.name as role, s.name as store_name, u.name as username, s.id as store_id
              FROM user u
              inner join user_roles ur on u.id = ur.user_id
              inner join role r on ur.role_id = r.id
              left outer join store s on s.id = ur.store_id
              where BINARY u.user_id = %s and BINARY u.password = %s """
        cursor.execute(query,(username, salt + cipher_front))
        rv = cursor.fetchall()

        if len(rv)>0:
            session["username"] = username

        return jsonify({"status":"success","response":rv})


class SessionVerify(Resource):
    def get(self):
        if "username" in session:
            return session["username"]
        return "Not logged in!"
