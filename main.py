from flask import Flask, render_template, request, redirect, url_for
from flask import  flash,session
from dbservice import get_data, insert_product, insert_sale, remaining_stock
from dbservice import check_email, check_email_password,create_user
from datetime import datetime


app = Flask(__name__)   
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.context_processor
def stock_quantity_processor():
    def check_stock_quantity(product_id, quantity):
        products = get_data("products")
        for product in products:
            if product[0] == product_id:
                if product[4] >= quantity:  # Check if stock quantity is sufficient
                    return True
                else:
                    return False
        return False  # Product not found
    return dict(check_stock_quantity=check_stock_quantity)


# a function to check if user is authenticated
# decorator function
def confirm_auth():
    return 'user_id' in session

# index route
@app.route("/")
def index():
    return render_template("landing.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        values = ("",email,password)
        user = check_email_password(email, password)
        found = check_email(email)
        x = user[1]
        username = x.split()
        first_name = username[0]
        if user:
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            flash(f'Welcome {first_name}')
            return redirect(url_for("dashboard"))
        elif not found: 
            create_user(values)
            flash("Account created!")
            flash("Login to access account")
            return redirect(url_for("login"))
        else:
            flash("Invalid logins")

    # Render the login page for GET requests
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
     if request.method == 'POST' and 'full_name' in request.form and 'email' in request.form and 'password' in request.form:
        fullname = request.form['full_name']
        password = request.form['password']
        email = request.form['email']
        values = (fullname,email,password)
        email_b = check_email(email)

        # Email Validation
        if email_b:
            flash("Email is already in use")
        elif not  password or not email:
            flash("Please fill all the inputs")
        else:
            create_user(values)
            flash("You have registered successfully!")
            return redirect(url_for("login"))
    
    # Render the register page for GET requests
     return render_template("register.html")

# get products
@app.route("/products",methods=["GET"])
def products():
    if confirm_auth():    
        records = get_data("products")
        return render_template("products.html", products=records )
    else:
        flash("You need to log in to access this page.")
        return redirect(url_for("login"))

# add product
@app.route("/add-product",methods=["POST"])
def add_product():
    product_name = request.form["product_name"]
    buying_price = float(request.form["buying_price"])
    selling_price = float(request.form["selling_price"])
    stock_quantity = int(request.form["stock_quantity"])
    values = (product_name,buying_price,selling_price,stock_quantity)
    # Insert the product into the database
    insert_product(values)
    flash("Product succesfully added!")
    return redirect(url_for("products"))
    
# get sales
@app.route("/sales", methods=["GET"])
def sales():
    if confirm_auth():
        prods = get_data("products")
        records = get_data("sales")
        return render_template("sales.html", sales= records,products = prods)
    else:
        flash("You need to log in to access this page.")
        return redirect(url_for("login"))
    

@app.route("/receipt" , methods = ["GET"])
def receipt():
    receipt= get_data("last_receipt")
    return render_template("receipt.html", receipt=receipt)

# add sale
@app.route("/add-sale", methods=["GET", "POST"])
def add_sale():
    if confirm_auth():
        if request.method == "POST":
            if "product_id" in request.form and "quantity" in request.form:
                product_id = int(request.form["product_id"])
                quantity = float(request.form["quantity"])
                user_id = session["user_id"]  # Capture the active user id from the session
                values = (product_id, quantity, "now()", user_id)
                # Insert the sale into the database
                insert_sale(values)  # Call your dbservice function to insert a sale
                # return redirect(url_for("add-sale"))
            else:
                flash("Make sure all inputs are captured")

        prods = get_data("products")
        return render_template("add-sale.html", products=prods)


# dashboard
@app.route("/dashboard")
def dashboard():
    if confirm_auth():
        # profit per day
        data = get_data("profit_per_day")
        dates = [date for date, profit in data]
        profits = [profit for date, profit in data]


        # top five sales
        top_sales = get_data("top_five_sales")
        p_names = [name[0] for name in top_sales]
        p_sales = [sale[1] for sale in top_sales]
    else:
        flash("You need to log in to access this page.")
        return redirect(url_for("login"))

    return render_template("dashboard.html", dates=dates,profits=profits,p_names=p_names,p_sales=p_sales)

    

@app.route("/remaining-stock")
def rem_stock():
    if confirm_auth():
        records = remaining_stock()
        return render_template("stock.html", stocks=records)
    else:
        flash("You need to log in to access this page.")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    flash("You have been logged out.")
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(debug=True)

