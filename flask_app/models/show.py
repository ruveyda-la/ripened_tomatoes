from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL 
from flask import flash
from flask_app.models.user import User

class Show():
    db='ripened_tomatoes'
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.release_date = data['release_date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.added_by=None

    @classmethod
    def get_all_shows(cls):
        query="SELECT * FROM shows LEFT JOIN users ON shows.user_id=users.id;"
        results=connectToMySQL(cls.db).query_db(query)
        shows=[]
        for result in results:
            data={
                'id':result['users.id'],
                'first_name':result['first_name'],
                'last_name':result['last_name'],
                'email':result['email'],
                'password':result['password'],
                'created_at':result['users.created_at'],
                'updated_at':result['users.updated_at']
            }
            show=cls(result)
            show.added_by=User(data)
            shows.append(show)
        return shows

    @staticmethod
    def validate_show(show):
        is_valid = True
        if len(show['title'])<1:
            flash("Show title is required!")
            is_valid = False
        if len(show['description'])<1:
            flash("Description is required!")
            is_valid = False
        if 0<len(show['title'])<2:
            flash("Show title is invalid!")
            is_valid = False
        if 0<len(show['description'])<2:
            flash("Description is invalid!")
            is_valid = False
        if len(show['release_date']) == '':
            flash("Please select a date!")
            is_valid = False
        if Show.get_by_title(show['title']) != None:
            flash("This show already exists!")
            is_valid = False 
    
        return is_valid

    @classmethod
    def get_by_title(cls, title):
        query = "SELECT * FROM shows WHERE title= %(title)s;"
        result=connectToMySQL(cls.db).query_db(query,{'title':title})
        return result[0] if result else None

    @classmethod
    def save (cls, data):
        query = """INSERT INTO shows (title,description,release_date,user_id)
                VALUES (%(title)s,%(description)s,%(release_date)s,%(user_id)s);"""
        result=connectToMySQL(cls.db).query_db(query,data)
        return result

    @classmethod
    def get_show_by_id(cls, id):
        query = "SELECT * FROM shows WHERE id= %(id)s;"
        result=connectToMySQL(cls.db).query_db(query,id)
        return result[0]  

    @classmethod
    def update_show(cls,data):
        query = "UPDATE  shows SET title=%(title)s, description=%(description)s, release_date=%(release_date)s WHERE id= %(id)s;"
        result=connectToMySQL(cls.db).query_db(query,data)
        return result

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM shows WHERE id=%(id)s"
        result = connectToMySQL(cls.db).query_db(query,data)
        return result



    

        