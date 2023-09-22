import psycopg2


def get_data(table_name):
    try:
        # Here we establish the connection
        conn = psycopg2.connect(
            host='127.0.0.1',
            database = "duka",
            user = "postgres",
            password = "2345"
            
        )
        
        # Create a cursor
        cursor = conn.cursor()

        # here we etrieve data from the table and return them as records
        cursor.execute(f"SELECT * FROM {table_name}")
        records = cursor.fetchall()

        return records

    
# here we know close the connection
    finally:
        if conn:
            conn.close()

# a variable to store the table name to
# be passsed as an argument


sales = get_data("sales")
prods = get_data("products")

# # here we loop throgh the records 'list' to print each record
for product in prods:
    print(product)


