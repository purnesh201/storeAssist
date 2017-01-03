from flask import Flask,url_for, render_template,redirect,request,jsonify,session,g
import json
import jsonschema
import MySQLdb
import os

auth = Flask(__name__)
auth.secret_key = os.urandom(24)

@auth.route('/' , methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        session.pop('user' , None)

        if  request.form['password'] == 'password':

    #return "hi"
            session['user'] =  request.form['username']
            return redirect(url_for('protected'))

    return render_template('index.html')

@auth.route('/protected')
def protected():
    if g.user :
       return render_template('response.html')

    return render_template('index.html')


@auth.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']


@auth.route('/getsession')
def getsession():
    if 'user' in session:
        return session['user']
    return 'Not logged in !'

@auth.route('/dropsession')
def dropsession():
    session.pop('user' , None)
    return 'Dropped!'


# @auth.route("/snd",methods=['POST'])
# def snd():
#     name=str(request.form['uname'])
#     password=str(request.form['pwd'])
#     age=str(request.form['age'])
#     fname=str(request.form['fname'])
#     print fname,age


#     db = MySQLdb.connect( host="localhost",user="root",passwd="root",db="store" )
#     cur = db.cursor()

#     query="""INSERT into user(uname,age)values(%s,%s)"""
#     cur.execute(query,(fname,age))
#     print "Record successfully added"
#     db.commit()
#     cur.close()
#     db.close()
#     if name=="chetna" and password=="123" :

#             lst=[10,20,40,60,80]
#             return render_template('response.html', fname=fname , age=age , nums=lst)
#     else :
#      return "Login Unsuccessful!! Try correct username and password"
# class UserLoginSchemaApiInputs(Inputs):
#     json = [JsonSchema(schema=UserLoginSchema)]

# class UserLogin(Resource):
#     def post(self):
#         logger = logging.getLogger("UserLogin post")
#         logger.info('Entered into UserLogin method')

#         inputs = UserLoginSchemaApiInputs(request)
#         if not inputs.validate():
#             return jsonify(success=False, errors=inputs.errors)

#         try:
#             user = request.json
#             cursor = g.appdb.cursor()
#             username = user["userid"]
#             password = user["password"]
#         except:
#             logger.error("variables from url", exc_info=True)
#         qury = """ SELECT password FROM user where user_id = %s """
#         cursor.execute(qury,(username,))

#         saltciphertext = cursor.fetchone()
#         salt = saltciphertext["password"][0:32]
#         cipher_db = saltciphertext["password"][32:]
#         cipher_front = hashlib.sha256(password + salt).hexdigest()

#         query = """ SELECT u.id, u.user_id as user_id, u.email, r.name as role, s.name as store_name, u.name as username, s.id as store_id
#               FROM user u
#               inner join user_roles ur on u.id = ur.user_id
#               inner join role r on ur.role_id = r.id
#               left outer join store s on s.id = ur.store_id
#               where BINARY u.user_id = %s and BINARY u.password = %s """
#         cursor.execute(query,(username, salt + cipher_front))
#         rv = cursor.fetchall()

#         return jsonify({"status":"success","response":rv})


if __name__ == '__main__':
    auth.run(host='localhost', debug=True, port=5050)
