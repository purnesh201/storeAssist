from flask_restful import reqparse
from flask_restful import Resource
from flask import  jsonify, abort, make_response, request, g
import MySQLdb
import collections
import logging
import hashlib, uuid

from flask_inputs import Inputs
from flask_inputs.validators import JsonSchema
from jsonschema import validate
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
