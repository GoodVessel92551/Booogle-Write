from better_profanity import profanity
from flask import Flask, render_template, redirect, request, current_app
from replit import web, db

app = Flask(__name__)
users = web.UserStore()

@app.route('/')
def index():
    db["names"] = []
    if web.auth.name != "":
        return redirect("/home")
    else:
        return render_template("index.html")
    return render_template("index.html")

@app.route('/sw.js', methods=['GET'])
def sw():
    return current_app.send_static_file('sw.js')

@web.authenticated
@app.route('/home')
def home():
    if web.auth.name not in db["names"]:
        db["names"].append(web.auth.name)
    return render_template("home.html",name = web.auth.name)

@web.authenticated
@app.route('/write')
def write():
    return render_template("write.html",name = web.auth.name)

app.run(host='0.0.0.0', port=81,debug=True)