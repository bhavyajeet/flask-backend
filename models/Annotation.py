from flask_mongoengine import MongoEngine
from config import db
import datetime


class Annotations(db.DynamicDocument):
    qid = db.StringField(required=True)
    sentenceOffset = db.IntField(required=True)
    sentence = db.StringField(required=True)
    facts = db.ListField(db.ListField())
    factIndex = db.ListField()
    email = db.StringField()
    covers = db.StringField()
    date = db.DateField(default=datetime.datetime.utcnow)

