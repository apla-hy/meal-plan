from app import app
from flask import render_template, request, redirect, session, flash
import users
import items
import shopping_lists

@app.route("/shopping_list", methods=["get"])
def shopping_list():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")

    # Set scroll position to the beginning of the page
    session["scroll_pos"] = 0

    # Execute search (empty search query returns all lists)
    query = request.args.get("query")
    if not query:
        query = ''
    lists = shopping_lists.list_search(user_id, query)

    # Show page
    return render_template("shopping_list.html", lists=lists, number_of_lists=len(lists))

@app.route("/shopping_list_details/<int:id>", methods=["get"])
def shopping_list_details(id):

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")

    # Check shopping list owner
    list_id = id
    if not shopping_lists.is_list_owner(user_id, list_id):
        return redirect("/error")

    # Get shopping list data from the database 
    default_list = False
    default_list_id = shopping_lists.get_default_list(user_id)
    if list_id == default_list_id:
        default_list = True

    list_data = shopping_lists.get_list(list_id)
    if not list_data:
        return redirect("/error")
    list_name = list_data[1]
    list_rows = shopping_lists.get_list_rows(list_id)
    row_ids = []
    row_names = []
    row_amounts = []
    row_marks = []
    row_class_names = []
    for list_row in list_rows:
        row_ids.append(list_row[0])
        row_names.append(list_row[2])
        row_amounts.append(list_row[3])
        row_marks.append(list_row[4])
        row_class_names.append(list_row[6])
    item_list = items.get_item_names()

    # Get list of saved shopping lists
    saved_lists = shopping_lists.list_search(user_id, "")

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

    # Show page
    return render_template("shopping_list_details.html", list_id=list_id, list_name=list_name, default_list=default_list, \
        row_ids=row_ids, row_names=row_names, row_amounts=row_amounts, row_marks=row_marks, row_class_names=row_class_names, \
        number_of_rows=len(row_ids), item_list=item_list, number_of_items=len(item_list), saved_lists=saved_lists)

@app.route("/shopping_list_save", methods=["post"])
def shopping_list_save():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")

    # Check csrf
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    # Save scroll position to the session data
    session["scroll_pos"] = request.form["scroll_pos"]

    # Validate header data
    try:
        list_id = int(request.form["list_id"])
    except:
        return redirect("/error")
    try:
        number_of_rows = int(request.form["number_of_rows"])
    except:
        return redirect("/error")

    # Save header if not default list
    error = False
    default_list_id = shopping_lists.get_default_list(user_id)
    if not list_id == default_list_id:
        list_name = request.form["list_name"]
        if len(list_name) > 50:
            flash("Ostoslistan nimen pituus ei voi olla yli 50 merkkiä")
            return redirect("/shopping_list_details/"+str(list_id))
        if len(list_name) == 0:
            flash("Ostoslistan nimi ei voi olla tyhjä")
            return redirect("/shopping_list_details/"+str(list_id))
        if not shopping_lists.save_header(list_id, list_name):
            error = True
            session["list_name"] = list_name
            flash("Listan nimen tallentaminen ei onnistunut")

    # Save rows
    error_rows = []
    for i in range(number_of_rows):
        row_id = request.form[str(i) + "_row_id"]
        item_name = request.form[str(i) + "_row_name"]
        if len(item_name) > 50:
            error = True
            flash("Kentän nimike pituus on liian suuri")
            break
        amount = request.form[str(i) + "_row_amount"]
        if len(amount) > 100:
            error = True
            flash("Kentän määrä pituus on liian suuri")
            break
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
    # Check csrf
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    # Save scroll position to the session data
    session["scroll_pos"] = request.form["scroll_pos"]

    # Validate data
    try:
        list_row_id = int(id)
    except:
        return redirect("/error")
    try:
        list_id = int(request.form["list_id"])
    except:
        return redirect("/error")
    try:
        number_of_rows = int(request.form["number_of_rows"])
    except:
        return redirect("/error")

    # Store form data to session (needed if form data is not saved before calling this action)
    if not list_id == shopping_lists.get_default_list(user_id):
        list_name = request.form["list_name"]
        if len(list_name) > 50:
            flash("Ostoslistan nimen pituus ei voi olla yli 50 merkkiä")
            return redirect("/shopping_list_details/"+str(list_id))
        session["list_name"] = list_name
    list_rows = []
    for i in range(number_of_rows):
        row_id = request.form[str(i) + "_row_id"]
        item_name = request.form[str(i) + "_row_name"]
        amount = request.form[str(i) + "_row_amount"]
        if len(item_name) < 50 and len(amount) < 100:
            list_rows.append([row_id, item_name, amount])
    session["list_rows"] = list_rows    

    # Toggle row mark
    shopping_lists.mark_row(list_id, list_row_id)

    return redirect("/shopping_list_details/"+str(list_id))    


@app.route("/shopping_list_add_row", methods=["post"])
def shopping_list_add_row():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    # Check csrf
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    # Set scroll position to the beginning of the page
    session["scroll_pos"] = 0

    # Validate data
    try:
        list_id = int(request.form["list_id"])
    except:
        return redirect("/error")
    try:
        number_of_rows = int(request.form["number_of_rows"])
    except:
        return redirect("/error")
    if number_of_rows > 299:
        flash("Lisäys ei onnistunut. Rivejä voi olla enintään 300.")
        return redirect("/shopping_list_details/"+str(list_id))

    # Store form data to session (needed if form data is not saved before calling this action)
    if not list_id == shopping_lists.get_default_list(user_id):
        list_name = request.form["list_name"]
        if len(list_name) > 50:
            flash("Ostoslistan nimen pituus ei voi olla yli 50 merkkiä")
            return redirect("/shopping_list_details/"+str(list_id))
        session["list_name"] = list_name
    list_rows = []
    for i in range(number_of_rows):
        row_id = request.form[str(i) + "_row_id"]
        item_name = request.form[str(i) + "_row_name"]
        amount = request.form[str(i) + "_row_amount"]
        if len(item_name) < 50 and len(amount) < 100:
            list_rows.append([row_id, item_name, amount])
    session["list_rows"] = list_rows    

    # Add row
    if not shopping_lists.new_row(list_id):
        flash("Rivin lisäys ei onnistunut")

    return redirect("/shopping_list_details/"+str(list_id))


@app.route("/shopping_list_delete_row/<int:id>", methods=["post"])
def shopping_list_delete_row(id):

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    # Check csrf
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    # Save scroll position to the session data
    session["scroll_pos"] = request.form["scroll_pos"]

    # Validate data
    try:
        list_row_id = int(id)
    except:
        return redirect("/error")
    try:
        list_id = int(request.form["list_id"])
    except:
        return redirect("/error")
    try:
        number_of_rows = int(request.form["number_of_rows"])
    except:
        return redirect("/error")

    # Store form data to session (needed if form data is not saved before calling this action)
    if not list_id == shopping_lists.get_default_list(user_id):
        list_name = request.form["list_name"]
        if len(list_name) > 50:
            flash("Ostoslistan nimen pituus ei voi olla yli 50 merkkiä")
            return redirect("/shopping_list_details/"+str(list_id))
        session["list_name"] = list_name
    list_rows = []
    for i in range(number_of_rows):
        row_id = request.form[str(i) + "_row_id"]
        item_name = request.form[str(i) + "_row_name"]
        amount = request.form[str(i) + "_row_amount"]
        if len(item_name) < 50 and len(amount) < 100:
            list_rows.append([row_id, item_name, amount])
    session["list_rows"] = list_rows    

    # Delete row
    if not shopping_lists.delete_row(list_id, list_row_id):
        flash("Rivin poisto ei onnistunut")

    return redirect("/shopping_list_details/"+str(list_id))


@app.route("/shopping_list_add_from_list", methods=["get","post"])
def shopping_list_add_from_list():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    # Check csrf
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)

    # Set scroll position to the beginning of the page
    session["scroll_pos"] = 0

    # Get list ids from form (case POST) or session (case GET)
    if request.method == "GET":
        if "list_add_from_id" in session:
            list_add_from_id = session["list_add_from_id"]
            del session["list_add_from_id"]
        else:
            return redirect("/error")
        if "list_add_to_id" in session:
            list_add_to_id = session["list_add_to_id"]
            del session["list_add_to_id"]
        else:
            return redirect("/error")
    if request.method == "POST":
        try:
            list_add_from_id = request.form["list_add_from_id"]
            list_add_to_id = request.form["list_add_to_id"]
        except:
            return redirect("/error")

    # Get 'all rows selected' status from the session data (by default all rows are selected)
    rows_selected_value = 1
    if "list_rows_selected" in session:
        if session["list_rows_selected"] == 0:
            rows_selected_value = 0
            del session["list_rows_selected"]

    # Get shopping list data from the database
    list_rows = shopping_lists.get_list_rows(list_add_from_id)
    row_checked = []
    row_ids = []
    row_item_ids = []
    row_names = []
    row_amounts = []
    row_class_names = []
    for list_row in list_rows:
        row_checked.append(rows_selected_value)
        row_ids.append(list_row[0])
        row_item_ids.append(list_row[1])
        row_names.append(list_row[2])
        row_amounts.append(list_row[3])
        row_class_names.append(list_row[6])

    # Show page
    return render_template("shopping_list_add_from_list.html", list_add_to_id=list_add_to_id, \
        list_add_from_id=list_add_from_id, row_checked=row_checked, row_ids=row_ids, row_item_ids=row_item_ids, \
        row_names=row_names, row_amounts=row_amounts, row_class_names=row_class_names, number_of_rows=len(row_ids))


@app.route("/shopping_list_add_from_list_select_rows", methods=["post"])
def shopping_list_add_from_list_select_rows():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    # Check csrf
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    # Validate form data
    try:
        list_add_from_id = int(request.form["list_add_from_id"])
        list_add_to_id = int(request.form["list_add_to_id"])
    except:
        return redirect("/error")

    # Store list ids to session
    session["list_add_from_id"] = list_add_from_id
    session["list_add_to_id"] = list_add_to_id

    # Store selected status to session
    session["list_rows_selected"] = 1

    return redirect("/shopping_list_add_from_list")


@app.route("/shopping_list_add_from_list_unselect_rows", methods=["post"])
def shopping_list_add_from_list_unselect_rows():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    # Check csrf
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    # Validate form data
    try:
        list_add_from_id = int(request.form["list_add_from_id"])
        list_add_to_id = int(request.form["list_add_to_id"])
    except:
        return redirect("/error")

    # Store list ids to session
    session["list_add_from_id"] = list_add_from_id
    session["list_add_to_id"] = list_add_to_id

    # Store selected status to session
    session["list_rows_selected"] = 0

    return redirect("/shopping_list_add_from_list")


@app.route("/shopping_list_add_from_list_save", methods=["post"])
def shopping_list_add_from_list_save():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
       return redirect("/")
    # Check csrf
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    # Validate from data
    try:
        list_id = int(request.form["list_add_to_id"])
        number_of_rows = int(request.form["number_of_rows"])
    except:
        return redirect("/error")

    # Loop all rows and store data from the selected rows
    item_list = []
    for i in range(number_of_rows):
        row_id = int(request.form.get(str(i) + "_selected", default='0'))
        if row_id != 0:
            item_id = int(request.form.get(str(i) + "_row_item_id", default='0'))
            amount = request.form.get(str(i) + "_row_amount", default='')
            if item_id != 0:
                item_list.append([item_id, amount])

    # Add selected rows to the shopping list if some rows are selected
    if len(item_list) != 0:
        # Add rows to the target shopping list
        list_rows = shopping_lists.add_items_from_list(list_id, item_list)
        if not list_rows:
            flash("Rivien lisäys ei onnistunut. Ostoslistalla voi olla enintään 300 riviä.")
            return redirect("/shopping_list_details/"+str(list_id))

        # Save the new version of the shopping list to the database
        if shopping_lists.save_list_rows(list_id, list_rows):
            flash("Rivit lisätty")
        else:
            flash("Rivien lisäys ei onnistunut")

    return redirect("/shopping_list_details/"+str(list_id))


@app.route("/item_new_from_shopping_list", methods=["get"])
def item_new_from_shopping_list():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")

    # Set scroll position to the beginning of the page
    session["scroll_pos"] = 0

    # Store shopping list details page to the session history
    list_id = request.args.get("list_id")
    if list_id != None:
        session["previous_page"] = "shopping_list"
        session["previous_page_url"] = "/shopping_list_details/" + str(list_id)

    # Open add items page
    return redirect("/item_new")

@app.route("/item_modify_from_shopping_list/<int:id>", methods=["post"])
def item_modify_from_shopping_list(id):

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    # Check csrf
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    # Save scroll position to the session data
    session["scroll_pos"] = request.form["scroll_pos"]

    # Validate form data
    try:
        list_id = int(request.form["list_id"])
        row_id = int(id)
    except:
        return redirect("/error")

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

    # Open page to get name for the new list
    return render_template("shopping_list_new.html")


@app.route("/shopping_list_new_save", methods=["post"])
def shopping_list_new_save():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    # Check csrf
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    # Validate form data
    try:
        list_name = request.form["shopping_list_name"]
    except:
        return redirect("/error")
    if len(list_name) > 30:
        flash("Nimi on liian pitkä")
        return redirect("/shopping_list_new")                    
    
    # Add new shopping list header
    list_id = shopping_lists.new_list(user_id, list_name)
    if not list_id:
        flash("Ostoslistan luonti ei onnistunut")
        return redirect("/shopping_list_new")

    # Add 3 blank rows to the new shopping list
    for i in range(3):
        shopping_lists.new_row(list_id)

    return redirect("/shopping_list_details/"+str(list_id))


@app.route("/shopping_list_new_from_default", methods=["get"])
def shopping_list_new_from_default():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")

    default_list_id =  shopping_lists.get_default_list(user_id)

    return render_template("shopping_list_new_from_default.html", default_list_id=default_list_id)


@app.route("/shopping_list_new_from_default_save", methods=["post"])
def shopping_list_new_from_default_save():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    # Check csrf
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    # Set scroll position to the beginning of the page
    session["scroll_pos"] = 0

    # Validate form data
    try:
        list_name = request.form["shopping_list_name"]
    except:
        return redirect("/error")
    if len(list_name) > 30:
        flash("Nimi on liian pitkä")
        return redirect("/shopping_list_new_from_default")                    
    
    list_id = shopping_lists.save_default_list_with_name(user_id, list_name)

    if not list_id:
        flash("Tallennuksessa tapahtui virhe")
        return redirect("/shopping_list_new_from_default")

    return redirect("/shopping_list_details/"+str(list_id))

@app.route("/shopping_list_delete", methods=["post"])
def shopping_list_delete():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    # Check csrf
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    
    # Validate data
    try:
        list_id = int(request.form["list_id"])
    except:
        return redirect("/error")

    # Delete list
    if shopping_lists.delete_list(user_id, list_id):
        flash("Lista on poistettu")
    else:
        flash("Listan poistaminen ei onnistunut")

    return redirect("/shopping_list")

