# db.py
import mysql.connector
from mysql.connector import Error
import os

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", "152006"),  # CONTRASEÑA REAL
    "database": os.environ.get("DB_NAME", "db_parcial"),
    "auth_plugin": "mysql_native_password"
}

def get_connection():
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn