from app import app
from flask import render_template, request, redirect
import users
import plans
import recipes
import items

@app.route("/")
def index():
    username = users.get_username()
    if username:
        return redirect("/plan")
    else:
        return render_template("index.html")

@app.route("/plan")
def plan():
    username = users.get_username()
    user_id = users.get_user_id()
    plans.create_default_plan(user_id)
    plan_id = plans.get_default_plan_id(user_id)
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
    startdate = request.form["startdate"]
    plan_id = request.form["plan_id"]
    plans.set_startdate(plan_id, startdate)

    return redirect("/plan")

@app.route("/plan_change_period", methods=["post"])
def plan_change_period():
    period = request.form["period"]
    plan_id = request.form["plan_id"]
    plans.set_period(plan_id, period)

    return redirect("/plan")

@app.route("/plan_save_rows", methods=["post"])
def plan_save_rows():
    plan_id = request.form["plan_id"]
    startdate = plans.get_startdate(plan_id)
    period = plans.get_period(plan_id)
    
    for i in range(period):
        plan_row_number = i
        recipes = []
        for j in range(3):
            recipes.append(request.form[str(i) + "_" + str(j)])
        notes = request.form[str(i) + "_notes"]
        plans.save_row(plan_id, startdate, plan_row_number, recipes, notes)        

    return redirect("/plan")



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
    username = users.get_username()
    if request.method == "GET":
        return render_template("profile.html",username=username)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.update_profile(username,password):
            return redirect("/")
        else:
            return render_template("error.html",message="Tietojen tallannus ei onnistunut")

@app.route("/item", methods=["get"])
def item():
    query = request.args.get("query")
    if query == None:
        query = ''
    item_list = items.item_search(query)
    return render_template("item.html",items=item_list, number_of_items=len(item_list))

@app.route("/item_details/<int:id>", methods=["get"])
def item_modify(id):
    item_id = id
    item = items.get_item(item_id)
    item_name = item[1]
    item_class = item[2]
    return render_template("item_details.html", item_id=item_id, item_name=item_name, item_class=item_class)

@app.route("/item_save", methods=["post"])
def item_save():
    item_id = request.form["item_id"]
    item_name = request.form["item_name"]
    item_class = request.form["item_class"]
    items.item_change(item_id, item_name, item_class)

    return redirect("/item_details/"+str(item_id))

