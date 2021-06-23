from flask_mongoengine import MongoEngine
from config import db
import datetime


class User(db.Document):
    firstname = db.StringField(required=True)
    lastname = db.StringField()
    email = db.StringField(required=True)
    password = db.StringField(required=True)
    count = db.IntField(default=0)
    date = db.DateField(default=datetime.datetime.utcnow)
