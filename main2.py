from sqlalchemy import create_engine

# Replace the placeholders with your PostgreSQL database information
db_user = 'postgres'
db_password = '2345'
db_host = 'localhost'  # This can be an IP address or 'localhost' if the database is on your local machine
db_port = '5432'  # Default PostgreSQL port is 5432
db_name = 'duka'

# PostgreSQL URL format for create_engine
db_url = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

engine = create_engine(db_url)