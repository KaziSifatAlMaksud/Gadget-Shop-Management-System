from flask import Flask, render_template, request, url_for, redirect, session
import pymongo

app = Flask(__name__)
myClined = pymongo.MongoClient("mongodb://localhost:27017/gShop")
mydb = myClined["gShop"]
mycol = mydb["user"]
shopProduct = mydb["producat"]
contactMess = mydb["contact"]

@app.route("/", methods=['GET', 'POST'])
def home_page():
    prodct_arry = []
    for y in shopProduct.find():
        prodct_arry.append(y)
    l = len(prodct_arry)
    if request.method == "POST":
        form_data = request.form
        prodct_model = form_data['pid']
        x = shopProduct.find_one({"Model":prodct_model})
        if x is not None:
            p_type = x["Type"]
            p_price = x["price"]
            p_model = x["Model"]
            p_processor =x["Processor"]
            p_display = x["Display"]
            p_ram = x["Ram"]
            p_feat = x["Features"]
            p_warrant = x["Warranty"]
            p_image = x["image"]
            p_descript = x["Description"]
            print(p_display)
        return render_template('quick_view.html', **locals())
    return render_template('index.html',**locals())

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
    return render_template('about.html')
@app.route("/checkout")
def checkout_page():
    return render_template('checkout.html')
@app.route("/cart")
def cart_page():
    return render_template('cart.html')

@app.route("/order")
def order_page():
    return render_template('order.html')



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
    return render_template('profile.html')
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
                logprofile = True
                message = "Hello,{username}"
                print(message)
                return render_template("index.html ",**locals())
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
    return render_template('quick_view.html',**locals())

if __name__ == "__main__":
    app.run(debug=True)
 #   app.run(host="127.0.0.1",port=5005)