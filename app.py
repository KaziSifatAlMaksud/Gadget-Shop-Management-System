from flask import Flask, render_template, request, url_for, redirect, session
import pymongo
from bson.objectid import ObjectId
from flask import *
app = Flask(__name__)
app.secret_key = "sifat"
myClined = pymongo.MongoClient("mongodb://localhost:27017/gShop")
mydb = myClined["gShop"]
mycol = mydb["user"]
shopProduct = mydb["producat"]
contactMess = mydb["contact"]
contactOrder = mydb['oder']


@app.before_request
def before_request():
    g.user = None

    if 'user' in session:
        g.user = session['user']





@app.route("/", methods=['GET', 'POST'])
def home_page():
    prodct_arry = []
    if 'product' not in session:
        session['product'] = []
        session['len_product'] = 0
        session['sub_total'] = 0
    for y in shopProduct.find():
        prodct_arry.append(y)
    l = len(prodct_arry)
    cart_list = session['product']
    if request.method == "POST":
        form_data = request.form
        pr_model = form_data['pid']
        cart_list.append(pr_model)
        session['product'] = cart_list
        print(session)
        session['len_product'] = len(session['product'])


    return render_template('index.html', **locals())

@app.route("/<name>", methods=['GET', 'POST'])
def home(name):
        prodct_arry = []
        name = name.replace("_"," ")
#        for x in shopProduct.find({"Model": search_value}):
#            prodct_arry.append(x)
        for x in shopProduct.find({"Type": name}):
            prodct_arry.append(x)
        l = len(prodct_arry)
        return render_template('search.html', **locals())


@app.route("/about")
def about_page():
    print(session)
    return render_template('about.html')
@app.route("/checkout",methods=["GET","POST"] )
def checkout_page():
    if request.method == "POST":
        form_data = request.form
        user_name = form_data['name']
        user_email = form_data['email']
        user_mobile = form_data['mobile']
        if form_data['address'] is not None:
            user_address = form_data['address']
        else:
            user_address = "None"
        user_method = form_data['method']
        user_oder = form_data['id']
        user_total_price = form_data['sub-total']
        payment_status = "uncompleted"
        oder = {"name":user_name,"email": user_email,"mobile": user_mobile,
                "payment_method": user_method,"address":user_address,"your_orders": user_oder,
                "total_price": user_total_price,"payment_status": payment_status}
        contactOrder.insert_one(oder)
        if 'product' in session:
            session.pop('product',None)
            session.pop('sub_total',None)
            session.pop('len_product',None)

            return redirect(url_for('home_page'))
    if 'user' in session:
        user = session['user']
        for x in mycol.find({"email": user}):
            user_id = x['_id']
            user_name = x['name']
            user_mobile = x['mobile']
            user_email = x['email']
            if x['address'] is not None:
                user_address = x['address']

                return render_template('checkout.html', **locals())
            else:
                return render_template('checkout.html', **locals())
    else:
        return '<p>Please login first</p>'



    return render_template('checkout.html')
@app.route("/cart")
def cart_page():
    # if request.args.get('delete') is not None:
    #     id = request.args.get('delete')
    #     print(id)
    #     len_product = len(session['product'])
    #     date_item = False
    #     for x in range(len_product):
    #         if session['product'][x] == id:
    #             del session['product'][x]
    #     print(session['product'])

    # if request.args.get('delete_all') is not None:
    #     print("clicked delte all")
    #     request.args.get('delete+all')
    #     return redirect(url_for('cart_page'))
    #     for x in range(len_product):
    #         if session['product'][x] == id:
    #             print("sifat")
    #             del session['product'][x]
    #             print("valuo delete")
    #             session.pop(session['product'][x])
    #
    #     return redirect(url_for('profile_page'))
    prodct_arry = []
    if 'product' not in session:
        session['product'] = []
        session['len_product'] = 0
        session['sub_total'] = 0
    sub_total = 0
    len_product = len(session['product'])
    for y in range(len_product):
        x = shopProduct.find_one({"_id": ObjectId(session['product'][y])})
        prodct_arry.append(x)
        session['sub_total'] = session['sub_total'] + x['price']
    l = len(prodct_arry)

    return render_template('cart.html',**locals())

@app.route("/order",methods=['GET',"POST"])
def order_page():
    list = []
    haveoder = False
    for data in contactOrder.find():
        list.append(data)
        haveoder = True
    return render_template('order.html', **locals())
@app.route("/update_address",methods=['GET',"POST"])
def update_address_page():
   if request.method == "POST":
        if request.form["btn"] == "save address":
            form_data = request.form
            user_email = form_data["email"]
            user_districts = form_data["districts"]
            user_city = form_data["city"]
            user_upazila = form_data["upazila"]
            user_pin_code = form_data["pin_code"]
            for x in mycol.find({"email": user_email}):
                myquery = {"email": x["email"]}
                newvalues = {"$set": {"email": user_email,"address": user_districts +","+ user_city+","+user_upazila+","+user_pin_code}}
                mycol.update_one(myquery, newvalues)
                print("update Successfull")
   return render_template('update_address.html',**locals())

@app.route("/profile")
def profile_page():
    if 'user' in session:
        user = session['user']
        for x in mycol.find({"email": user}):
            user_name = x['name']
            session['name'] = user_name
            user_mobile = x['mobile']
            user_email = x['email']
            if x['address'] is not None:
                user_address = x['address']
                return render_template('profile.html', **locals())
            else:
                return render_template('profile.html', **locals())
    else:
        return '<p>Please login first</p>'


@app.route("/logout")
def logout_page():
    if 'user' in session:
        session.pop('user', None)
        session.pop('name', None)
        session.pop('product',None)
        return render_template('login.html',**locals());
    else:
        return '<p>user already logged out</p>'

@app.route("/update_profile",methods=['GET',"POST"])
def update_profile_page():
    if request.method == "POST":

        if request.form["btn"] == "update now":
            form_data = request.form
            user_name = form_data["name"]
            user_email = form_data["email"]
            user_mobile = form_data["number"]
            user_old_pas = form_data["old_pass"]
            user_pass = form_data["new_pass"]
            user_re_pass = form_data["confirm_pass"]
            for x in mycol.find({"email": user_email}):
                myquery = {"name":x["name"],"email": x["email"],"mobile":x["mobile"],"pass": x["re_pass"]}
                newvalues = {"$set": {"name": user_name ,"email": user_email ,"mobile": user_mobile,"pass": user_re_pass,"address":""}}
                mycol.update_one(myquery,newvalues)
                print("update Successfull")
    return render_template('update_profile.html')

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == "POST":
        form_data = request.form
        username = form_data["email"]
        password = form_data["pass"]
        for x in mycol.find({"email": username}):
            for y in mycol.find({"re_pass": password}):
                session['user'] = username
                return redirect(url_for('profile_page'))
        message = "Username or password is incorrect"
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
        user_d["address"] = ""
        mycol.insert_one(user_d)
        sucess_mess = "Register Successfully"
        #return render_template("login.html", **locals())
    return render_template('register.html',**locals())

@app.route("/contact",methods=["GET","POST"])
def contact():
    cont_d = {}
    if request.method == "POST":
        form_data = request.form
        cont_name = form_data["name"]
        cont_email = form_data["email"]
        cont_mess = form_data["msg"]
        cont_d["name"] = cont_name
        cont_d["email"] = cont_email
        cont_d["message"] = cont_mess
        contactMess.insert_one(cont_d)
        sucessmess = "Register Successfully"
        print(sucessmess)
    return render_template('contact.html')
@app.route("/menu", methods=["GET","POST"])
def menu():
    prodct_arry = []
    for k in shopProduct.find():
        prodct_arry.append(k)
    l = len(prodct_arry)
    if request.method == "POST":
        if request.form["btn"] == "search":
            prodct_arry.clear()
            if request.method == "POST":
                form_data = request.form
                search_value = form_data['search_box']
                for x in shopProduct.find({"Model": search_value}):
                    prodct_arry.append(x)
                for x in shopProduct.find({"Type": search_value}):
                    prodct_arry.append(x)
                l = len(prodct_arry)
                return render_template('menu.html', **locals())
        elif request.form["btn"] == "eye":
            form_data = request.form
            prodct_model = form_data['pid']
            x = shopProduct.find_one({"Model": prodct_model})
            if x is not None:
                p_type = x["Type"]
                p_price = x["price"]
                p_model = x["Model"]
                p_processor = x["Processor"]
                p_display = x["Display"]
                p_ram = x["Ram"]
                p_feat = x["Features"]
                p_warrant = x["Warranty"]
                p_image = x["image"]
                p_descript = x["Description"]
                print(p_display)
                return render_template('quick_view.html', **locals())
    return render_template('menu.html',**locals())
@app.route("/search",methods=["GET","POST"])
def search():
    if request.method == "POST":
        form_data = request.form
        search_value = form_data['search_box']
        prodct_arry = []
        for x in shopProduct.find({"Model": search_value}):
            prodct_arry.append(x)
        for x in shopProduct.find({"Type": search_value}):
            prodct_arry.append(x)
        l = len(prodct_arry)
        return render_template('search.html',**locals())
@app.route("/quick_view",methods=["GET","POST"])
def quick_view():
    if request.args.get('id') is not None:
        id = request.args.get('id')
        x = shopProduct.find_one({"_id": ObjectId(id)})
        P_id = x['_id']
        p_type = x["Type"]
        p_price = x["price"]
        p_model = x["Model"]
        p_processor = x["Processor"]
        p_display = x["Display"]
        p_ram = x["Ram"]
        p_feat = x["Features"]
        p_warrant = x["Warranty"]
        p_image = x["image"]
        p_descript = x["Description"]
    # if request.args.get('delete') is not None:
    #     id = request.args.get('delete')
    #     print(id)
    #     len_product = len(session['product'])
    #     date_item = False
    #     for x in range(len_product):
    #         if session['product'][x] == id:
    #             del session['product'][x]
    #     print(session['product'])
    # if request.args.get('delete_all') is not None:
    #     id = request.args.get('delete+all')
    #     session['product'] = []
    #     return redirect(url_for('profile_page'))
    return render_template('quick_view.html',**locals())

if __name__ == "__main__":
    app.run(debug=True)
 #   app.run(host="127.0.0.1",port=5005)