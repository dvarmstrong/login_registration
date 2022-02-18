from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
import re 
from flask import flash



EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User:
    
    db_name = 'registration'
    
    
    def __init__(self,data):
        self.id = data['id']
        self.first_name= data['first_name']
        self.last_name= data['last_name']
        self.email= data['email']
        self.password = data['password']
        self.created_at= data['created_at']
        self.updated_at= data['updated_at']


    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, now(), now());"

        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) < 3:
            flash("Invalid First Name", "register")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Invalid Last Name", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email!", "register")
            is_valid = False 
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters","register")
            is_valid= False
        return is_valid


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db_name).query_db(query)

        all_users= []
        for row in results:
            #make user objects from the row in the tables
            user_object = cls(row)
            print(results)
            all_users.append(user_object)
        return all_users

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        # Checks to see if the email matches the user in database
        if len(results)< 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(results[0])
        

    


