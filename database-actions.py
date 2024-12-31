import psycopg2

DB_USER_FILE = "secrets/postgres_user"
DB_PASSWORD_FILE = "secrets/postgres_password"
# Change host IP per final deployment
DB_HOST_ADDRESS = "192.168.100.222"

# Read secrets securely
def read_secret(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()
    
# initialize Database credentials
db_user = read_secret(DB_USER_FILE)
db_password = read_secret(DB_PASSWORD_FILE)

try:
    conn = psycopg2.connect(
        dbname="smart-home-db",
        user=db_user,
        password=db_password,
        host=DB_HOST_ADDRESS,
        port=5432
    )

    cur = conn.cursor()
    cur.execute("SELECT * FROM smart_sensors;")
    rows = cur.fetchall()
    print(rows)

    cur.close()
    conn.close()

except Exception as e:
    print(f"An error occurred: {e}")