import datetime
from time import sleep

def date(input_date):
    """Validates if the input is a date in YYYY-MM-DD format."""
    try:
        datetime.strptime(input_date, '%Y-%m-%d')
        return True
    except ValueError:
        print("\nTanggal tidak valid. Gunakan format YYYY-MM-DD")
        sleep(0.5)
        return False

def numeric(input_value, min_value=None, max_value=None):
    """Checks if the input is a number, optionally within a specified range."""
    try:
        value = float(input_value)
        if min_value is not None and value < min_value:
            print(f"\nNilai harus lebih besar atau sama dengan {min_value}")
            return False
        if max_value is not None and value > max_value:
            print(f"\nNilai harus lebih kecil atau sama dengan {max_value}")
            return False
        return True
    except ValueError:
        return False

