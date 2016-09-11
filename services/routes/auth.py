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

AddUserSchema = {
    'type': 'object',
    'properties': {
        'user_id': {'type': 'string'},
        'name': {'type': 'string'},
        'email': {'type': 'string'},
        'initials': {'type':'string'},
        'password': {'type': 'string'},
        'role_id': {'type': 'integer'},
        'store_id': {'type': 'integer'},
    },
    "required": ["user_id","name","email","initials","password","role_id","store_id"]
}

class UserLoginSchemaApiInputs(Inputs):
    json = [JsonSchema(schema=UserLoginSchema)]

class UserLogin(Resource):
    def post(self):
        logger=logging.getLogger('/UserLogin')

        inputs = UserLoginSchemaApiInputs(request)
        if not inputs.validate():
            return jsonify(success=False, errors=inputs.errors)

        try:
            user=request.json
            cursor = g.appdb.cursor()
            username=user["userid"]
            password=user["password"]
        except:
            logger.error("variables from url", exc_info=True)
        qury=""" SELECT password FROM 7eleven.user where user_id=%s; """
        cursor.execute(qury,(username,))

        saltciphertext = cursor.fetchone()
        salt=saltciphertext["password"][0:32]
        cipher_db=saltciphertext["password"][32:]
        cipher_front = hashlib.sha256(password + salt).hexdigest()

        query=""" SELECT u.id,u.user_id as userid,u.email,r.name as role,s.name as store_name,
        s.location as storeloc,u.name as username,s.id as storeid
        FROM user u inner join user_role ur on
        u.id=ur.user_id inner join role r on ur.role_id=r.id left outer join
        store s on s.id=ur.store_id where  BINARY u.user_id=%s and BINARY u.password = %s """
        cursor.execute(query,(username, salt +cipher_front))
        rv = cursor.fetchall()
        store_id = rv[0]["storeid"]
        query2 = """ SELECT profile_name, IFNULL(level_id,0) as level_id FROM store_profiles sp
        inner join  profiles p on p.id = sp.profile_id
        where store_id= %s """
        cursor.execute(query2,(store_id, ))
        profile_names = cursor.fetchall()

        rv[0]["lockTime"]  = g.config.get("lockTime")
        for word in profile_names:
            if word["profile_name"] =="Roller Grills":
                rv[0]["rollerGrills"] = True
                rv[0]["level_id"] = word["level_id"]
            elif word["profile_name"] =="Capital City":
                rv[0]["capitalCity"] = True
            elif word["profile_name"] == "Perishable Goods":
                rv[0]["perishableGoods"] = True

        if "capitalCity" not in rv[0].keys():
            rv[0]["capitalCity"] = False
        if "rollerGrills" not in  rv[0].keys():
            rv[0]["rollerGrills"] = False
        if "perishableGoods" not in rv[0].keys():
            rv[0]["perishableGoods"]  = False
        if "level_id" not in rv[0].keys():
            rv[0]["level_id"] = 0
        return jsonify({"status":"success","response":rv})

class AddUserSchemaApiInputs(Inputs):
    json = [JsonSchema(schema=AddUserSchema)]

class AddUser(Resource):

    def post(self):
        logger = logging.getLogger("Add_user")
        logger.info('Entered into Add_user  post method')
        try:
            value = request.json
            user_id = value["user_id"]
            name = value["name"]
            email = value["email"]
            password = value["password"]
            initials = value["initials"]
            role_id = value["role_id"]
            store_id = value["store_id"]

            salt=uuid.uuid4().hex
            cipher=hashlib.sha256(password+salt).hexdigest()
            pass_db=salt+cipher
            cursor = g.appdb.cursor()

        except:
            logger.error("DB connection or url parameters error", exc_info=True)
        query = """ INSERT INTO `user` (user_id,name,email,password,initials)VALUES(%s,%s,%s,%s,%s); """
        query_2 = """ INSERT INTO `user_role` (user_id,role_id,store_id)VALUES(%s,%s,%s); """
        cursor.execute(query,(user_id,name,email,pass_db,initials))
        g.appdb.commit()
        newID = cursor.lastrowid
        cursor.execute(query_2,(newID,role_id,store_id))
        g.appdb.commit()
        logger.info('Exited from Add_User post method')
        return jsonify({"status":"success", "response":"New user created successfully"})

    def put(self):
        logger = logging.getLogger("change password of the user")
        logger.info('Entered into Add_User put method')
        try:
            changePassword = request.json
            user_id = changePassword["user_id"]
            newpass = changePassword["newpass"]
            email=changePassword["email"]

            salt = uuid.uuid4().hex
            cipher = hashlib.sha256(newpass + salt).hexdigest()
            pass_db=salt+cipher
            cursor = g.appdb.cursor()

        except:
            logger.error('DB connection error', exc_info=True)

        query="""SELECT id from user where user_id=%s and email=%s;"""
        cursor.execute(query,(user_id,email))
        g.appdb.commit()
        ids=cursor.fetchone()
        update=""" update user set password=%s where id= %s; """
        cursor.execute(update,(pass_db,ids['id']))
        g.appdb.commit()
        logger.info('Exited from changing password put method')
        return jsonify({"status":"done", "response":"successfully changed your password"})

    def get(self):
        logger = logging.getLogger("UserRole get")
        logger.info('Entered into UserRole get method')
        try:
            cursor = g.appdb.cursor()
            store_id = request.values.get("store_id")

        except:
            logger.error('DB Connection error', exc_info=True)
        query = """ SELECT r.id, r.name from role r where r.name not in ('Admin', 'DBQ_Admin')
        and r.id not in (select ur.role_id from user_role ur where ur.store_id = %s) """
        cursor.execute(query, (store_id,))
        rv = cursor.fetchall()
        logger.info('Exited from UserRole get method')
        return jsonify({"status":"success", "response":rv})
