from better_profanity import profanity
from flask import Flask, render_template, redirect, request, current_app
from replit import web, db
app = Flask(__name__)
users = web.UserStore()
@app.route('/')
def index():
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
        users.current["current"] = 0
        users.current["id"] = 0
        users.current["docs"] = []
        db["names"].append(web.auth.name)
    return render_template("home.html",name = web.auth.name,docs=users.current["docs"][0:])

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
        doc = users.current["docs"]
        for i in range(len(doc)):
            if str(doc[i]) == str(id):
                doc[i-6]=title
                doc[i-5]=font_size
                doc[i-4]=color
                doc[i-3]=text
                doc[i-2]=align
                doc[i-1]=bold
                doc[i]=id
                users.current["docs"] = doc
        return redirect("/write")
    else:
        if users.current["current"] != -1:
            doc = users.current["docs"]
            currentdoc = []
            j = -7
            for i in range(len(doc)):
                current = users.current["current"]
                if str(doc[i]) == str(current):
                    for k in range(7):
                        j = j + 1
                        currentdoc.append(doc[i+j])
                    break
            return render_template("write.html",name = web.auth.name, doc=currentdoc)
        else:
            return "Please open a doc"

@web.authenticated
@app.route('/new')
def new():
    if len(users.current["docs"])/7 < 10:
        db["docs"] = db["docs"] + 1
        users.current["current"] = users.current["id"]+1
        users.current["id"] = users.current["id"]+ 1
        users.current["docs"].append("New Document")
        users.current["docs"].append("13")
        users.current["docs"].append("#000000")
        users.current["docs"].append("")
        users.current["docs"].append("left")
        users.current["docs"].append("False")
        users.current["docs"].append(users.current["id"])
    else:
        return "You have used up your 10 documents delete some so you can make more"
    return redirect("/write")

@web.authenticated
@app.route('/open')
def open():
    id = request.args.get("id")
    users.current["current"] = int(id)
    return redirect("/write")

@web.authenticated
@app.route('/delete')
def delete():
    def delit(i):
        doc = users.current["docs"]
        doc.pop(i-6)
        doc.pop(i-6)
        doc.pop(i-6)
        doc.pop(i-6)
        doc.pop(i-6)
        doc.pop(i-6)
        doc.pop(i-6)
        users.current["docs"] = doc
        return
    id = request.args.get("id")
    if int(id) == users.current["current"]:
        users.current["current"] = -1
    try:
        int(id)
    except:
        return "Something Went Wrong"
    else:
        docs = users.current["docs"]
        i = 6
        if str(docs[i]) == str(id):
            delit(i)
            return redirect("/home")
        while i < len(docs):
            if str(docs[i]) == str(id):
                delit(i)
                break
            i=i+7
        return redirect("/home")

@app.route('/admin')
def admin():
    if web.auth.name == "GoodVessel92551":
        names = db["names"][0:]
        return render_template("admin.html",name = web.auth.name, names=names, docs=db["docs"])
    else:
        return redirect("/home")

app.run(host='0.0.0.0', port=81)