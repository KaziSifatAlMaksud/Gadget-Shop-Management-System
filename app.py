from flask import Flask, render_template, request, url_for, redirect, session
import pymongo
app = Flask(__name__)

myClined = pymongo.MongoClient("mongodb://localhost:27017/gShop")
mydb = myClined["gShop"]
mycol = mydb["user"]

@app.route("/")
def home_page():
    return render_template('index.html')

@app.route("/about")
def about_page():
    return render_template('about.html')

@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        form_data = request.form
        username = form_data["email"]
        password = form_data["password"]
        print(username)
        print(password)
        for x in mycol.find({"email": username},{"re_pass": password}):

            return "hellow sifat"

    return render_template("login.html", **locals())


@app.route("/register",methods=["GET","POST"])
def register():
    user_d = {}
    if request.method == "POST":
        form_data = request.form
        user_name = form_data["name"]
        user_email = form_data["email"]
        user_mobile = form_data["mobile"]
        user_pass = form_data["password1"]
        user_re_pass = form_data["password2"]
        user_d["name"] = user_name
        user_d["email"] = user_email
        user_d["mobile"] = user_mobile
        user_d["pass"] = user_pass
        user_d["re_pass"] = user_re_pass
        mycol.insert_one(user_d)
        return render_template("login.html", **locals())
    return render_template('register.html',**locals())

@app.route("/contact")
def contact():
    return render_template('contact.html')
@app.route("/menu")
def menu():
    return render_template('menu.html')
@app.route("/quick_view")
def quick_view():
    return render_template('quick_view.html')

if __name__ == "__main__":
    app.run(debug=True)
 #   app.run(host="127.0.0.1",port=5005)