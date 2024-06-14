import sqlite3

# Function to get database connection
def get_db_connection():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    return con

# Use the function to connect with db
con = get_db_connection()
cur = con.cursor()

# Create "users" table
cur.execute(
    """CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT NOT NULL,
        faculty TEXT NOT NULL,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        phone_number TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )"""
)

# Create "availability" table
cur.execute(
    """CREATE TABLE IF NOT EXISTS availability (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lecturer TEXT NOT NULL,
        appointment_date TEXT NOT NULL,
        start_time TEXT NOT NULL,
        end_time TEXT NOT NULL,
        repeat_type TEXT NOT NULL,
        FOREIGN KEY (lecturer) REFERENCES users(username)
    )"""
)

# Create "appointments" table
cur.execute(
    """CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        booking_id INTEGER NOT NULL,
        student TEXT NOT NULL,
        lecturer TEXT NOT NULL,
        appointment_date TEXT NOT NULL,
        appointment_hour TEXT NOT NULL,
        start_time TEXT NOT NULL,
        end_time TEXT NOT NULL,
        purpose TEXT NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY (student) REFERENCES users(username),
        FOREIGN KEY (lecturer) REFERENCES users(username),
        FOREIGN KEY (appointment_date) REFERENCES availability(appointment_date),
        FOREIGN KEY (appointment_hour) REFERENCES availability(appointment_hour),
        FOREIGN KEY (start_time) REFERENCES availability(start_time),
        FOREIGN KEY (end_time) REFERENCES availability(end_time)
    )"""
)

# Create "facultyhub" table
cur.execute(
    """CREATE TABLE IF NOT EXISTS facultyhub (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        faculty_name TEXT NOT NULL,
        faculty_image TEXT NOT NULL
    )"""
)

con.commit()
con.close()
