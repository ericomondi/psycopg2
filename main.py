from flask import Flask, render_template, request, redirect, url_for
from dbservice import get_data, insert_product, insert_sale, remaining_stock
app = Flask(__name__)   

# index route
@app.route("/")
def index():
    return render_template("index.html")

# insert_data(table_name, values, columns)
@app.route("/products",methods=["GET", "POST"])
def products_int():
    if request.method == "POST":
        # Retrieve form data
        product_name = request.form["product_name"]
        buying_price = float(request.form["buying_price"])
        selling_price = float(request.form["selling_price"])
        stock_quantity = int(request.form["stock_quantity"])
        values = (product_name,buying_price,selling_price,stock_quantity)
        # Insert the product into the database
        insert_product(values)
        return redirect(url_for("products_int"))
    
    records = get_data("products")
    return render_template("products.html", products=records )


@app.route("/sales", methods=["GET", "POST"])
def sales_int():
    if request.method == "POST":
        # Retrieve form data
        product_id = int(request.form["product_id"])
        quantity = float(request.form["quantity"])
        created_at = (request.form["created_at"])
        values = (product_id,quantity,created_at)
        # Insert the sale into the database
        insert_sale(values)
        return redirect(url_for("sales_int"))

    records = get_data("sales")
    return render_template("sales.html", sales= records)

@app.route("/dashboard")
def dash_int():
    return render_template("dashboard.html")


@app.route("/remaining-stock")
def rem_stock():
    records = remaining_stock()
    return render_template("stock.html", stocks=records)

if __name__ == '__main__':
    app.run(debug=True)


    