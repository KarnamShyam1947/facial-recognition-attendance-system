import email
from werkzeug.security import check_password_hash, generate_password_hash
from dotenv import dotenv_values
import mysql.connector

secrets = dotenv_values(".env")

login_query = "SELECT * FROM users WHERE email = %s"
add_user_query = "INSERT INTO users(name, email, password, role) VALUES(%s, %s, %s, %s)"

config = {
    "host": secrets['DB_HOST_URL'],
    "port": secrets['DB_PORT'],
    "database": secrets['DB_DATABASE'],
    "user": secrets['DB_USERNAME'],
    "password": secrets['DB_PASSWORD'],
    "charset": "utf8",
    "use_unicode": True,
    "get_warnings": True,
}

def login(email, password):
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor(dictionary=True)

    cur.execute(login_query, (email, ))
    result = cur.fetchone()
    
    cur.close()
    cnx.close()

    if result is None:
        return None
    
    hashed_pw = result['password']
    if not check_password_hash(hashed_pw, password):
        return None
    
    return result

def add_user(name, email, password, role):
    password = generate_password_hash(password)
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor(dictionary=True)

    cur.execute(login_query, (email, ))
    result = cur.fetchone()
    
    if result:
        cur.close()
        cnx.close()
        return None
    
    else:
        cur.execute(add_user_query, (name, email, password, role, ))
        cnx.commit()

        cur.close()
        cnx.close()

        return True
    
def add_faculty(name, email, password):
    return add_user(name, email, password, "FACULTY")

def add_student(name, email, password):
    return add_user(name, email, password, "STUDENT")

if __name__ == "__main__":
    name = "faculty1"
    email = "f1@gmail.com"
    password = "faculty1"
    
    # r = add_faculty(name, email, password)

    r = login(email, password)

    print(r)
    