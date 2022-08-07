from better_profanity import profanity
from flask import Flask, render_template, redirect, request, current_app
from replit import web, db

app = Flask(__name__)
users = web.UserStore()
doc = ['Document', '13', '#000000', 'This is a test', 'right', 'False']
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
@app.route('/write',methods=['POST','GET'])
def write():
    if request.method == "POST":
        title = request.form["title"]
        font_size = request.form["size"]
        color = request.form["color"]
        text = request.form["text"]
        id = request.args.get("id")
        align = request.args.get("align")
        bold = request.args.get("bold")
        print(align)
        doc[4] = align
        doc[5] = bold
        doc[0] = title
        doc[1] = font_size
        doc[2] = color
        doc[3] = text
        print(doc)
    return render_template("write.html",name = web.auth.name, doc=doc)




app.run(host='0.0.0.0', port=81,debug=True)