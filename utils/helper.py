from datetime   import datetime ,timedelta

def is_key_expired(expiration_time):
    if expiration_time < datetime.now():
        return True
    return False

