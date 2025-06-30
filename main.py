from backend.services.catalogue_service import CatalogueService
from backend.exception.exceptions import CatalogueError,CatalogueDateExpired,CatalogueDeleteError,CatalogueNotFoundError,CatalogueUpdateError
from datetime import datetime
from backend.util.validators import validate_active_status,validate_date_format,validate_date_order,validate_non_empty

def main():
    service = CatalogueService()

    while True:
        print("\n=== Catalogue Management ===")
        print("1. Create Catalogue")
        print("2. Get Catalogue by ID")
        print("3. Update Catalogue by ID")
        print("4. Delete Catalogue by ID")
        print("5. Get All Catalogues")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            while True:
                try:
                    n_input = input("\nHow many catalogues do you want to add: ").strip()
                    if not n_input:
                        raise ValueError("WARNING! Input cannot be empty.")
                    if not n_input.isdigit():
                        raise ValueError("WARNING! Please enter digits only.")
                    n = int(n_input)
                    break
                except ValueError as e:
                    print(e)

            for i in range(n):
                print(f"\nEnter details for Catalogue {i + 1}")

            
                while True:
                    try:
                        name = input("Enter catalogue name: ").strip()
                        if not name:
                            raise ValueError("WARNING! Name cannot be empty.")
                        if not name.replace(" ", "").isalpha():
                            raise ValueError("WARNING! Name must contain only letters.")
                        break
                    except Exception as e:
                        print(e)

                
                while True:
                    try:
                        description = input("Enter catalogue description: ").strip()
                        if not description:
                            raise ValueError("WARNING! Description cannot be empty.")
                        if not description.replace(" ", "").isalpha():
                            raise ValueError("WARNING! Description must contain only letters.")
                        break
                    except Exception as e:
                        print(e)

            
                while True:
                    try:
                        start_date_str = input("Enter start date (YYYY-MM-DD): ").strip()
                        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
                        break
                    except ValueError:
                        print("WARNING! Invalid start date format. Use YYYY-MM-DD.")

                
                while True:
                    try:
                        end_date_str = input("Enter end date (YYYY-MM-DD): ").strip()
                        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
                        if start_date > end_date:
                            raise ValueError("Start date must be before end date.")
                        break
                    except ValueError as e:
                        print("WARNING!", e)

                
                while True:
                    try:
                        active_input = input("Is catalogue active? (1 for yes, 0 for no): ").strip()
                        if not active_input:
                            raise ValueError("Active status cannot be empty.")
                        if active_input not in ("0", "1"):
                            raise ValueError("Active must be 0 or 1.")
                        active = int(active_input)
                        break
                    except ValueError as e:
                        print("WARNING!", e)

                
                try:
                    service.create_catalogue(name, description, start_date, end_date, active)
                    print(f"Catalogue {i + 1} created successfully.")
                except Exception as e:
                    print(f" Failed to save catalogue {i + 1}: {e}")

        elif choice == '2':
            try:
                catalogue_id = int(input("\nEnter catalogue ID: "))
                service.get_catalogue(catalogue_id)
            except CatalogueNotFoundError as e:
                print(f"ERROR : {e}")
            except Exception as e:
                print(f"ERROR: {e}")


        elif choice == '3':
            while True:
                try:
                    catalogue_id_input = input("Enter catalogue ID to update: ").strip()
                    if not catalogue_id_input:
                        raise ValueError("Catalogue ID cannot be empty")
                    if not catalogue_id_input.isdigit():
                        raise ValueError("Catalogue ID must be integer")
                    catalogue_id = int(catalogue_id_input)
                    
                    service.get_catalogue(catalogue_id)
                    break
                
                except CatalogueNotFoundError as e:
                    print(f"Error : {e}")
                    return
                except ValueError as e:
                    print(e)
                except Exception as e:
                    print(e)
                
            while True:
                try:
                    name = input("Enter new catalogue name: ").strip()
                    if not name:
                        raise ValueError("WARNING! Name cannot be empty.")
                    if not name.replace(" ", "").isalpha():
                        raise ValueError("WARNING! Name must contain only letters.")
                    break
                except Exception as e:
                    print(e)

            while True:
                try:
                    description = input("Enter new catalogue description: ").strip()
                    if not description:
                        raise ValueError("WARNING! Description cannot be empty.")
                    if not description.replace(" ", "").isalpha():
                        raise ValueError("WARNING! Description must contain only letters.")
                    break
                except Exception as e:
                    print(e)
        
            while True:
                try:
                    start_date_str = input("Enter new start date (YYYY-MM-DD): ").strip()
                    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
                    break
                except ValueError:
                    print("WARNING! Invalid start date format. Use YYYY-MM-DD.")
            while True:
                try:
                    end_date_str = input("Enter new end date (YYYY-MM-DD): ").strip()
                    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
                    if start_date > end_date:
                        raise ValueError("Start date must be before end date.")
                    break
                except ValueError as e:
                    print("WARNING!", e)


            while True:
                try:
                    active_input = input("Is new catalogue is active? (1 for yes, 0 for no): ").strip()
                    if not active_input:
                        raise ValueError("Active status cannot be empty.")
                    if active_input not in ("0", "1"):
                        raise ValueError("Active must be 0 or 1.")
                    active = int(active_input)
                    break
                except ValueError as e:
                    print("WARNING!", e)

            try:
                service.update_catalogue(catalogue_id, name, description, start_date, end_date, active)
            except CatalogueError as e:
                print(f"[{e.error_code}] {e}")
            except Exception as e:
                print(f"error:{e}")




        elif choice == '4':
            while True:
                try:
                    catalogue_id_input = input("Enter catalogue ID to update: ").strip()
                    if not catalogue_id_input:
                        raise ValueError("Catalogue ID cannot be empty")
                    if not catalogue_id_input.isdigit():
                        raise ValueError("Catalogue ID must be integer")
                    catalogue_id = int(catalogue_id_input)
                    service.delete_catalogue(catalogue_id)
                    break

                except CatalogueNotFoundError as e:
                    print(f"ERROR : {e}")
                except Exception as e:
                    print(f"ERROR : {e}")

        elif choice == '5':
            try:
                service.get_all_catalogue()
            except Exception as e:
                print(f"ERROR :{e}")

        elif choice == '0':
            print("Exiting... Goodbye!")
            break

        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
