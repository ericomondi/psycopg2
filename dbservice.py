import psycopg2

 # Here we establish the connection
conn = psycopg2.connect(
    host='127.0.0.1',
    database = "duka",
    user = "postgres",
    password = "2345"
    
)
# Create a cursor
cursor = conn.cursor() 
# get table data

def get_data(table_name):

        # here we etrieve data from the table and return them as records
        
        cursor.execute(f"SELECT * FROM {table_name}")
        records = cursor.fetchall()

        return records

# def insert_data(table_name, values, columns):
#     try:
#         plc_holders = ", ".join(["%s" for column in columns])
#         insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({plc_holders})"
        
#         cursor.execute(insert_query, values)
#         conn.commit()
        
#         print(f"Data inserted into {table_name} successfully!")
#     except psycopg2.Error as error:
#         conn.rollback()  # Roll back the transaction on error
#         print(f"Error inserting into {table_name}: {error}")

# insert [product]
def insert_product(values):
    # SQL query to insert data
    insert_query = "INSERT INTO products (product_name, buying_price, selling_price, stock_quantity) VALUES (%s, %s, %s, %s)"
    try:
        cursor.execute(insert_query, values)
        conn.commit()
    except Exception as e:
        # Handle any errors here
        print("Error:", e)
        conn.rollback()
    
# insert sale
def insert_sale(values):
    # SQL query to insert data
    insert_query = "INSERT INTO sales (product_id, quantity, created_at) VALUES (%s, %s, %s)"
    try:
        cursor.execute(insert_query, values)
        conn.commit()
    except Exception as e:
        # Handle any errors here
        print("Error:", e)
        conn.rollback()

# remaining stock

def remaining_stock():
    stock = [] # a list to append each product info
    
    cursor.execute(f'SELECT * FROM rem_stock')
    rem_stocks = cursor.fetchall()
    
    for rem_stock in rem_stocks:
        product = {}  # Create a new dictionary for each product
        product['product_name'] = rem_stock[1]
        product['rem_stock'] = rem_stock[2]
        stock.append(product)
    
    return stock




