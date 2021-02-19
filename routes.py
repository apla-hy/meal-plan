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

### Plan ###

@app.route("/plan")
def plan():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    username = users.get_username()

    plan_id = plans.get_default_plan(user_id)
    startdate = plans.get_startdate(plan_id)
    period = plans.get_period(plan_id)
    planning_dates = plans.get_planning_dates(startdate, period)
    weekdays = []
    dates = []
    for planning_date in planning_dates:
        weekdays.append(plans.get_weekday(planning_date.weekday()))
        dates.append(planning_date.strftime("%d.%m.%Y"))
    recipe_list = recipes.get_recipe_names()
    notes = plans.get_notes(plan_id)
    selected_recipes = plans.get_selected_recipes(plan_id)

    return render_template("plan.html", username=username, plan_id=plan_id, startdate=startdate, period=period, dates=dates, weekdays=weekdays, recipes=recipe_list, selected_recipes=selected_recipes, notes=notes)

@app.route("/plan_change_date", methods=["post"])
def plan_change_date():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    username = users.get_username()

    # Change the start date
    plans.set_startdate(request.form["plan_id"], request.form["startdate"])

    return redirect("/plan")

@app.route("/plan_change_period", methods=["post"])
def plan_change_period():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    username = users.get_username()

    # Change pediod
    plans.set_period(request.form["plan_id"], request.form["period"])

    return redirect("/plan")

@app.route("/plan_save_rows", methods=["post"])
def plan_save_rows():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    username = users.get_username()

    # Save rows
    plan_id = request.form["plan_id"]
    startdate = plans.get_startdate(plan_id)
    period = plans.get_period(plan_id)
    
    for i in range(period):
        plan_row_number = i
        selected_recipes = []
        for j in range(3):
            selected_recipes.append(request.form[str(i) + "_" + str(j)])
        notes = request.form[str(i) + "_notes"]
        plans.save_row(plan_id, startdate, plan_row_number, selected_recipes, notes)        

    return redirect("/plan")

@app.route("/plan_create_shopping_list", methods=["post"])
def plan_create_shopping_list():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    username = users.get_username()

    # Collect data from the form
    plan_id = request.form["plan_id"]
    startdate = plans.get_startdate(plan_id)
    period = plans.get_period(plan_id)

    selected_recipes = []
    for i in range(period):
        for j in range(3):
            selected_recipes.append(request.form[str(i) + "_" + str(j)])

    # Create shopping list
    list_rows = shopping_lists.new_list_from_plan(selected_recipes)
    
    # Save shopping list to the database
    list_id = shopping_lists.get_default_list(user_id)
    save_result = shopping_lists.save_list_rows(list_id, list_rows)

    return redirect("/shopping_list_details/"+str(list_id))


@app.route("/plan_show_default_shopping_list", methods=["post"])
def plan_show_default_shopping_list():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    username = users.get_username()

    list_id = shopping_lists.get_default_list(user_id)

    return redirect("/shopping_list_details/"+str(list_id))


#####################
### Shopping list ###
#####################

@app.route("/shopping_list", methods=["get"])
def shopping_list():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    username = users.get_username()

    query = request.args.get("query")
    if query == None:
        query = ''
    lists = shopping_lists.list_search(query)

    return render_template("shopping_list.html",username=username, lists=lists, number_of_lists=len(lists))

@app.route("/shopping_list_details/<int:id>", methods=["get"])
def shopping_list_details(id):

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    username = users.get_username()

    # Get shopping list data from the database
    list_id = id
    default_list = False
    default_list_id = shopping_lists.get_default_list(user_id)
    if list_id == default_list_id:
        default_list = True

    list_data = shopping_lists.get_list(list_id)
    list_name = list_data[1]
    list_rows = shopping_lists.get_list_rows(list_id)
    row_ids = []
    row_names = []
    row_amounts = []
    row_marks = []
    for list_row in list_rows:
        row_ids.append(list_row[0])
        row_names.append(list_row[2])
        row_amounts.append(list_row[3])
        row_marks.append(list_row[4])
    item_list = items.get_item_names()

    # If session contains shopping list data, use it (there was an error in saving this data)
    if "list_name" in session:
        list_name = session["list_name"]
        del session["list_name"]

    if "list_rows" in session:
        for list_row in session["list_rows"]:
            if int(list_row[0]) in row_ids:
                index = row_ids.index(int(list_row[0]))
                row_ids[index] = list_row[0]
                row_names[index] = list_row[1]
                row_amounts[index] = list_row[2]
        del session["list_rows"]

    return render_template("shopping_list_details.html", username=username, list_id=list_id, list_name=list_name, default_list=default_list, row_ids=row_ids, row_names=row_names, row_amounts=row_amounts, row_marks=row_marks, number_of_rows=len(row_ids), item_list=item_list, number_of_items=len(item_list))

@app.route("/shopping_list_save", methods=["post"])
def shopping_list_save():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    username = users.get_username()

    error = False

    # Save header
    list_id = request.form["list_id"]
    default_list_id = shopping_lists.get_default_list(user_id)
    if not int(list_id) == default_list_id:
        list_name = request.form["list_name"]
        if not shopping_lists.save_header(list_id, list_name):
            error = True
            session["list_name"] = list_name
            flash("Listan nimen tallentaminen ei onnistunut")

    # Save rows
    error_rows = []
    number_of_rows = int(request.form["number_of_rows"])
    for i in range(number_of_rows):
        row_id = request.form[str(i) + "_row_id"]
        item_name = request.form[str(i) + "_row_name"]
        amount = request.form[str(i) + "_row_amount"]
        if not shopping_lists.save_row(row_id, item_name, amount):
            error = True
            error_rows.append([row_id, item_name, amount])
            flash("Rivin " + item_name + " tallentaminen ei onnistunut")
    if len(error_rows) > 0:
        session["list_rows"] = error_rows

    if not error:
        flash("Muutokset tallennettu")

    return redirect("/shopping_list_details/"+str(list_id))

@app.route("/shopping_list_mark_row/<int:id>", methods=["post"])
def shopping_list_mark_row(id):

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    username = users.get_username()

    # Store form data to session (needed if form data is not saved before calling this action)
    list_id = request.form["list_id"]
    if not int(list_id) == shopping_lists.get_default_list(user_id):
        session["list_name"] = request.form["list_name"]
    list_rows = []
    for i in range(int(request.form["number_of_rows"])):
        row_id = request.form[str(i) + "_row_id"]
        item_name = request.form[str(i) + "_row_name"]
        amount = request.form[str(i) + "_row_amount"]
        list_rows.append([row_id, item_name, amount])
    session["list_rows"] = list_rows    

    # Toggle row mark
    result = shopping_lists.mark_row(list_id, id)

    return redirect("/shopping_list_details/"+str(list_id))    


@app.route("/shopping_list_add_row", methods=["post"])
def shopping_list_add_row():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    username = users.get_username()

    # Store form data to session (needed if form data is not saved before calling this action)
    list_id = request.form["list_id"]
    if not int(list_id) == shopping_lists.get_default_list(user_id):
        session["list_name"] = request.form["list_name"]
    list_rows = []
    for i in range(int(request.form["number_of_rows"])):
        row_id = request.form[str(i) + "_row_id"]
        item_name = request.form[str(i) + "_row_name"]
        amount = request.form[str(i) + "_row_amount"]
        list_rows.append([row_id, item_name, amount])
    session["list_rows"] = list_rows    

    # Add row
    row_id = shopping_lists.new_row(list_id)

    return redirect("/shopping_list_details/"+str(list_id))



@app.route("/shopping_list_delete_row/<int:id>", methods=["post"])
def shopping_list_delete_row(id):

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    username = users.get_username()

    # Store form data to session (needed if form data is not saved before calling this action)
    list_id = request.form["list_id"]
    if not int(list_id) == shopping_lists.get_default_list(user_id):
        session["list_name"] = request.form["list_name"]
    list_rows = []
    for i in range(int(request.form["number_of_rows"])):
        row_id = request.form[str(i) + "_row_id"]
        item_name = request.form[str(i) + "_row_name"]
        amount = request.form[str(i) + "_row_amount"]
        list_rows.append([row_id, item_name, amount])
    session["list_rows"] = list_rows    

    # Delete row
    result = shopping_lists.delete_row(list_id, id)

    return redirect("/shopping_list_details/"+str(list_id))    


@app.route("/item_new_from_shopping_list", methods=["get"])
def item_new_from_shopping_list():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    username = users.get_username()

    # Store shopping list details page to the session history
    list_id = request.args.get("list_id")
    if list_id != None:
        session["previous_page"] = "shopping_list"
        session["previous_page_url"] = "/shopping_list_details/" + str(list_id)

    # Open add items page
    return redirect("/item_new")

@app.route("/item_modify_from_shopping_list//<int:id>", methods=["post"])
def item_modify_from_shopping_list(id):

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    username = users.get_username()

    list_id = request.form["list_id"]
    row_id = id

    # Store shopping list details page to the session history
    session["previous_page"] = "shopping_list"
    session["previous_page_url"] = "/shopping_list_details/" + str(list_id)

    # Get item id based on the list row
    list_row = shopping_lists.get_list_row(list_id, row_id)
    item_id = list_row[1]

    # Check that item is not the default item (changing this item is not allowed)
    if items.is_default_item(item_id):
        flash("Tyhjää nimikettä ei voi muokata")
        return redirect("/shopping_list_details/" + str(list_id))

    # Open change item page
    return redirect("/item_details/" + str(item_id))


@app.route("/shopping_list_new", methods=["get"])
def shopping_list_new():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    username = users.get_username()

    return render_template("shopping_list_new.html", username=username)


@app.route("/shopping_list_new_save", methods=["post"])
def shopping_list_new_save():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    username = users.get_username()
    
    # Add new shopping list header
    list_name = request.form["shopping_list_name"]
    list_id = shopping_lists.new_list(user_id, list_name)
    if not list_id:
        flash("Ostoslistan luonti ei onnistunut")
        return redirect("/shopping_list_new")

    # Add 3 black rows to the new shopping list
    for i in range(3):
        shopping_lists.new_row(list_id)

    return redirect("/shopping_list_details/"+str(list_id))


### User ###

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
        if users.register(username,password):
            return redirect("/")
        else:
            return render_template("error.html",message="Rekisteröinti ei onnistunut")

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
        if users.update_profile(username,password):
            return redirect("/")
        else:
            return render_template("error.html",username=username, message="Tietojen tallannus ei onnistunut")

### Item ###

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

### Recipe ###

@app.route("/recipe", methods=["get"])
def recipe():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    username = users.get_username()

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

    recipe_id = request.form["recipe_id"]
    row_id = recipes.new_row(recipe_id)

    return redirect("/recipe_details/"+str(recipe_id))

@app.route("/recipe_delete_row", methods=["post"])
def recipe_delete_row():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    username = users.get_username()

    recipe_id = request.form["recipe_id"]
    number_of_rows = int(request.form["number_of_rows"])

    # Loop all rows and delete the selected ones
    for i in range(number_of_rows):
        row_id = int(request.form.get(str(i) + "_selected", default='0'))
        if row_id != 0:
            recipes.delete_row(row_id)

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

@app.route("/item_modify_from_recipe", methods=["post"])
def item_modify_from_recipe():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    username = users.get_username()

    recipe_id = request.form["recipe_id"]
    number_of_rows = int(request.form["number_of_rows"])

    # Loop all rows and find the first selected row
    selected_row = 0
    for i in range(number_of_rows):
        row_id = int(request.form.get(str(i) + "_selected", default='0'))
        if row_id != 0:
            selected_row = row_id
            break

    # If no row selected
    if selected_row == 0:
        flash("Riviä ei ole valittu")
        return redirect("/recipe_details/" + str(recipe_id))

    # Store recipe details page to the session history
    if recipe != None:
        session["previous_page"] = "recipe"
        session["previous_page_url"] = "/recipe_details/" + str(recipe_id)

    # Get item id based on the recipe row
    recipe_row = recipes.get_recipe_row(recipe_id, selected_row)
    item_id = recipe_row[1]

    # Check that item is not the default item (changing this item is not allowed)
    if items.is_default_item(item_id):
        flash("Tyhjää nimikettä ei voi muokata")
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

