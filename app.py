from flask import Flask, request, make_response
from flask_mongoengine import MongoEngine
from config import db
from config import app
import json
import sys
import bcrypt

sys.path.append("models")
from User import User


@app.route("/", methods=["GET", "POST"])
def newuser():
    if request.method == "POST":
        dets = request.json
        try:
            fname = dets["firstname"]
        except:
            print("fname error")
            return ("first name not given", 400)
        try:
            lname = dets["lastname"]
        except:
            print("lname not found")
            lname = ""
        try:
            email = dets["email"]
        except:
            print("mail error")
            return ("email not given", 400)
        try:
            password = bcrypt.hashpw(dets["password"].encode("utf=8"), bcrypt.gensalt())
            print(password)
        except:
            print("password error")
            return ("password not given", 400)

        finding = User.objects(email=email)
        if len(finding) != 0:
            return ("email exists", 400)
        newUser = User(firstname=fname, lastname=lname, email=email, password=password)
        newUser.save()

        return ({"firstname": fname, "lastname": lname, "email": email}, 500)

    if request.method == "GET":
        for k in User.objects():
            print(k.firstname)
        print((User.objects()))
        return User.objects().to_json()


@app.route("/login", methods=["GET", "POST"])
def userlogin():
    dets = request.json

    try:
        email = dets["email"]
    except:
        print("mail error")
        return ("email not given", 400)
    try:
        password = dets["password"].encode("utf=8")
    except:
        print("password error")
        return ("password not given", 400)

    theuser = User.objects(email=email)
    if len(theuser) == 0:
        resp = make_response("email does not exist", 400)
        resp.set_cookie("logged", False)
        return resp

    # compare bcrypt and set cookie


if __name__ == "__main__":
    app.run(debug=True)
