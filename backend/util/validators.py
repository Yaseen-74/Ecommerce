from datetime import datetime
from backend.exception.exceptions import InvalidInputError

def validate_non_empty(field_name, value):
    if not value or str(value).strip() == "":
        raise InvalidInputError(f"{field_name} cannot be empty.")

def validate_date_format(field_name, date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise InvalidInputError(f"{field_name} must be in YYYY-MM-DD format.")

def validate_date_order(start_date, end_date):
    if start_date > end_date:
        raise InvalidInputError("Start date must be before end date.")

def validate_active_status(value):
    if value not in (0, 1):
        raise InvalidInputError("Active status must be 0 (inactive) or 1 (active).")
