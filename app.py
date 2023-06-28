from flask import Flask, render_template, request, redirect
import mysql.connector
from datetime import datetime

now = datetime.now()
formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1234",
  database="boutique"
)
mycursor = mydb.cursor()

app=Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/admin_register", methods=["POST", "GET"])
def admin_register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        sql = "INSERT INTO admin_detail (username, email, password) VALUES (%s, %s, %s)"
        val = (username, email, password)
        mycursor.execute(sql, val)
        mydb.commit()
        if mycursor.rowcount == 1:
           return render_template("admin_login.html") 

    return render_template("admin_register.html")

@app.route("/admin_login", methods=["POST", "GET"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        sql = "select * from admin_detail where username=%s and password=%s"
        val = (username, password)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        print(mycursor.rowcount)
        if int(mycursor.rowcount) == 1:
           return redirect("admin_dashboard") 
        
    return render_template("admin_login.html")

@app.route("/admin_dashboard", methods=["POST", "GET"])
def admin_dashboard():
    # mycursor.execute("SELECT id, gas_type, location, quantity_available FROM gas_inventory")
    # myresult = mycursor.fetchall()
    # print(list(myresult))
    return render_template("admin_dashboard.html")

@app.route("/admin_order", methods=["POST", "GET"])
def admin_order():
    mycursor.execute("SELECT * FROM order_detail")
    myresult = mycursor.fetchall()
    print(list(myresult))
    return render_template("admin_order.html", myresult=list(myresult))

@app.route("/user_register", methods=["POST", "GET"])
def user_register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        sql = "INSERT INTO user_detail (username, email, password) VALUES (%s, %s, %s)"
        val = (username, email, password)
        mycursor.execute(sql, val)
        mydb.commit()
        if mycursor.rowcount == 1:
           return render_template("user_login.html") 

    return render_template("user_register.html")

@app.route("/user_login", methods=["POST", "GET"])
def user_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        global client_user
        client_user = username
        
        sql = "select * from user_detail where username=%s and password=%s"
        val = (username, password)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        print(mycursor.rowcount)
        if int(mycursor.rowcount) == 1:
           return redirect("user_dashboard") 
        
    return render_template("user_login.html")

@app.route("/user_dashboard", methods=["POST", "GET"])
def user_dashboard():
    return render_template("user_dashboard.html", client_user=client_user)

@app.route("/user_cat", methods=["POST", "GET"])
def user_cat():
    if request.method == "POST":
        i1 = request.form.get("i1")
        i2 = request.form.get("i2")
        i3 = request.form.get("i3")
        i4 = request.form.get("i4")
    return render_template("user_fab.html",i1=i1,i2=i2,i3=i3,i4=i4)

@app.route("/user_order", methods=["POST", "GET"])
def user_order():
    if request.method == "POST":
        i1 = request.form.get("i1")
        i2 = request.form.get("i2")
        i3 = request.form.get("i3")
        i4 = request.form.get("i4")
        measurement = request.form.get("measurement")
        payment = request.form.get("payment")
        f1 = request.form.get("f1")
        f2 = request.form.get("f2")
        f3 = request.form.get("f3")
        f4 = request.form.get("f4")
        sql = "INSERT INTO user_order (cat1,cat2,cat3,cat4,fab1,fab2,fab3,fab4,measurement,payment) VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s, %s)"
        val = (i1,i2,i3,i4,f1,f2,f3,f4,measurement,payment)
        mycursor.execute(sql, val)
        mydb.commit()


    return render_template("user_dashboard.html")


if __name__=="__main__":
    app.run(debug=True)