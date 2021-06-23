from flask_mongoengine import MongoEngine
from config import db
import datetime


class Sentences(db.Document):
    qid = db.StringField(required=True)
    sentence_offset = db.IntField(required=True)
    sentence_count = db.IntField(required=True)
    annotation_count = db.IntField(required=True)
    facts = db.ArrayField(required=True)
    sentence = db.StringField(required=True)
    seqno = db.IntField(required=True)

