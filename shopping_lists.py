from db import db
from flask import session
import plans
import recipes


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
            recipe_rows = recipes.get_recipe_rows(recipe_id) # RR.id, RR.item_id, item_name, RR.amount
            for recipe_row in recipe_rows:
                shopping_list_rows.append([recipe_row[1], recipe_row[2], recipe_row[3]])

    # Combine same items to one row
    shopping_list_rows.sort()
    shopping_list_combined = []
    for i in range(len(shopping_list_rows)):
        if i < len(shopping_list_rows)-1 and shopping_list_rows[i][0] == shopping_list_rows[i+1][0]:
            shopping_list_rows[i+1] = combine_rows(shopping_list_rows[i], shopping_list_rows[i+1])
        else:
            shopping_list_combined.append(shopping_list_rows[i])

    return shopping_list_combined

def combine_rows(row_1, row_2):
    combined_row = [row_1[0], row_1[1], ""]

    if row_1[2] == "":
        combined_row[2] = row_2[2]
    elif row_2[2] == "":
        combined_row[2] = row_1[2]
    else:
        combined_row[2] = row_1[2] + " + " + row_2[2]
    
    return combined_row

