from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username,password):
    sql = "SELECT password, id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        return False
    else:
        if check_password_hash(user[0],password):
            session["user_id"] = user[1]
            return True
        else:
            return False

def logout():
    del session["user_id"]

def register(username,password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username,password) VALUES (:username,:password)"
        db.session.execute(sql, {"username":username,"password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username,password)

def get_user_id():
    return session.get("user_id",0)

def get_username():
    user_id = get_user_id()
    sql = "SELECT username FROM users WHERE id=:id"
    result = db.session.execute(sql, {"id":user_id})
    username = result.fetchone()
    if username == None:
        return False
    else:
        return username[0]

def update_profile(username,password):
    user_id = get_user_id()
    hash_value = generate_password_hash(password)
    try:
        sql = "UPDATE users SET username=:username, password=:password WHERE id=:id"
        db.session.execute(sql, {"username":username,"password":hash_value,"id":user_id})
        db.session.commit()
    except:
        db.session.rollback()
        return False
    return True

