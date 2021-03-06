from app import app
from flask import render_template, request, redirect, session, flash
import users
import items


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
            flash("Väärä tunnus tai salasana")
            return redirect("/login")

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
        if password != password_check:
            flash("Salasanat eivät ole samat")
            return redirect("/register")

        # Check password length
        if len(password) < 4:
            flash("Salasana on liian lyhyt")
            return redirect("/register")

       # Check username length
        if len(username) < 4:
            flash("Käyttäjätunnus on liian lyhyt")
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

    if request.method == "GET":
        return render_template("profile.html")

    if request.method == "POST":

        # Check csrf
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)

        # Validate form data
        try:
            username = request.form["username"]
            password = request.form["password"]
            password_check = request.form["password_check"]
        except:
            return redirect("/error")

        # Check that passwords are the same
        if password != password_check:
            flash("Salasanat eivät ole samat")
            return redirect("/profile")

        # Check password length
        if len(password) < 4:
            flash("Salasana on liian lyhyt")
            return redirect("/profile")

       # Check username length
        if len(username) < 4:
            flash("Käyttäjätunnus on liian lyhyt")
            return redirect("/register")

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

    # Store this page to the session history
    session["previous_page"] = "item"
    session["previous_page_url"] = "/item"

    query = request.args.get("query")
    if query == None:
        query = ''
    item_list = items.item_search(query)

    return render_template("item.html", items=item_list, number_of_items=len(item_list))

@app.route("/item_details/<int:id>", methods=["get"])
def item_details(id):

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")

    item_id = id
    item = items.get_item(item_id)
    if not item:
        return redirect("/error")
    item_name = item[1]
    item_class = item[3]
    class_list = items.get_class_names()

    return render_template("item_details.html", item_id=item_id, item_name=item_name, item_class=item_class, \
        class_list=class_list, number_of_classes=len(class_list))

@app.route("/item_save", methods=["post"])
def item_save():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    # Check csrf
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    # Validate form data
    try:
        item_id = int(request.form["item_id"])
        item_name = request.form["item_name"]
        item_class = request.form["item_class"]
    except:
        return redirect("/error")
    if len(item_name) > 50:
        flash("Nimikkeen nimi on liian pitkä")
        return redirect("/item_details/"+str(item_id))    
    if len(item_name) == 0:
        flash("Nimikkeen nimi ei voi olla tyhjä")
        return redirect("/item_details/"+str(item_id))    
        
    # Save data
    if items.item_change(item_id, item_name, item_class):
        flash("Tallennettu")
    else:
        flash("Tallennus ei onnistunut")

    return redirect("/item_details/"+str(item_id))


@app.route("/item_new", methods=["get"])
def item_new():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")

    class_list = items.get_class_names()

    return render_template("item_new.html", class_list=class_list, number_of_classes=len(class_list))


@app.route("/item_new_save", methods=["post"])
def item_new_save():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    # Check csrf
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    # Validate form data
    try:
        item_name = request.form["item_name"]
        item_class = request.form["item_class"]
    except:
        return redirect("/error")
    if len(item_name) > 50:
        flash("Nimikkeen nimi on liian pitkä")
        return redirect("/item_new")    
    if len(item_name) == 0:
        flash("Nimikkeen nimi ei voi olla tyhjä")
        return redirect("/item_new")    

    if items.item_new(item_name, item_class):
        flash("Nimike lisätty")
    else:
        flash("Nimikkeen lisäys ei onnistunut")

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

    item_class_list = items.get_item_classes()

    row_ids = []
    row_names = []
    for item_class in item_class_list:
        row_ids.append(item_class[0])
        row_names.append(item_class[1])

    return render_template("item_class.html", row_ids=row_ids, row_names=row_names, number_of_rows=len(row_ids))


@app.route("/item_class_move_up/<int:id>", methods=["post"])
def item_class_move_up(id):

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    # Check csrf
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    items.item_class_move_up(id)

    return redirect("/item_class")


@app.route("/item_class_move_down/<int:id>", methods=["post"])
def item_class_move_down(id):

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    # Check csrf
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    items.item_class_move_down(id)

    return redirect("/item_class")


@app.route("/item_class_save", methods=["post"])
def item_class_save():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    # Check csrf
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    # Validate form data
    try:
        number_of_rows = int(request.form["number_of_rows"])
    except:
        return redirect("/error")

    # Save classes
    error = False
    for i in range(number_of_rows):
        try:
            class_id = int(request.form[str(i) + "_row_id"])
            class_name = request.form[str(i) + "_row_name"]
        except:
            return redirect("/error")
        if len(class_name) > 50:
            error = True
            flash("Luokan nimi on liian pitkä")
            return redirect("/item_class")
        if not items.save_class(class_id, class_name):
            error = True
            flash(str(i+1) + ". rivin tallentaminen ei onnistunut")

    if not error:
        flash("Tallennus onnistui")

    return redirect("/item_class")


@app.route("/item_class_new", methods=["post"])
def item_class_new():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    # Check csrf
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    # Validate form data
    try:
        class_name = request.form["item_class_new_name"]
    except:
        return redirect("/error")
    if len(class_name) > 50:
        flash("Luokan nimi on liian pitkä")

    # Add new item class
    if items.new_class(class_name):
        flash("Luokan lisäys onnistui")
    else:
        flash("Luokan lisäys ei onnistunut")

    return redirect("/item_class")

