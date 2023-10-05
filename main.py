from flask import Flask, render_template, request, redirect, url_for
from flask import jsonify, flash
from dbservice import get_data, insert_product, insert_sale, remaining_stock
import pygal


app = Flask(__name__)   
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# index route
@app.route("/")
def index():
    return render_template("landing.html")

# get products
@app.route("/products",methods=["GET"])
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
def sales():
    prods = get_data("products")
    records = get_data("sales")
    return render_template("sales.html", sales= records,products = prods)

# add sale
@app.route("/add-sale", methods=["POST"])
def add_sale():
    # Retrieve form data
    product_id = int(request.form["product_id"])
    quantity = float(request.form["quantity"])
    values = (product_id,quantity,"now()")
    # Insert the sale into the database
    insert_sale(values)
    flash("Sale added succefully!")
    return redirect(url_for("sales"))

# dashboard
@app.route("/dashboard")
def dashboard():
    # remaining_stock
    # Remaining stock per product (bar chart)
    bar_chart = pygal.Bar()
    remaining_stock_data = get_data("rem_stock")  # Query to get remaining stock by product
    product_names = []
    remaining_stock_values = []
    id = []
    for product in remaining_stock_data:
        id.append(product[0])
        product_names.append(product[1])
        remaining_stock_values.append(product[2])
    bar_chart.title = "Remaining Stock by Product"
    bar_chart.x_labels = id
    bar_chart.add('Stock', remaining_stock_values)
    bar_chart_rem = bar_chart.render_data_uri()


    return render_template("dashboard.html", bar_chart_rem=bar_chart_rem)

@app.route("/remaining-stock")
def rem_stock():
    records = remaining_stock()
    return render_template("stock.html", stocks=records)


@app.context_processor
def stock_quantity_processor():
    def check_stock_quantity(product_id, quantity):
        products = get_data("products")
        for product in products:
            if product[0] == product_id:
                if product[4] >= quantity:  # Check if stock quantity is sufficient
                    return True
                else:
                    flash("Product out of stock")
                    return False
        return False  # Product not found
    return dict(check_stock_quantity=check_stock_quantity)




if __name__ == '__main__':
    app.run(debug=True)

