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
    
def recipe_search(query):
    sql = "SELECT id, name FROM recipes WHERE LOWER(name) LIKE LOWER(:query) ORDER BY name"
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    recipes = result.fetchall()
    return recipes

def get_recipe(recipe_id):
    sql = "SELECT id, name FROM recipes WHERE id=:recipe_id"
    result = db.session.execute(sql, {"recipe_id":recipe_id})
    recipe = result.fetchone()
    return recipe

def get_recipe_rows(recipe_id):
    sql = "SELECT RR.id, RR.item_id, I.name AS item_name, RR.amount FROM recipe_rows RR LEFT JOIN items I ON RR.item_id=I.id WHERE RR.recipe_id=:recipe_id ORDER BY RR.id"
    result = db.session.execute(sql, {"recipe_id":recipe_id})
    recipe_rows = result.fetchall()
    return recipe_rows

def save_header(recipe_id, recipe_name):
    sql = "UPDATE recipes SET name=:name WHERE id=:recipe_id"
    db.session.execute(sql, {"recipe_id":recipe_id, "name":recipe_name})
    db.session.commit()

    return True

def save_row(row_id, item_name, amount):

    # Find id for the item
    sql = "SELECT id FROM items WHERE name=:name"
    result = db.session.execute(sql, {"name":item_name})
    item_id = result.fetchone()
    if item_id == None:
        print("Virhe: valittua nimikettä ei löydy")
        return False
    else:
        item_id = item_id[0]

    # Update recipe row data to the database
    sql = "UPDATE recipe_rows SET amount=:amount, item_id=:item_id WHERE id=:row_id"
    
    db.session.execute(sql, {"row_id":row_id, "item_id":item_id, "amount":amount})
    db.session.commit()

    return True

def new_row(recipe_id):
    sql = "INSERT INTO recipe_rows (recipe_id, item_id, amount) VALUES (:recipe_id, 1, '')"
    db.session.execute(sql, {"recipe_id":recipe_id})
    db.session.commit()

    return True

def delete_row(row_id):
    sql = "DELETE FROM recipe_rows WHERE id=:row_id"
    db.session.execute(sql, {"row_id":row_id})
    db.session.commit()

    return True
    


