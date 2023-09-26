import psycopg2

 # Here we establish the connection
conn = psycopg2.connect(
    host='127.0.0.1',
    database = "duka",
    user = "postgres",
    password = "2345"
    
)
        
# get table data

def get_data(table_name):
    
       
        # Create a cursor
        cursor = conn.cursor()

        # here we etrieve data from the table and return them as records
        
        cursor.execute(f"SELECT * FROM {table_name}")
        records = cursor.fetchall()

        return records

sales = get_data("sales")
prods = get_data("products")

# remaining stock

def remaining_stock():
    stock = [] # a list to append each product info
    cursor = conn.cursor()
    
    cursor.execute(f'SELECT * FROM rem_stock')
    rem_stocks = cursor.fetchall()
    
    for rem_stock in rem_stocks:
        product = {}  # Create a new dictionary for each product
        product['name'] = rem_stock[1]
        product['rem_stock'] = rem_stock[2]
        stock.append(product)
    
    return stock

s = remaining_stock()
# the output is a list of dictionaries
print(s)

conn.close()

