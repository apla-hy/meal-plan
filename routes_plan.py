from app import app
from flask import render_template, request, redirect, session, flash, abort
import users
import plans
import recipes
import shopping_lists


@app.route("/plan", methods=["get"])
def plan():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")

    # Get the default plan id of the user
    plan_id = plans.get_default_plan(user_id)
    if not plan_id:
        return redirect("/error")
    
    # Get the data for the plan page
    startdate = plans.get_startdate(plan_id)
    if not startdate:
        return redirect("/error")
    period = plans.get_period(plan_id)
    if not period:
        return redirect("/error")
    planning_dates = plans.get_planning_dates(startdate, period)
    weekdays = []
    dates = []
    for planning_date in planning_dates:
        weekdays.append(plans.get_weekday(planning_date.weekday()))
        dates.append(planning_date.strftime("%d.%m.%Y"))
    recipe_list = recipes.get_recipe_names()
    notes = plans.get_notes(plan_id)
    selected_recipes = plans.get_selected_recipes(plan_id)

    # Show the plan page
    return render_template("plan.html", plan_id=plan_id, startdate=startdate, period=period, dates=dates, \
        weekdays=weekdays, recipes=recipe_list, selected_recipes=selected_recipes, notes=notes)

@app.route("/plan_change_date", methods=["post"])
def plan_change_date():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    # Check csrf
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    # Validate form data
    try:
        plan_id = int(request.form["plan_id"])
    except:
        return redirect("/error")
    startdate = request.form["startdate"]
    if len(startdate) > 10:
        flash("Päivämäärän muoto on väärin")
        return redirect("/plan")

    # Change the start date
    if not plans.set_startdate(plan_id, startdate):
        flash("Aloituspäivän muutos ei onnistunut")

    return redirect("/plan")

@app.route("/plan_change_period", methods=["post"])
def plan_change_period():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    # Check csrf
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    # Validate form data
    try:
        plan_id = int(request.form["plan_id"])
    except:
        return redirect("/error")
    try:
        period = int(request.form["period"])
    except:
        flash("Suunnittelujakso pitää olla kokonaisluku")
        return redirect("/plan")
    if period < 2 or period > 30:
        flash("Suunnittelujakso pitää olla välillä 1-30")
        return redirect("/plan")

    # Change period
    if not plans.set_period(plan_id, period):
        flash("Suunnittelujakson muutos ei onnistunut")

    return redirect("/plan")

@app.route("/plan_save_rows", methods=["post"])
def plan_save_rows():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    # Check csrf
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    # Validate form header data
    try:
        plan_id = int(request.form["plan_id"])
    except:
        return redirect("/error")
    startdate = plans.get_startdate(plan_id)
    if not startdate:
        return redirect("/error")

    # Save rows
    period = plans.get_period(plan_id)
    if not period:
        return redirect("/error")
    error_rows = 0
    for i in range(period):
        plan_row_number = i
        selected_recipes = []
        for j in range(3):
            selected_recipe = request.form[str(i) + "_" + str(j)]
            if len(selected_recipe) > 100:
                flash("Reseptikentän maksimipituus on 100 merkkiä")
                selected_recipe = selected_recipe[:100]
            selected_recipes.append(selected_recipe)
        notes = request.form[str(i) + "_notes"]
        if len(notes) > 1000:
            flash("Muistiinpanojen maksimimpituus on 1000 merkkiä")
            notes = notes[:1000]
        if not plans.save_row(plan_id, startdate, plan_row_number, selected_recipes, notes):
            error_rows += 1

    if error_rows > 0:
        flash(str(error_rows) + " rivin tallennus ei onnistunut")
    else:
        flash("Suunnitelma tallennettu")

    return redirect("/plan")

@app.route("/plan_create_shopping_list", methods=["post"])
def plan_create_shopping_list():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    # Check csrf
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    # Validate form data
    try:
        plan_id = int(request.form["plan_id"])
    except:
        return redirect("/error")
    startdate = plans.get_startdate(plan_id)
    if not startdate:
        return redirect("/error")
    period = plans.get_period(plan_id)
    if not period:
        return redirect("/error")
    selected_recipes = []
    for i in range(period):
        for j in range(3):
            selected_recipe = request.form[str(i) + "_" + str(j)]
            if len(selected_recipe) > 100:
                flash("Reseptikentän maksimipituus on 100 merkkiä")
                selected_recipe = selected_recipe[:100]
            selected_recipes.append(selected_recipe)

    # Create shopping list
    list_rows = shopping_lists.new_list_from_plan(selected_recipes)
    
    # Save shopping list to the database
    list_id = shopping_lists.get_default_list(user_id)
    if not list_id:
        return redirect("/error")
    if not shopping_lists.save_list_rows(list_id, list_rows):
        flash("Ostoslista luonti ei onnistunut")
        return redirect("/plan")

    # Set scroll position to the beginning of the page
    session["scroll_pos"] = 0

    # Show shopping list
    return redirect("/shopping_list_details/"+str(list_id))


@app.route("/plan_show_default_shopping_list", methods=["post"])
def plan_show_default_shopping_list():

    # Check that there is an active session
    user_id = users.get_user_id()
    if not user_id:
        return redirect("/")
    # Check csrf
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    list_id = shopping_lists.get_default_list(user_id)
    if not list_id:
        return redirect("/error")

    # Set scroll position to the beginning of the page
    session["scroll_pos"] = 0

    # Show shopping list
    return redirect("/shopping_list_details/"+str(list_id))




