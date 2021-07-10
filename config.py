from flask_mongoengine import MongoEngine
from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)


app.config["MONGODB_SETTINGS"] = {
    "db": "factify",
    "host": "localhost",
    "port": 27017,
}
db = MongoEngine()
db.init_app(app)

cors = CORS(app)
# cors = CORS(app, resources={r"/*": {"origins":"*"}})
app.config["CORS_HEADERS"] = "Content-Type"
