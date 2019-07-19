from flask import Flask,redirect,url_for,render_template,request,session
import os
import sqlite3
app = Flask(__name__)
app.secret_key=os.urandom(142)
sql = sqlite3.connect("database_1.db")
sql.execute("CREATE TABLE IF NOT EXISTS login(name TEXT,password TEXT)")

menu1= sqlite3.connect("menubase.db")
menu1.execute("CREATE TABLE IF NOT EXISTS items(title TEXT,desc TEXT)")



@app.route("/signup",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        sql = sqlite3.connect("database_1.db")
        sql.execute("INSERT INTO login(name,password)VALUES(?,?)",(request.form["name"],request.form["newpassword"]))
        sql.commit()
        #sql.close()
        #database.update({request.form["name"]:request.form["newpassword"]})
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/",methods=["GET","POST"])
def login():
    error = ""
    if request.method=="POST":
        session["Username"]=request.form["Username"]
        sql= sqlite3.connect("database_1.db")
        data= sql.execute("SELECT * FROM login")
        for i in data:
            if i[0]== request.form["Username"] and i[1]== request.form["Password"]:
                return redirect(url_for("menu"))
            #sql.close()
        #for k,v in database.items():
        #    if k == request.form["Username"] and v == request.form["Password"]:
        #        return redirect(url_for("blogpage"))
        else:
            error="Invalid Credentials try again"
            return render_template("loginpage.html", error=error)
    return  render_template("loginpage.html",error = error)

@app.route("/menu")
def menu():
    if "Username" in session:
        N=session["Username"]
        title=[]
        desc=[]
        menu1=sqlite3.connect("menubase.db")
        it=menu1.execute("SELECT * from items")
        for i in it:
            title.append(i[0])
            desc.append(i[1])
        return render_template("menu.html",title=title,desc=desc,N=N)



@app.route("/blogpage")
def blogpage():
    if "Username" in session:
        N= session["Username"]
        return render_template("blog.html",N= N)
    else:
        return "<p>Please Login First</p>"



@app.route("/logout")
def logout():
    if "Username" in session:
        session.pop("Username",None)
        return render_template("logout.html")

@app.route("/result",methods=["POST"])
def result():
    if "Username" in session:
        N = session["Username"]
        title= request.form["title"]
        blog = request.form["text"]
        menu1= sqlite3.connect("menubase.db")
        menu1.execute("INSERT INTO items(title,desc)VALUES(?,?)",(title,blog))
        menu1.commit()
        return render_template("result.html",title= title,blog= blog,N=N)

if __name__ == "__main__":
    app.run(debug=True)
