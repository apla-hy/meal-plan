from app import app
from flask import render_template, request, redirect, session, flash
import users
import recipes
import items

@app.route("/recipe", methods=["get"])
def recipe():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    username = users.get_username()

    # Execute search (empty search query returns all lists)
    query = request.args.get("query")
    if query == None:
        query = ''
    recipe_list = recipes.recipe_search(query)

    return render_template("recipe.html",username=username, recipes=recipe_list, number_of_recipes=len(recipe_list))


@app.route("/recipe_details/<int:id>", methods=["get"])
def recipe_details(id):

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    username = users.get_username()

    # Check that recipe is not the default recipe (modification is not allowed)
    recipe_id = id
    if recipe_id == recipes.get_default_recipe_id():
        return redirect("/")

    # Get recipe data from the database
    recipe = recipes.get_recipe(recipe_id)
    if not recipe:
        return redirect("/error")
    recipe_name = recipe[1]
    recipe_rows = recipes.get_recipe_rows(recipe_id)
    row_ids = []
    row_names = []
    row_amounts = []
    for recipe_row in recipe_rows:
        row_ids.append(recipe_row[0])
        row_names.append(recipe_row[2])
        row_amounts.append(recipe_row[3])
    item_list = items.get_item_names()

    # If session contains recipe data, use it (there was an error in saving this data)
    if "recipe_name" in session:
        recipe_name = session["recipe_name"]
        del session["recipe_name"]

    if "recipe_rows" in session:
        for recipe_row in session["recipe_rows"]:
            if int(recipe_row[0]) in row_ids:
                index = row_ids.index(int(recipe_row[0]))
                row_ids[index] = recipe_row[0]
                row_names[index] = recipe_row[1]
                row_amounts[index] = recipe_row[2]
        del session["recipe_rows"]

    return render_template("recipe_details.html", username=username, recipe_id=recipe_id, recipe_name=recipe_name, row_ids=row_ids, \
        row_names=row_names, row_amounts=row_amounts, number_of_rows=len(row_ids), item_list=item_list, number_of_items=len(item_list))


@app.route("/recipe_save", methods=["post"])
def recipe_save():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    username = users.get_username()

    # Validate header data
    try:
        recipe_id = int(request.form["recipe_id"])
        recipe_name = request.form["recipe_name"]
        number_of_rows = int(request.form["number_of_rows"])
    except:
        return redirect("/error")
    if len(recipe_name) == 0:
        flash("Nimi ei voi olla tyhjä")
        return redirect("/recipe_details/"+str(recipe_id))
    if len(recipe_name) > 50:
        flash("Nimen pituus ei voi olla yli 50 merkkiä")
        return redirect("/recipe_details/"+str(recipe_id))

    error = False
    # Save header
    if not recipes.save_header(recipe_id, recipe_name):
        error = True
        session["recipe_name"] = recipe_name
        flash("Reseptin nimen tallentaminen ei onnistunut")
    # Save rows
    error_rows = []
    for i in range(number_of_rows):
        try:
            row_id = request.form[str(i) + "_row_id"]
            item_name = request.form[str(i) + "_row_name"]
            amount = request.form[str(i) + "_row_amount"]
        except:
            return redirect("/error")
        if len(item_name) > 50:
            flash("Nimikkeen nimi on liian pitkä")
            return redirect("/recipe_details/"+str(recipe_id))
        if len(amount) > 50:
            flash("Määrä on liian pitkä")
            return redirect("/recipe_details/"+str(recipe_id))
        if not recipes.save_row(row_id, item_name, amount):
            error = True
            error_rows.append([row_id, item_name, amount])
            flash("Rivin " + item_name + " tallentaminen ei onnistunut")
    if len(error_rows) > 0:
        session["recipe_rows"] = error_rows

    if not error:
        flash("Resepti tallennettu")

    return redirect("/recipe_details/"+str(recipe_id))

@app.route("/recipe_add_row", methods=["post"])
def recipe_add_row():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    username = users.get_username()

    # Validate form data
    try:
        recipe_id = int(request.form["recipe_id"])
        recipe_name = request.form["recipe_name"]
    except:
        return redirect("/error")
    if len(recipe_name) > 50:
        flash("Reseptin nimi on liian pitkä")
        return redirect("/recipe_details/"+str(recipe_id))

    # Store form data to session (needed if form data is not saved before calling this action)
    if not recipe_id == recipes.get_default_recipe_id():
        session["recipe_name"] = recipe_name
    recipe_rows = []
    for i in range(int(request.form["number_of_rows"])):
        try:
            row_id = request.form[str(i) + "_row_id"]
            item_name = request.form[str(i) + "_row_name"]
            amount = request.form[str(i) + "_row_amount"]
        except:
             return redirect("/error")
        recipe_rows.append([row_id, item_name, amount])
    session["recipe_rows"] = recipe_rows    

    if not recipes.new_row(recipe_id):
        flash("Rivin lisääminen ei onnistunut")
    else:
        flash("Rivi lisätty")

    return redirect("/recipe_details/"+str(recipe_id))


@app.route("/recipe_delete_row/<int:id>", methods=["post"])
def recipe_delete_row(id):

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    username = users.get_username()

    # Validate form data
    try:
        delete_row_id = int(id)
        recipe_id = int(request.form["recipe_id"])
        recipe_name = request.form["recipe_name"]
    except:
        return redirect("/error")
    if len(recipe_name) > 50:
        flash("Reseptin nimi on liian pitkä")
        return redirect("/recipe_details/"+str(recipe_id))

    # Store form data to session (needed if form data is not saved before calling this action)
    if not recipe_id == recipes.get_default_recipe_id():
        session["recipe_name"] = recipe_name
    recipe_rows = []
    for i in range(int(request.form["number_of_rows"])):
        try:
            row_id = request.form[str(i) + "_row_id"]
            item_name = request.form[str(i) + "_row_name"]
            amount = request.form[str(i) + "_row_amount"]
        except:
             return redirect("/error")
        recipe_rows.append([row_id, item_name, amount])
    session["recipe_rows"] = recipe_rows    

    # Delete row
    if not recipes.delete_row(recipe_id, delete_row_id):
        flash("Rivin poisto ei onnistunut")
    else:
        flash("Rivi poistettu")

    return redirect("/recipe_details/"+str(recipe_id))    


@app.route("/item_new_from_recipe", methods=["get"])
def item_new_from_recipe():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    username = users.get_username()

    # Store recipe details page to the session history
    recipe_id = request.args.get("recipe_id")
    if recipe_id != None:
        session["previous_page"] = "recipe"
        session["previous_page_url"] = "/recipe_details/" + str(recipe_id)

    # Open add items page
    return redirect("/item_new")


@app.route("/item_modify_from_recipe/<int:id>", methods=["post"])
def item_modify_from_recipe(id):

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    username = users.get_username()

    # Validate form data
    try:
        recipe_id = int(request.form["recipe_id"])
        row_id = int(id)
    except:
        return redirect("/error")

    # Store recipe details page to the session history
    session["previous_page"] = "recipe"
    session["previous_page_url"] = "/recipe_details/" + str(recipe_id)

    # Get item id based on the list row
    recipe_row = recipes.get_recipe_row(recipe_id, row_id)
    item_id = recipe_row[1]

    # Check that item is not the default item (changing this item is not allowed)
    if items.is_default_item(item_id):
        flash("Valittua nimikettä ei voi muokata")
        return redirect("/recipe_details/" + str(recipe_id))

    # Open change item page
    return redirect("/item_details/" + str(item_id))


@app.route("/recipe_new", methods=["get"])
def recipe_new():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    username = users.get_username()

    return render_template("recipe_new.html", username=username)

@app.route("/recipe_new_save", methods=["post"])
def recipe_new_save():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    username = users.get_username()

    # Validate form data
    try:
        recipe_name = request.form["recipe_name"]
    except:
        return redirect("/error")
    if len(recipe_name) > 50:
        flash("Reseptin nimi on liian pitkä")
        return redirect("/recipe_new")
    if len(recipe_name) == 0:    
        flash("Reseptin nimi ei voi olla tyhjä")
        return redirect("/recipe_new")

    # Add new recipe header
    recipe_id = recipes.new_recipe(recipe_name)
    if not recipe_id:
        flash("Reseptin luonti ei onnistunut")
        return redirect("/recipe_new")

    # Add 3 black rows to the new recipe
    for i in range(3):
        recipes.new_row(recipe_id)

    return redirect("/recipe_details/"+str(recipe_id))

