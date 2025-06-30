import mysql.connector

def get_connection():
    try:
       return mysql.connector.connect(
       host="127.0.0.1",
       user="root",
       password="yaseen@2006",
       database="flipkart"
       )
    
    except mysql.connector.Error as a:
        print(f"database error is failed:{a}")
        return None


