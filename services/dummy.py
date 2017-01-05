import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *
 
engine = create_engine('sqlite:///login.db', echo=True)
 
# create a Session
Session = sessionmaker(bind=engine)
session = Session()
 
user = User("admin","12")
session.add(user)
 
user = User("chetna","singh")
session.add(user)
 
user = User("madan","mohan")
session.add(user)
 
# commit the record the database
session.commit()
 
session.commit()