users_db = {
    "john@company.com": {"name": "John Doe", "status": "active", "password": "old_password_123"},
    "jane@company.com": {"name": "Jane Smith", "status": "active", "password": "secure_pass_456"}
}

def get_all_users():
    return users_db

def get_user(email: str):
    return users_db.get(email)

def reset_password(email: str, new_password: str):
    if email in users_db:
        users_db[email]["password"] = new_password
        return True
    return False

def create_user(email: str, name: str, password: str):
    if email not in users_db:
        users_db[email] = {"name": name, "status": "active", "password": password}
        return True
    return False