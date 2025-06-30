import mysql.connector
import configparser
import os
from backend.exception.exceptions import DatabaseConnectorError  # fix the import if needed

def get_connection():
    try:
        config = configparser.ConfigParser()

        # Absolute path to config
        config_path = os.path.join(os.path.dirname(__file__), "..", "config", "config.ini")
        config.read(config_path)

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
