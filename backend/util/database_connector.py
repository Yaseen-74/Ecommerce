import mysql.connector
import configparser
from backend.exception.exceptions import DatabaseConnectorError  # fix the import if needed

def get_connection():
    try:
        config = configparser.ConfigParser()
        config.read('backend/config/config.ini')

        if "mysql" not in config:
            raise DatabaseConnectorError("Missing 'mysql' section in config.ini")

        db = config["mysql"]

        return mysql.connector.connect(
            host=db["host"],
            user=db["user"],
            password=db["password"],
            database=db["database"]
        )

    except mysql.connector.Error as e:
        raise DatabaseConnectorError(f"MySQL connection error: {e}")
    except Exception as e:
        raise DatabaseConnectorError(f"General DB error: {e}")
