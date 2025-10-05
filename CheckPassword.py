import re

def check_password_strength(password: str):
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password): 
        return False
    if not re.search(r"[0-9]", password): 
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

    
if __name__ == "__main__":
    pwd = input("Enter your password: ")

    if check_password_strength(pwd):
        print("Strong password!")
    else:
        print("Weak password. Please include at least 8 chars, uppercase, lowercase, digit, and special character.")
