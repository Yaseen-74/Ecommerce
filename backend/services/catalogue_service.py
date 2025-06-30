from backend.dto.catalogue import Catalogue
from backend.util.database_connector import get_connection 
from backend.exception.exceptions import(CatalogueDateExpired,CatalogueDeleteError,CatalogueError,CatalogueNotFoundError,CatalogueUpdateError)
from datetime import date,datetime

class CatalogueService:


    def create_catalogue(self,name,description,start_date,end_date,active=True):
        con = None
        try:
            if isinstance(start_date, str):
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            if isinstance(end_date, str):
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            if end_date<date.today():
                raise CatalogueDateExpired(name)
            
            con=get_connection()
            cursor=con.cursor()

            query = """INSERT INTO catalogue (catalogue_name, catalogue_description, start_date, end_date, active) VALUES (%s, %s, %s, %s, %s)"""

            cursor.execute(query,(name,description,start_date,end_date,active))
            con.commit()

            

        except CatalogueDateExpired as e:
            raise e

        except Exception as e:
            raise CatalogueError(f"Error for creating {e}")
        finally:
            if con:
                con.close()



    def get_catalogue(self,catalogue_id):
        con=None
        try:
            con=get_connection()
            cursor=con.cursor()
 
            active_query="update catalogue set active = 0 where catalogue_id = %s and end_date < curdate() and active = 1"
            cursor.execute(active_query,(catalogue_id,))
            con.commit           

            query="SELECT * FROM catalogue where catalogue_id = %s"
            cursor.execute(query,(catalogue_id,))
            row = cursor.fetchone() 

            if not row:
                raise CatalogueNotFoundError(catalogue_id)
            
            print("\n---CATALOGUE LIST----")
            catalogue_id,name,description,start_date,end_date,active = row
            catalogue=Catalogue(catalogue_id,name,description,start_date,end_date,active)
            catalogue.display_info()

        except CatalogueNotFoundError as e:
            print(f"Error:{e}")

        except Exception as e:
            raise CatalogueError(f"Error for fetching {e}")
        
        finally:
            if con:
                con.close()
                

            
    def get_all_catalogue(self):
        con=None
        try:
            con=get_connection()
            cursor=con.cursor()

            active_query="update catalogue set active = 0 where end_date < curdate() and active = 1"
            cursor.execute(active_query)
            con.commit
        

            query="select * from catalogue "
            cursor.execute(query)
            rows=cursor.fetchall()

            if not rows:
                print("There is no catalogues.")
                return
            
            print("\n---CATALOGUE LIST----")
            for row in rows:
                catalogue_id,name,description,start_date,end_date,active = row
                catalogue=Catalogue(catalogue_id,name,description,start_date,end_date,active)
                catalogue.display_info() 

        except Exception as e:
            raise CatalogueError(f"Error for catelogues {e}")
        finally:
            if con:
                con.close()               



    def update_catalogue(self,catalogue_id,name,description,start_date,end_date,active=True):
        con = None
        try:
            con=get_connection()
            cursor=con.cursor()

            query="""update catalogue set catalogue_name = %s,catalogue_description = %s,start_date = %s,end_date = %s ,active = %s where catalogue_id = %s"""
            cursor.execute(query,(name,description,start_date,end_date,active,catalogue_id))
            con.commit()

            if cursor.rowcount == 0:
                raise CatalogueNotFoundError(catalogue_id)
            
            print("Catalogue updated successfully")

        except CatalogueNotFoundError as e:
            raise e
        except Exception as e:
            raise CatalogueUpdateError(catalogue_id)
        
        finally:
            if con:
                con.close()

    
    def delete_catalogue(self,catalogue_id):
        con = None
        try:
            con=get_connection()
            cursor=con.cursor()

            query="delete from catalogue where catalogue_id = %s"
            cursor.execute(query,(catalogue_id,))
            con.commit()

            if cursor.rowcount == 0:
                raise CatalogueDeleteError(catalogue_id)
            
            print("Catalogue deleted successfully")

        except CatalogueDeleteError as e:
            raise e
        except Exception as e:
            raise CatalogueError(f"Error for deleting {e}")
        
        finally:
            if con:
                con.close()

    def get_all_catalogue_json(self):
        con = None
        
        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute("SELECT * FROM catalogue")
            rows = cursor.fetchall()
            keys = ['catalogue_id', 'name', 'description', 'start_date', 'end_date', 'active']
            return [dict(zip(keys, row)) for row in rows]
        finally:
            con.close()

    def get_catalogue_json(self, catalogue_id):
        con = None
        
        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute("SELECT * FROM catalogue WHERE catalogue_id = %s", (catalogue_id,))
            row = cursor.fetchone()
            if not row:
                raise CatalogueNotFoundError(catalogue_id)
            keys = ['catalogue_id', 'name', 'description', 'start_date', 'end_date', 'active']
            return dict(zip(keys, row))
        finally:
            con.close()


    


    