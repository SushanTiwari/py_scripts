import psycopg2

# Replace these with your PostgreSQL database connection details
db_params = {
    'host': 'localhost',
    'port': 15432,
    'database': 'translator_state_db_dev',
    'user': 'admin',
    'password': 'adminpw',
}

# Connect to the PostgreSQL database
connection = psycopg2.connect(**db_params)
cursor = connection.cursor()

# Insert 10,000 rows into users_orgs
for i in range(10000):
    user_id = i
    org_id = 1

    cursor.execute('''
        INSERT INTO users_orgs (user_id, org_id) VALUES (%s, %s)
    ''', (user_id, org_id))

# Commit the changes and close the connection
connection.commit()
connection.close()
