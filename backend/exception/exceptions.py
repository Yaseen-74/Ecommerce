class CatalogueError(Exception):
    error_code="Catalogue Error"
    
    def __init__(self,message="Error in Catalogue"):
        self.message=message
        super().__init__(self.message)

class InvalidInputError(CatalogueError):
    error_code="Invalid Input"

    def __init__(self, message="Invalid Input"):
        super().__init__(message)
        
class CatalogueNotFoundError(CatalogueError):
    error_code="Catalogue Not Found"

    def __init__(self,catalogue_id):
        self.catalogue_id=catalogue_id
        self.message=f"in this Catalogue {self.catalogue_id}"
        super().__init__(self.message)

    def __str__(self):
        return f"{self.error_code} {self.message}"

class CatalogueUpdateError(CatalogueError):
    error_code="Catalogue Update Failed"

    def __init__(self,catalogue_id):
        self.catalogue_id=catalogue_id
        self.message=f"in this catalogue{self.catalogue_id}"
        super().__init__(self.message)

    def __str__(self):
        return f"{self.error_code} {self.message}"
    
class CatalogueDeleteError(CatalogueError):
    error_code="Catalogue Delete Failed"

    def __init__(self,catalogue_id):
        self.catalogue_id=catalogue_id
        self.message=f"in this catalogue {self.catalogue_id}"
        super().__init__(self.message)

    def __str__(self):
        return f"{self.error_code} {self.message}"

class CatalogueDateExpired(CatalogueError):
    error_code="Catalogue Data is Expired"

    def __init__(self,catalogue_name):
        self.name=catalogue_name
        self.message=f" in this {catalogue_name}"
        super().__init__(self.message)

    def __str__(self):
        return f"{self.error_code}{self.message}"
    
class DatabaseConnectorError(CatalogueError):
    error_code = "Database Connection Error"

    def __init__(self, message=" in Catalogue Connection"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"[{self.error_code}] {self.message}"


