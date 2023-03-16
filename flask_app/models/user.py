from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL 
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:

    db='ripened_tomatoes'
    def __init__(self, data):
        self.id = data['id']     
        self.first_name = data['first_name'] 
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password'] 
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        

    @staticmethod
    def validate_user(user):
    
        is_valid = True
        if len(user['first_name'])<1:
            flash("First name is required!","reg")
            is_valid = False
        if len(user['last_name'])<1:
            flash("Last name is required!","reg")
            is_valid = False
        if 0<len(user['first_name'])<2:
            flash("First name is invalid!", "reg")
            is_valid = False
        if 0<len(user['last_name'])<2:
            flash("Last name is invalid!","reg")
            is_valid = False
        if len(user['email'])<1:
            flash("Email is required!","reg")
            is_valid = False
        if User.get_by_email(user['email']) != None:
            flash("Email is already registered!","reg")
            is_valid = False 
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!","reg")
            is_valid = False
        if len(user['password'])<8:
            flash ("Password must be at least 8 characters!","reg")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Passwords do not match!","reg")
            is_valid = False
    
        return is_valid
         

# CREATE - SQL
    @classmethod
    def save (cls, data):
        query = """INSERT INTO users (first_name, last_name, email,password)
                VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);"""
        result=connectToMySQL(cls.db).query_db(query,data)
        return result

    @classmethod
    def get_all(cls):
        query="SELECT * FROM users;"
        results=connectToMySQL(cls.db).query_db(query)
        users=[]
        for result in results:
            users.append(cls(result))
        return users
        

    @classmethod
    def get_by_email(cls, email):
        query = "SELECT * FROM users WHERE email= %(email)s;"
        result=connectToMySQL(cls.db).query_db(query,{'email':email})
        return result[0] if result else None

    @classmethod
    def delete_user(cls,data):
        query="DELETE FROM users WHERE id=%(id)s;"
        result=connectToMySQL(cls.db).query_db(query,data)
        return result


    

