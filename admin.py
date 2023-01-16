
from os.path import join, dirname, realpath

from flask import Flask, flash, render_template,request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from werkzeug.utils import secure_filename
import pymongo

from bson.objectid import ObjectId
UPLOADS_PATH = join(dirname(realpath(__file__)), 'static\\img')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)
app.secret_key = 'sifat'
from pymongo import MongoClient

myClined = pymongo.MongoClient("mongodb://localhost:27017/gShop")
mydb = myClined["gShop"]
mycol = mydb["user"]
shopProduct = mydb["producat"]
contactMess = mydb["contact"]
adminAccount = mydb["admin"]
odersnumber = mydb["oder"]

@app.route('/',methods=["GET","POST"])
def admin_login():
    if request.method == "POST":
        form_data = request.form
        email = form_data["email"]
        passw = form_data["enter_pass"]
        user_name = adminAccount.find_one({"email": email})
        if user_name is None:
            email_mess = "Email was not register, Please Sign Up"
        user_passw = adminAccount.find_one({"password": passw})
        if user_passw is None:
            pass_mess = "Password not Correct, Try Again "
        if user_passw is not None:
            profile_name = user_passw["name"]
            email_address = user_passw["email"]
            return redirect(url_for('dashboard'))
    return render_template("admin_login.html",**locals())
@app.route('/dashboard',methods=["GET","POST"])
def dashboard():  # put application's code here
    user = []
    admin = []
    p =[]
    m = []
    o =[]
    total_amount = 0
    for y in mycol.find():
        user.append(y)
    u_l =len(user)
    for y in adminAccount.find():
        admin.append(y)
    a_l = len(admin)
    for y in shopProduct.find():
        p.append(y)
    p_l = len(p)
    for y in contactMess.find():
        m.append(y)
    m_l = len(m)
    for y in odersnumber.find():
        o.append(y)
        total_amount = total_amount + (int)(y['total_price'])
    o_l = len(o)
    return render_template("dashboard.html",**locals())

@app.route('/products',methods=['GET', 'POST'])
def products():  # put application's code here
    if request.args.get('id') is not None:
        id = request.args.get('id')
        shopProduct.delete_one({'_id': ObjectId(id)})
    elif request.args.get('update_p') is not None:
        id = request.args.get('update_p')
        find = shopProduct.find_one({'_id': ObjectId(id)})
        nowid = find['_id']
        p_type = find['Type']
        p_price = find['price']
        p_model = find['Model']
        p_prose = find['Processor']
        p_display = find['Display']
        p_ram = find['Ram']
        p_graphics = find['Graphics']
        p_features = find['Features']
        p_warranty = find['Warranty']
        image = find['image']
        p_description = find['Description']
    else:
        f = "Don't have any id"
    result = ''
    isPost = False
    if request.method == "POST":
        p_type = request.form['type']
        p_price = request.form['price']
        p_model = request.form['model']
        p_prose = request.form['prosesor']
        p_display = request.form['display']
        p_ram = request.form['ram']
        p_graphics = request.form['graphics']
        p_features = request.form['features']
        p_warranty = request.form['warranty']
        image = request.form['file']
        p_description = request.form['discrption']
        shopProduct.insert_one({'Type':p_type, 'price': p_price,'Model':p_model,'Processor':p_prose ,'Display':p_display,'Ram':p_ram,'Graphics': p_graphics,'Features':p_features,'Warranty':p_warranty,'image':"images/"+image,'Description':p_description })
        isPost = True
        result = "Insert Successfully"
        print(result)
    return render_template("products.html",**locals())
@app.route('/messages')
def messages():  # put application's code here
    return render_template("messages.html",**locals())
@app.route('/user')
def user():  # put application's code here
    if request.args.get('id') is not None:
        id = request.args.get('id')
        mycol.delete_one({'_id': ObjectId(id)})
    else:
        f = "Don't have any id"
    list = []
    haveuser = False
    for data in mycol.find():
        list.append(data)
        haveuser = True
    return render_template("user.html",**locals())
@app.route('/admin')
def admin():  # put application's code here
    if request.args.get('id') is not None:
        id = request.args.get('id')
        adminAccount.delete_one({'_id': ObjectId(id)})
    else:
        f = "Don't have any id"
    list = []
    haveuser = False
    for data in adminAccount.find():
        list.append(data)
        haveuser = True
    return render_template("admin.html",**locals())
@app.route('/oder')
def oder():  # put application's code here
    if request.args.get('id') is not None:
        id = request.args.get('id')
        odersnumber.delete_one({'_id': ObjectId(id)})
    else:
        f = "Don't have any id"
    list = []
    haveoder = False
    for value in odersnumber.find():
        list.append(value)
        haveoder = True
    return render_template("oder.html",**locals())
@app.route('/update_payment')
def update_payment():
        if request.args.get('id') is not None:
            id = request.args.get('id')
            find = odersnumber.find_one({"_id": ObjectId(id)})
            payment_s = find['payment_status']
            if payment_s == "uncompleted":
                myquery ={"payment_status": payment_s}
                newvakyes = {"$set":{"payment_status": "Completed"}}
                odersnumber.update_one(myquery,newvakyes)
                return redirect(url_for('oder'))
            if payment_s == "Completed":
                myquery ={"payment_status": payment_s}
                newvakyes = {"$set":{"payment_status": "uncompleted"}}
                odersnumber.update_one(myquery,newvakyes)
                return redirect(url_for('oder'))
@app.route('/admin_add',methods=['GET', 'POST'])
def admin_add():
    if request.method == "POST":
        form_data = request.form
        name = form_data["username"]
        email = form_data["email"]
        u_pass = form_data["password"]
        re_pass = form_data["re_password"]
        if u_pass == re_pass:
            d = {"name": name, "email": email, "password": re_pass}
            x = adminAccount.insert_one(d)
        else:
            passmess = "Password is not match"
    return render_template("admin_add.html",**locals())

@app.route('/view_product')
def view_product():  # put application's code here
    if request.args.get('id') is not None:
        id = request.args.get('id')
        shopProduct.delete_one({'_id': ObjectId(id)})
    else:
        f = "Don't have any id"
    list = []
    haveuser = False
    for data in shopProduct.find():
        list.append(data)
        haveuser = True
    return render_template("view_product.html",**locals())

if __name__ == "__main__":
    app.run(debug=True)