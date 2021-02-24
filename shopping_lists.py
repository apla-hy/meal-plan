from db import db
from flask import session
import plans
import items
import recipes


def list_search(query):
    sql = "SELECT id, name FROM shopping_lists WHERE LOWER(name) LIKE LOWER(:query) AND default_list=0 ORDER BY name"
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    lists = result.fetchall()
    return lists

def get_list(list_id):
    sql = "SELECT id, name FROM shopping_lists WHERE id=:list_id"
    result = db.session.execute(sql, {"list_id":list_id})
    s_list = result.fetchone()
    return s_list

def get_list_rows(list_id):
    sql = "SELECT R.id, R.item_id, I.name AS item_name, R.amount, R.marked, IC.id AS class_id, IC.name AS class_name FROM shopping_list_rows R LEFT JOIN items I ON R.item_id=I.id LEFT JOIN item_classes IC ON I.class_id=IC.id WHERE R.shopping_list_id=:list_id ORDER BY IC.class_order, I.name"
    result = db.session.execute(sql, {"list_id":list_id})
    list_rows = result.fetchall()
    return list_rows
  
def get_list_row(list_id, row_id):
    sql = "SELECT R.id, R.item_id, I.name AS item_name, R.amount, R.marked FROM shopping_list_rows R LEFT JOIN items I ON R.item_id=I.id WHERE R.shopping_list_id=:list_id AND R.id=:row_id"
    result = db.session.execute(sql, {"list_id":list_id, "row_id":row_id})
    list_row = result.fetchone()
    return list_row

def new_list_from_plan(selected_recipes):

    # Find ids for the selected recipes
    recipe_ids = []
    recipe_list = recipes.get_recipes() # name, id
    for selected_recipe in selected_recipes:
        for recipe in recipe_list:
            if selected_recipe == recipe[0]:
                recipe_ids.append(recipe[1]) 
                break

    # Add all needed items to the shopping list
    shopping_list_rows = []
    default_recipe_id = recipes.get_default_recipe_id()
    for recipe_id in recipe_ids:
        if recipe_id != default_recipe_id:
            recipe_rows = recipes.get_recipe_rows_with_classes(recipe_id) # RR.id, RR.item_id, item_name, RR.amount, class_id, class_name
            for recipe_row in recipe_rows:
                shopping_list_rows.append([recipe_row[1], recipe_row[3], 0]) # item_id, amount, marked 

    # Combine same items to one row
    shopping_list_combined = remove_duplicate_rows(shopping_list_rows)

    return shopping_list_combined

def get_default_list(user_id):
    # Check if there is a default list already
    sql = "SELECT id FROM shopping_lists WHERE user_id=:user_id AND default_list=1"
    result = db.session.execute(sql, {"user_id":user_id})
    list_id = result.fetchone()
    # If not, create default plan
    if list_id == None:
        sql = "INSERT INTO shopping_lists (user_id, default_list, name) VALUES (:user_id,1, '') RETURNING id"
        result = db.session.execute(sql, {"user_id":user_id})
        list_id = result.fetchone()
        db.session.commit()
    return list_id[0]


def add_items_from_list(list_id, item_list):

    # Get current list rows
    sql = "SELECT item_id, amount, marked FROM shopping_list_rows WHERE shopping_list_id=:list_id"
    result = db.session.execute(sql, {"list_id":list_id})
    list_rows = result.fetchall()
    
    # Add all needed items to the shopping list
    shopping_list_rows = []
    for list_row in list_rows:
        shopping_list_rows.append([ list_row[0], list_row[1], list_row[2] ])
    for item in item_list:
        shopping_list_rows.append([item[0], item[1], 0])

    # Combine same items to one row
    shopping_list_combined = remove_duplicate_rows(shopping_list_rows)

    return shopping_list_combined
    

def save_list_rows(list_id, list_rows):

    # Delete old rows
    sql = "DELETE FROM shopping_list_rows WHERE shopping_list_id=:list_id"
    result = db.session.execute(sql, {"list_id":list_id})
    db.session.commit()

    # Add new rows
    sql = "INSERT INTO shopping_list_rows (shopping_list_id, item_id, amount, marked) VALUES (:list_id, :item_id, :amount, :marked)"
    for row in list_rows:
        result = db.session.execute(sql, {"list_id":list_id, "item_id":row[0], "amount":row[1], "marked":row[2]})
        db.session.commit()
    
    return True


def mark_row(list_id, row_id):

    # Check if the row is currently marked or not
    sql = "SELECT marked FROM shopping_list_rows WHERE shopping_list_id=:list_id AND id=:row_id"
    result = db.session.execute(sql, {"list_id":list_id, "row_id":row_id})
    row_marked = result.fetchone()[0]
    mark_value = 1
    if row_marked:
        mark_value = 0

    try:
        sql = "UPDATE shopping_list_rows SET marked=:mark_value WHERE shopping_list_id=:list_id AND id=:row_id"
        db.session.execute(sql, {"list_id":list_id, "row_id":row_id, "mark_value":mark_value})
        db.session.commit()
    except:
        return False
    return True


def delete_row(list_id, row_id):

    try:
        sql = "DELETE FROM shopping_list_rows WHERE shopping_list_id=:list_id AND id=:row_id"
        db.session.execute(sql, {"list_id":list_id, "row_id":row_id})
        db.session.commit()
    except:
        return False
    return True


def save_header(list_id, list_name):
    try:
        sql = "UPDATE shopping_lists SET name=:name WHERE id=:list_id"
        db.session.execute(sql, {"list_id":list_id, "name":list_name})
        db.session.commit()
    except:
        return False
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

    # Update shopping list row data to the database
    sql = "UPDATE shopping_list_rows SET amount=:amount, item_id=:item_id WHERE id=:row_id"
    db.session.execute(sql, {"row_id":row_id, "item_id":item_id, "amount":amount})
    db.session.commit()

    return True

def new_row(list_id):
    item_id = items.get_default_item_id()
    sql = "INSERT INTO shopping_list_rows (shopping_list_id, item_id, amount) VALUES (:list_id, :item_id, '', 0) RETURNING id"
    result = db.session.execute(sql, {"list_id":list_id, "item_id":item_id})
    row_id = result.fetchone()[0]
    db.session.commit()

    return row_id

def new_list(user_id, list_name):
    try:
        sql = "INSERT INTO shopping_lists (user_id, default_list, name) VALUES (:user_id, 0, :name) RETURNING id"
        result = db.session.execute(sql, {"user_id":user_id, "name":list_name})
        list_id = result.fetchone()[0]
        db.session.commit()
    except:
        db.session.rollback()
        return False
    return list_id


def save_default_list_with_name(user_id, list_name):
    default_list_id = get_default_list(user_id)
    list_id = new_list(user_id, list_name)
    if not list_id:
        return False
    list_rows = get_list_rows(default_list_id) # Row.id, Row.item_id, Item.name, Row.amount, Row.marked
    for list_row in list_rows:
            sql = "INSERT INTO shopping_list_rows (shopping_list_id, item_id, amount, marked) VALUES (:list_id, :item_id, :amount, :marked) RETURNING id"
            result = db.session.execute(sql, {"list_id":list_id, "item_id":list_row[1], "amount":list_row[3], "marked":list_row[4]})
            row_id = result.fetchone()[0]
            db.session.commit()
     
    return list_id
    

def remove_duplicate_rows(shopping_list_rows):
    shopping_list_rows.sort()
    shopping_list_combined = []
    for i in range(len(shopping_list_rows)):
        if i < len(shopping_list_rows)-1 and shopping_list_rows[i][0] == shopping_list_rows[i+1][0]:
            shopping_list_rows[i+1] = combine_rows(shopping_list_rows[i], shopping_list_rows[i+1])
        else:
            shopping_list_combined.append(shopping_list_rows[i])

    return shopping_list_combined

def combine_rows(row_1, row_2):

    combined_row = [row_1[0], "", 0]

    # Combine amount
    if row_1[1] == "":
        combined_row[1] = row_2[1]
    elif row_2[1] == "":
        combined_row[1] = row_1[1]
    else:
        combined_row[1] = row_1[1] + " + " + row_2[1]
    
    return combined_row

