from backend.util.database_connector import get_connection 

class AuthenticationService:
    def login(self,username,password):
        con=None
        try:
            con=get_connection()
            cursor=con.cursor()

            query="select * from login where username=%s and password=%s"
            cursor.execute(query,(username,password))
            result = cursor.fetchall()

            if result:
                return True
            else:
                return False
 
            
        except Exception as e:
            raise e
        
        finally:
            if con:
                con.close()



            
        



