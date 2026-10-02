import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Load variables from .env into the environment
load_dotenv()

def get_connection():
    """
    Opens and returns a new connection to MySQL.
    Every function that needs the database will call this first.
    """
    try:
        connection = mysql.connector.connect(
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", "3306")),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", ""),
    database=os.getenv("DB_NAME", "answer_grading"),
    charset="utf8mb4",
    autocommit=False
)
        return connection
    except Error as e:
        print(f"[DB ERROR] Could not connect to MySQL: {e}")
        raise


def fetch_all(query, params=None):
    """
    Runs a SELECT query and returns ALL matching rows as a list of dicts.
    Example: fetch_all("SELECT * FROM students")
    """
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())
        result = cursor.fetchall()
        return result
    finally:
        cursor.close()
        connection.close()


def fetch_one(query, params=None):
    """
    Runs a SELECT query and returns ONE matching row as a dict (or None).
    Example: fetch_one("SELECT * FROM students WHERE id = %s", (student_id,))
    """
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())
        result = cursor.fetchone()
        return result
    finally:
        cursor.close()
        connection.close()


def execute_query(query, params=None):
    """
    Runs an INSERT, UPDATE, or DELETE query.
    Commits the change and returns the ID of the last inserted row (if any).
    """
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(query, params or ())
        connection.commit()
        return cursor.lastrowid
    except Error as e:
        connection.rollback()
        print(f"[DB ERROR] Query failed: {e}")
        raise
    finally:
        cursor.close()
        connection.close()