from flask import Flask, render_template, request, redirect, url_for
from flask import  flash,session
from dbservice import get_data, insert_product, insert_sale, remaining_stock, update_product_barcode
from dbservice import check_email, check_email_password,create_user, get_pid
from functools import wraps
import barcode
from barcode import Code128
from barcode.writer import ImageWriter
import psycopg2



app = Flask(__name__, static_url_path='/static')   
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# a function to check if user is authenticated
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'loggedin' in session:
            return f(*args, **kwargs)
        else:
            print(session)  # Debug: Print the session data
            flash("You need to login first")
            return redirect(url_for('login'))
    return wrap



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
        if user:
            x = user[1]
            username = x.split()
            first_name = username[0]
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            session['loggedin'] = True
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
@login_required
def products():
    records = get_data("products")
    return render_template("products.html", products=records )
   
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
@login_required
def sales():
    prods = get_data("products")
    records = get_data("sales")
    return render_template("sales.html", sales= records,products = prods)
   
    

@app.route("/receipt" , methods = ["GET"])
def receipt():
    receipt= get_data("last_receipt")
    return render_template("receipt.html", receipt=receipt)

# add sale
@app.route("/add-sale", methods=["GET", "POST"])
def add_sale():
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
    # profit per day
    data = get_data("profit_per_day")
    dates = [date for date, profit in data]
    profits = [profit for date, profit in data]


    # top five sales
    top_sales = get_data("top_five_sales")
    p_names = [name[0] for name in top_sales]
    p_sales = [sale[1] for sale in top_sales]
   

    return render_template("dashboard.html", dates=dates,profits=profits,p_names=p_names,p_sales=p_sales)

    

@app.route("/remaining-stock")
def rem_stock():
    records = remaining_stock()
    return render_template("stock.html", stocks=records)



@app.context_processor
def generate_barcode():
    id_list = get_pid()  # Replace with your function to get product IDs
    barcode_paths = []

    for pid_tuple in id_list:
        pid = pid_tuple[0]
        try:
            code = Code128(str(pid), writer=ImageWriter())
            barcode_filename = f"{pid}"  
            barcode_path = f"barcodes/{barcode_filename}" 
            code.save(f"static/{barcode_path}")
            barcode_paths.append(barcode_path)

            # Update the product's barcode in the database
            update_product_barcode(pid, barcode_filename) 
        except Exception as e:
            print(f"Error generating barcode for product with ID {pid}: {str(e)}")

    return {'generate_barcode': generate_barcode}


@app.route("/products-barcodes",methods=["GET"])
@login_required
def products_barcodes():
    records = get_data("products")
    return render_template("products-barcodes.html", products=records )


@app.route("/logout")
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    flash("You have been logged out.")
    return redirect(url_for("login"))












if __name__ == '__main__':
    app.run(debug=True)

