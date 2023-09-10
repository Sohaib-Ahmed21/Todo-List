import pypyodbc as odbc
connection_string="Driver={ODBC Driver 18 for SQL Server};Server=tcp:todo-list-server.database.windows.net,1433;Database=todo-list;Uid=sohaib;Pwd=alpha122-;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
conn = odbc.connect(connection_string)
cursor = conn.cursor()

try:        # Table should be created ahead of time in production app.
    # Create the 'users' table
    cursor.execute("""
    CREATE TABLE users (
        id INT PRIMARY KEY IDENTITY(1,1),
        username VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password VARCHAR(100) NOT NULL
    )
""")

# Create the 'todos' table
    cursor.execute("""
    CREATE TABLE todos (
        id INT PRIMARY KEY IDENTITY(1,1),
        todo VARCHAR(255) NOT NULL,
        complete_status BIT DEFAULT 0,
        user_id INT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
""")

    conn.commit()
except Exception as e:
        # Table may already exist
    print(e)
# from sqlalchemy import create_engine

# # Define the SQLAlchemy URI
# server = 'todo-list-server.database.windows.net'
# database = 'todo-list'
# username = "sohaib"
# # conn = odbc.connect(connection_string)'
# password = 'alpha122-'
# # Create an SQLAlchemy engine and connection
# uri= f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+18+for+SQL+Server&trusted_connection=no&encrypt=no"
# engine = create_engine(uri)
# connection = engine.connect()

# # # Execute SQL queries using SQLAlchemy
# # result = connection.execute("SELECT * FROM your_table_name")
# # for row in result:
# #     print(row)

# # # Close the connection
# connection.close()
print("done")