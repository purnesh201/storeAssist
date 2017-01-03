from flask import Blueprint, render_template

#the following Blueprint is inteded to create a constructor
account_api = Blueprint('account_api', __name__)

@account_api.route("/account")
def accountList():
    return render_template('/index.html')

@account_api.route("/madan")
def maddy():
    return render_template('/mad.html')

@account_api.route("/ren")
def rend():
    return 'hi how are you'
