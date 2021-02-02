from db import db
from flask import session

def get_recipes():
    sql = "SELECT name, id FROM recipes ORDER BY id"
    result = db.session.execute(sql)
    recipes = result.fetchall()
    return recipes

def get_recipe_names():
    recipes = get_recipes()
    recipe_list = []
    for recipe in recipes:
        recipe_list.append(recipe[0])
    recipe_list.sort()
    return recipe_list
    

