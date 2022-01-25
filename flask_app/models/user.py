from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.recipe import Recipe
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self, data):
        self.id=data['id']
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.email=data['email']
        self.password=data['password']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.recipes=[]


    @classmethod
    def create(cls, data):
        query="INSERT INTO users (first_name, last_name, email, password, created_at, updated_at)"\
            "VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW())"
        result=connectToMySQL('recipes_schema').query_db(query, data)
        return result


    @classmethod
    def get_one(cls, data):
        query="SELECT * FROM users "\
            "LEFT JOIN recipes ON users.id=recipes.user_id "\
            "WHERE users.id=%(id)s;"
        results=connectToMySQL('recipes_schema').query_db(query, data)
        user=cls(results[0])
        if results[0]['recipes.id']!=None:
            for row in results:
                row_data={
                    'id':row['recipes.id'],
                    'name':row['name'],
                    'description':row['description'],
                    'under_over':row['under_over'],
                    'instructions':row['instructions'],
                    'date_made':row['date_made'],
                    'created_at':row['recipes.created_at'],
                    'updated_at':row['recipes.updated_at']
                }
                user.recipes.append(Recipe(row_data))
        return user


    @classmethod
    def get_by_email(cls, data):
        query="SELECT * FROM users WHERE email=%(email)s;"
        result=connectToMySQL('recipes_schema').query_db(query, data)
        print(result)
        if len(result)<1:
            return False
        return cls(result[0])


    @staticmethod
    def validate(data):
        is_valid=True

        if 'first_name' not in data:
            flash('*Please enter a first name', 'register_errors')
            is_valid=False
        elif len(data['first_name'])<2:
            flash('*First name must be at least two characters', 'register_errors')
            is_valid=False

        if 'last_name' not in data:
            flash('*Please enter a last name', 'register_errors')
            is_valid=False
        elif len(data['last_name'])<2:
            flash('*Last name must be at least two characters', 'register_errors')
            is_valid=False

        if 'email' not in data:
            flash('*Please enter an email address', 'register_errors')
            is_valid=False
        elif not EMAIL_REGEX.match(data['email']):
            flash('*Invalid email address', 'register_errors')
            is_valid=False
        elif User.get_by_email(data):
            flash(f"*{data['email']} is already in use on this site", 'register_errors')
            is_valid=False

        if 'password' not in data:
            flash('*Please enter a password', 'register_errors')
            is_valid=False
        elif 'confirm_password' not in data:
            flash('*Please confirm your password', 'register_errors')
            is_valid=False
        elif len(data['password'])<8:
            flash('*Passwords must be at least eight characters', 'register_errors')
            is_valid=False
        elif data['password']!=data['confirm_password']:
            flash('*Passwords do not match', 'register_errors')
            is_valid=False

        return is_valid