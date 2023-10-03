from flask import Flask, render_template, request, redirect, url_for
from dbservice import get_data, insert_product, insert_sale, remaining_stock
import pygal


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
        values = (product_id,quantity,"now()")
        # Insert the sale into the database
        insert_sale(values)
        return redirect(url_for("sales_int"))

    records = get_data("sales")
    prods = get_data("products")
    return render_template("sales.html", sales= records, products = prods)

@app.route("/dashboard")
def dash_int():
   
    # # sales per product
    # bar_chart = pygal.Bar()
    # sp = get_data("sales_per_product")
    # name = []
    # sale = []
    # id = []
    # for s in sp:
    #  id.append(s[0])
    # #  name.append(s[1][:4])
    #  sale.append(s[2])
     

    # bar_chart.title = "Sales per Product"
    # bar_chart.x_labels = id
    # bar_chart.add('Sale', sale)
    # bar_chart_data = bar_chart.render_data_uri()


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

    # alternatively

    

    return render_template("dashboard.html", bar_chart_rem=bar_chart_rem)


@app.route("/remaining-stock")
def rem_stock():
    records = remaining_stock()
    return render_template("stock.html", stocks=records)

if __name__ == '__main__':
    app.run(debug=True)


    