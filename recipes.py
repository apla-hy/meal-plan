from db import db
from flask import session
import items

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
        if recipe[0] != "":
            recipe_list.append(recipe[0] + " (valmis)")
    recipe_list.sort()
    return recipe_list

def get_default_recipe_id():
    sql = "SELECT id FROM recipes WHERE default_recipe=1"
    result = db.session.execute(sql)
    recipe_id = result.fetchone()
    return recipe_id[0]

def recipe_search(query):
    sql = "SELECT id, name FROM recipes WHERE LOWER(name) LIKE LOWER(:query) AND default_recipe=0 ORDER BY name"
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    recipes = result.fetchall()
    return recipes

def get_recipe(recipe_id):
    sql = "SELECT id, name FROM recipes WHERE id=:recipe_id"
    result = db.session.execute(sql, {"recipe_id":recipe_id})
    recipe = result.fetchone()
    return recipe

def get_recipe_rows(recipe_id):
    sql = "SELECT RR.id, RR.item_id, I.name AS item_name, RR.amount FROM recipe_rows RR LEFT JOIN items I ON RR.item_id=I.id \
        WHERE RR.recipe_id=:recipe_id ORDER BY RR.id"
    result = db.session.execute(sql, {"recipe_id":recipe_id})
    recipe_rows = result.fetchall()
    return recipe_rows

def get_recipe_row(recipe_id, row_id):
    sql = "SELECT RR.id, RR.item_id, I.name AS item_name, RR.amount FROM recipe_rows RR LEFT JOIN items I ON RR.item_id=I.id \
       WHERE RR.recipe_id=:recipe_id AND RR.id=:row_id ORDER BY RR.id"
    result = db.session.execute(sql, {"recipe_id":recipe_id, "row_id":row_id})
    recipe_row = result.fetchone()
    return recipe_row

def get_recipe_rows_with_classes(recipe_id):
    sql = "SELECT RR.id, RR.item_id, I.name AS item_name, RR.amount, IC.id, IC.name FROM recipe_rows RR LEFT JOIN items I ON RR.item_id=I.id \
        LEFT JOIN item_classes IC ON I.class_id=IC.id WHERE RR.recipe_id=:recipe_id ORDER BY RR.id"
    result = db.session.execute(sql, {"recipe_id":recipe_id})
    recipe_rows = result.fetchall()
    return recipe_rows

def save_header(recipe_id, recipe_name):
    try:
        sql = "UPDATE recipes SET name=:name WHERE id=:recipe_id"
        db.session.execute(sql, {"recipe_id":recipe_id, "name":recipe_name})
        db.session.commit()
    except:
        db.session.rollback()
        return False
    return True
        

def save_row(row_id, item_name, amount):

    # Find id for the item
    sql = "SELECT id FROM items WHERE name=:name"
    result = db.session.execute(sql, {"name":item_name})
    item_id = result.fetchone()
    if item_id == None:
        return False
    else:
        item_id = item_id[0]

    # Update recipe row data to the database
    try:
        sql = "UPDATE recipe_rows SET amount=:amount, item_id=:item_id WHERE id=:row_id"
        db.session.execute(sql, {"row_id":row_id, "item_id":item_id, "amount":amount})
        db.session.commit()
    except:
        db.session.rollback()
        return False

    return True

def new_row(recipe_id):
    item_id = items.get_default_item_id()
    try:
        sql = "INSERT INTO recipe_rows (recipe_id, item_id, amount) VALUES (:recipe_id, :item_id, '') RETURNING id"
        result = db.session.execute(sql, {"recipe_id":recipe_id, "item_id":item_id})
        row_id = result.fetchone()[0]
        db.session.commit()
    except:
        db.session.rollback()
        return False

    return row_id

def delete_row(recipe_id, row_id):
    try:
        sql = "DELETE FROM recipe_rows WHERE recipe_id=:recipe_id AND id=:row_id"
        db.session.execute(sql, {"recipe_id":recipe_id, "row_id":row_id})
        db.session.commit()
    except:
        db.session.rollback()
        return False
    return True

def new_recipe(recipe_name):
    try:
        sql = "INSERT INTO recipes (name, default_recipe) VALUES (:name, 0) RETURNING id"
        result = db.session.execute(sql, {"name":recipe_name})
        recipe_id = result.fetchone()[0]
        db.session.commit()
    except:
        db.session.rollback()
        return False
    return recipe_id

    


