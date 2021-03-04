from app import app
from flask import render_template, request, redirect, session, flash
import users
import plans
import recipes
import items
import shopping_lists


@app.route("/")
def index():
    user_id = users.get_user_id()
    if user_id:
        return redirect("/plan")
    else:
        return render_template("index.html")


@app.route("/error")
def error():
    return render_template("error.html")



############
### User ###
############

@app.route("/login", methods=["get","post"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username,password):
            return redirect("/")
        else:
            return render_template("error.html",message="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["get","post"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_check = request.form["password_check"]

        # Check that passwords are the same
        password_check = request.form["password_check"]
        if password != password_check:
            flash("Salasanat eivät ole samat")
            return redirect("/register")

        # Check password length
        if len(password) < 4:
            flash("Salasana on liian lyhyt")
            return redirect("/register")

        # Register user
        if users.register(username,password):
            flash("Rekisteröinti onnistui")
            return redirect("/")
        else:
            flash("Rekisteröinti ei onnistunut")
            return redirect("/register")

@app.route("/profile", methods=["get","post"])
def profile():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    username = users.get_username()

    if request.method == "GET":
        return render_template("profile.html",username=username)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Check that passwords are the same
        password_check = request.form["password_check"]
        if password != password_check:
            flash("Salasanat eivät ole samat")
            return redirect("/profile")

        # Check password length
        if len(password) < 4:
            flash("Salasana on liian lyhyt")
            return redirect("/profile")

        # Save profile data
        if users.update_profile(username,password):
            flash("Tiedot tallennettu")
        else:
            flash("Tietojen tallennus ei onnistunut")

    return redirect("/profile")

############
### Item ###
############

@app.route("/item", methods=["get"])
def item():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    username = users.get_username()

    # Store this page to the session history
    session["previous_page"] = "item"
    session["previous_page_url"] = "/item"

    query = request.args.get("query")
    if query == None:
        query = ''
    item_list = items.item_search(query)

    return render_template("item.html", username=username, items=item_list, number_of_items=len(item_list))

@app.route("/item_details/<int:id>", methods=["get"])
def item_modify(id):

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    username = users.get_username()

    item_id = id
    item = items.get_item(item_id)
    item_name = item[1]
    item_class = item[3]
    class_list = items.get_class_names()

    return render_template("item_details.html", username=username, item_id=item_id, item_name=item_name, item_class=item_class, class_list=class_list, number_of_classes=len(class_list))

@app.route("/item_save", methods=["post"])
def item_save():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    username = users.get_username()

    item_id = request.form["item_id"]
    item_name = request.form["item_name"]
    item_class = request.form["item_class"]
    items.item_change(item_id, item_name, item_class)

    return redirect("/item_details/"+str(item_id))

@app.route("/item_new", methods=["get"])
def item_new():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    username = users.get_username()

    class_list = items.get_class_names()

    return render_template("item_new.html", username=username, class_list=class_list, number_of_classes=len(class_list))


@app.route("/item_new_save", methods=["post"])
def item_new_save():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    username = users.get_username()

    item_name = request.form["item_name"]
    item_class = request.form["item_class"]
    item_id = items.item_new(item_name, item_class)

    return redirect("/item_new")

##################
### Item Class ###
##################

@app.route("/item_class", methods=["get"])
def item_class():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    username = users.get_username()

    item_class_list = items.get_item_classes()

    row_ids = []
    row_names = []
    for item_class in item_class_list:
        row_ids.append(item_class[0])
        row_names.append(item_class[1])

    return render_template("item_class.html", username=username, row_ids=row_ids, row_names=row_names, number_of_rows=len(row_ids))


@app.route("/item_class_move_up/<int:id>", methods=["post"])
def item_class_move_up(id):

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    username = users.get_username()

    result = items.item_class_move_up(id)

    return redirect("/item_class")


@app.route("/item_class_move_down/<int:id>", methods=["post"])
def item_class_move_down(id):

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    username = users.get_username()

    result = items.item_class_move_down(id)

    return redirect("/item_class")


##############
### Recipe ###
##############

@app.route("/recipe", methods=["get"])
def recipe():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    username = users.get_username()

    # Run search
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
    if id == recipes.get_default_recipe_id():
        return redirect("/")

    # Get recipe data from the database
    recipe_id = id
    recipe = recipes.get_recipe(recipe_id)
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

    return render_template("recipe_details.html", username=username, recipe_id=recipe_id, recipe_name=recipe_name, row_ids=row_ids, row_names=row_names, row_amounts=row_amounts, number_of_rows=len(row_ids), item_list=item_list, number_of_items=len(item_list))


@app.route("/recipe_save", methods=["post"])
def recipe_save():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    username = users.get_username()

    error = False

    # Save header
    recipe_id = request.form["recipe_id"]
    recipe_name = request.form["recipe_name"]
    if not recipes.save_header(recipe_id, recipe_name):
        error = True
        session["recipe_name"] = recipe_name
        flash("Reseptin nimen tallentaminen ei onnistunut")

    # Save rows
    error_rows = []
    number_of_rows = int(request.form["number_of_rows"])
    for i in range(number_of_rows):
        row_id = request.form[str(i) + "_row_id"]
        item_name = request.form[str(i) + "_row_name"]
        amount = request.form[str(i) + "_row_amount"]
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

    # Store form data to session (needed if form data is not saved before calling this action)
    recipe_id = request.form["recipe_id"]
    if not int(recipe_id) == recipes.get_default_recipe_id():
        session["recipe_name"] = request.form["recipe_name"]
    recipe_rows = []
    for i in range(int(request.form["number_of_rows"])):
        row_id = request.form[str(i) + "_row_id"]
        item_name = request.form[str(i) + "_row_name"]
        amount = request.form[str(i) + "_row_amount"]
        recipe_rows.append([row_id, item_name, amount])
    session["recipe_rows"] = recipe_rows    

    row_id = recipes.new_row(recipe_id)

    return redirect("/recipe_details/"+str(recipe_id))


@app.route("/recipe_delete_row/<int:id>", methods=["post"])
def recipe_delete_row(id):

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    username = users.get_username()

    # Store form data to session (needed if form data is not saved before calling this action)
    recipe_id = request.form["recipe_id"]
    if not int(recipe_id) == recipes.get_default_recipe_id():
        session["recipe_name"] = request.form["recipe_name"]
    recipe_rows = []
    for i in range(int(request.form["number_of_rows"])):
        row_id = request.form[str(i) + "_row_id"]
        item_name = request.form[str(i) + "_row_name"]
        amount = request.form[str(i) + "_row_amount"]
        recipe_rows.append([row_id, item_name, amount])
    session["recipe_rows"] = recipe_rows    

    # Delete row
    result = recipes.delete_row(recipe_id, id)

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

    recipe_id = request.form["recipe_id"]
    row_id = id

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
    
    # Add new recipe header
    recipe_name = request.form["recipe_name"]
    recipe_id = recipes.new_recipe(recipe_name)
    if not recipe_id:
        flash("Reseptin luonti ei onnistunut")
        return redirect("/recipe_new")

    # Add 3 black rows to the new recipe
    for i in range(3):
        recipes.new_row(recipe_id)

    return redirect("/recipe_details/"+str(recipe_id))

