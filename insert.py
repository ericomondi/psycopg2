import psycopg2
# we pass the connection as an argument to to deal with any issue
# of how the database connection is being handled
def insert_data(conn,table_name, values, columns):
    try:
        # Create a cursor
        cursor = conn.cursor()

        # tuple containing the names of the columns where you 
        # want to insert data
        col_str = ", ".join(columns) #.join is used to concantenate the columns into commma separated strings
        #  a comprehension is used below to create a list
        #  '%s' is a placeholder used in parametized queries
        plc_holders = ", ".join(["%s" for column in columns]) #concatinate the placeholders into a comma separated str
        insert_query = f"INSERT INTO {table_name} ({col_str}) VALUES ({plc_holders}) "

        # we then  execute the insert statment
        cursor.execute(insert_query,values)

        # commit transaction
        conn.commit()

        print(f"data inserted into {table_name} succecfull!")

    except psycopg2.Error as error:
        print(f'error inserting into {table_name} : {error}')

   

# Establish the connection
conn = psycopg2.connect(
    host='127.0.0.1',
    database='duka',
    user='postgres',
    password='2345'
)


# we now call the insert_data with table name,
# a tuple of values and a tuple of columns names
# example

new_sale = (2, 10, 'now()')
columns = ('product_id','quantity','created_at')
insert_data (conn, 'sales' , new_sale, columns)

# columns = ('name', 'buying_price', 'selling_price', 'stock_quantity')
# new_products = ('raw milk', 50, 100, 200)
# insert_data(conn, 'products', new_products, columns)

conn.close()

