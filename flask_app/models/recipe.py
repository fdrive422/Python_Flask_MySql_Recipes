from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import datetime

class Recipe:
    def __init__(self, data):
        self.id=data['id']
        self.name=data['name']
        self.description=data['description']
        self.under_over=data['under_over']
        self.instructions=data['instructions']
        self.date_made=data['date_made'].date()
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        if 'user_id' in data:
            self.user=data['user_id']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        results =  connectToMySQL("recipes_schema").query_db(query)
        all_recipes = []
        for row in results:
            print(row['date_made'])
            all_recipes.append( cls(row) )
        return all_recipes

    @classmethod
    def get_one(cls, data):

        query="SELECT * FROM recipes WHERE id=%(id)s;"
        result=connectToMySQL('recipes_schema').query_db(query, data)
        print(result)
        return cls(result[0])

    @classmethod
    def create(cls, data):
        query="INSERT INTO recipes (name, description, instructions, under_over, date_made, user_id, created_at, updated_at)"\
            "VALUES (%(name)s, %(description)s, %(instructions)s, %(under_over)s, %(date_made)s, %(user_id)s, NOW(), NOW())"
        result=connectToMySQL('recipes_schema').query_db(query, data)
        return result

    @classmethod
    def delete(cls, data):
        query="DELETE FROM recipes "\
            "WHERE id=%(id)s;"
        result=connectToMySQL('recipes_schema').query_db(query, data)
        return result

    @classmethod
    def update(cls, data):
        query="UPDATE recipes "\
            "SET name=%(name)s, description=%(description)s, "\
            "instructions=%(instructions)s, under_over=%(under_over)s, "\
            "date_made=%(date_made)s, updated_at=NOW() "\
            "WHERE id=%(id)s;"
        result=connectToMySQL('recipes_schema').query_db(query, data)
        return result

    @staticmethod
    def validate(data):
        is_valid=True

        if 'name' not in data:
            flash('*Please enter a name for your recipe', 'create_errors')
            is_valid=False
        elif len(data['name'])<3:
            flash('*Name must be at least three characters', 'create_errors')
            is_valid=False

        if 'description' not in data:
            flash('*Please enter a description for your recipe', 'create_errors')
            is_valid=False
        elif len(data['description'])<3:
            flash('*Description must be at least three characters', 'create_errors')
            is_valid=False

        if 'instructions' not in data:
            flash('*Please enter instructions for your recipe', 'create_errors')
            is_valid=False
        elif len(data['instructions'])<3:
            flash('*Instructions must be at least three characters', 'create_errors')
            is_valid=False

        if 'under_over' not in data:
            flash('*Must select a valid checkbox', 'create_errors')
            is_valid=False
        elif data['under_over']!='0' and data['under_over']!='1':
            flash('*Must select a valid checkbox', 'create_errors')
            is_valid=False

        if 'date_made' not in data:
            flash('*Please enter the date made for your recipe', 'create_errors')
            is_valid=False
        elif len(data['date_made'])!=10:
            flash('*Please enter a valid date', 'create_errors')
            is_valid=False

        return is_valid