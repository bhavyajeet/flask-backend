from flask_mongoengine import MongoEngine
from config import db
import datetime


class Annotations(db.Document):
    qid = db.StringField(required=True)
    sentenceOffset = db.IntField(required=True)
    sentence = db.StringField(required=True)
    facts = db.ArrayField()
    factIndex = db.ArrayField()
    email = db.StringField()
    covers = db.StringField()
    date = db.DateField(default=datetime.datetime.utcnow)

