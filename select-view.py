import psycopg2

 # Here we establish the connection
conn = psycopg2.connect(
    host='127.0.0.1',
    database = "duka",
    user = "postgres",
    password = "2345"
    
)
        

def get_data(view_name):
    
       
        # Create a cursor
        cursor = conn.cursor()

        # here we etrieve data from the table and return them as records
        
        cursor.execute(f"SELECT * FROM {view_name}")
        records = cursor.fetchall()

        return records

last_sales = get_data("last_sale")
last_product = get_data("last_product")

# # here we  print 
print(last_product)


print(last_sales)
conn.close()

