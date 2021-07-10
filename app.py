from flask import Flask, request, make_response
from flask_mongoengine import MongoEngine
from config import db
from config import app
import json
import sys
import bcrypt

sys.path.append("models")
from User import User
from Sentences import Sentences
from Annotation import Annotations


@app.route("/users", methods=["GET", "POST"])
def newuser():
    if request.method == "POST":
        print(request.json)
        dets = request.json
        print(dets)
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

        return ({"firstname": fname, "lastname": lname, "email": email}, 200)

    if request.method == "GET":
        for k in User.objects():
            print(k.firstname)
        print((User.objects()))
        return User.objects().to_json()


@app.route("/users/login", methods=["GET", "POST"])
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

    userlist = User.objects(email=email)
    if len(userlist) == 0:
        resp = make_response("email does not exist", 400)
        resp.set_cookie("logged", "False")
        return resp

    theuser = userlist[0]
    # compare bcrypt and set cookie
    print(theuser.email)
    # print(theuser.password)
    # print(password)
    ver = bcrypt.checkpw(password, theuser.password.encode("utf=8"))
    if not (ver):
        return ("incorrect password", 400)
    else:
        resp = make_response(theuser.to_json(), 200)
        resp.set_cookie("logged", "True")
        return resp

    return "return"


@app.route("/sentence", methods=["GET", "POST"])
def sentencefunc():
    dets = request.json
    seqno = dets["seqno"]
    sentlist = Sentences.objects(seqno=seqno)
    print(sentlist.to_json())
    sentence = sentlist[0]
    print(sentence.to_json())
    return sentlist.to_json()


@app.route("/annotation", methods=["GET", "POST"])
def annotatefunc():
    if request.method == "GET":
        return str(len(Annotations.objects()))

    if request.method == "POST":

        dets = request.json
        print(dets)
        newAnnotation = Annotations(
            email=dets["email"],
            sentence=dets["sentence"],
            sentenceOffset=dets["sentenceOffset"],
            qid=dets["qid"],
            facts=dets["facts"],
            factIndex=dets["factIndex"],
            covers=dets["covers"],
        )

        newAnnotation.save()

        return (newAnnotation.to_json(), 200)


if __name__ == "__main__":
    app.run(debug=True)

