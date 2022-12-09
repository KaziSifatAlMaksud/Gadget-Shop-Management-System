from flask import Flask,render_template
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flasksfa!"


@app.route("/landing")
def home_page():
    return render_template('index.html')

@app.route("/about")
def about_page():
    return render_template('mithu.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/register")
def register():
    return render_template('register.html')


if __name__ == "__main__":
    app.run(debug=True)
 #   app.run(host="127.0.0.1",port=5005)