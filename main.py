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
            print(id)
            if str(doc[i]) == str(id):
                print("Hello")
                doc[i-6]=title
                doc[i-5]=font_size
                doc[i-4]=color
                doc[i-3]=text
                doc[i-2]=align
                doc[i-1]=bold
                doc[i]=id
                print(doc)
                users.current["docs"] = doc
                print(doc)
        return redirect("/write")
    else:
        doc = users.current["docs"]
        print(users.current["current"])
        currentdoc = []
        j = -7
        for i in range(len(doc)):
            if str(doc[i]) == str(users.current["current"]):
                print("hi")
                for k in range(7):
                    j = j + 1
                    currentdoc.append(doc[i+j])
                break
        print(currentdoc)
        print(users.current["docs"])
        return render_template("write.html",name = web.auth.name, doc=currentdoc)

@web.authenticated
@app.route('/new')
def new():
    #['Document', '13', '#000000', 'This is a test', 'right', 'False',1]
    users.current["current"] = users.current["id"]+1
    users.current["id"] = users.current["id"]+ 1
    users.current["docs"].append("New Document")
    users.current["docs"].append("13")
    users.current["docs"].append("#000000")
    users.current["docs"].append("")
    users.current["docs"].append("left")
    users.current["docs"].append("False")
    users.current["docs"].append(users.current["id"])
    print(users.current["docs"])
    return redirect("/write")

@web.authenticated
@app.route('/open')
def open():
    id = request.args.get("id")
    users.current["current"] = id
    return redirect("/write")

@web.authenticated
@app.route('/delete')
def delete():
    def delit(id):
        users.current["docs"].pop(i-6)
        users.current["docs"].pop(i-6)
        users.current["docs"].pop(i-6)
        users.current["docs"].pop(i-6)
        users.current["docs"].pop(i-6)
        users.current["docs"].pop(i-6)
        users.current["docs"].pop(i-6)
        return
    id = request.args.get("id")
    try:
        int(id)
    except:
        return "Something Went Wrong"
    else:
        docs = users.current["docs"]
        i = 6
        print(docs[i])
        if str(docs[i]) == str(id):
            delit(id)
            return redirect("/home")
        while i < len(docs):
            if str(docs[i]) == str(id):
                delit(id)
                break
            i=i+7
        return redirect("/home")

app.run(host='0.0.0.0', port=81,debug=True)