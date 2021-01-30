from db import db
from flask import session

def get_recipes():
    sql = "SELECT name FROM recipes ORDER BY name"
    result = db.session.execute(sql)
    recipes = result.fetchall()
    recipe_list = []
    for recipe in recipes:
        recipe_list.append(recipe[0])
    return recipe_list

