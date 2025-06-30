class Catalogue:
   

    def __init__(self,catalogue_id,catalogue_name,catalogue_description,start_date,end_date,active=True):
        self.catlogue_id=catalogue_id
        self.name=catalogue_name
        self.description=catalogue_description
        self.start_date=start_date
        self.end_date=end_date
        self.status=active

    def display_info(self):
        print("\n---CATALOGUE LIST----")
        print(f"\nID ={self.catlogue_id}")
        print(f"NAME = {self.name}")
        print(f"DESCRIPTION = {self.description}")
        print(f"START_DATE = {self.start_date}")
        print(f"END_DATE = {self.end_date}")
        print(f"ACTIVE ={self.status}")

