import psycopg2

 # Here we establish the connection
conn = psycopg2.connect(
    host='127.0.0.1',
    database = "duka",
    user = "postgres",
    password = "2345"
    
)
        

def get_data(table_name):
    
       
        # Create a cursor
        cursor = conn.cursor()

        # here we etrieve data from the table and return them as records
        
        cursor.execute(f"SELECT * FROM {table_name}")
        records = cursor.fetchall()

        return records

# sales = get_data("sales")
prods = get_data("products")

# # here we loop throgh the prods 'list' to print each record
for product in prods:
    print(product)

conn.close()

