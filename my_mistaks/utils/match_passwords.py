import bcrypt

def match_passwords(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)