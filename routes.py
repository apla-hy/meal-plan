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



