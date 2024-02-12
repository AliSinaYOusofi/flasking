
import bcrypt

def hash_password(password):
    try:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    except Exception as e:
        print(e, ' Error Bro')
        return None