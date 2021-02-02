from db import db
from flask import session
import datetime
import recipes

def create_default_plan(user_id):
    # Check if there is a default plan already
    sql = "SELECT id FROM plans WHERE user_id=:user_id AND default_plan=1"
    result = db.session.execute(sql, {"user_id":user_id})
    plan_id = result.fetchone()
    # If not, create default plan
    if plan_id == None:
        date_today = datetime.date.today().strftime("%Y-%m-%d")
        sql = "INSERT INTO plans (user_id, default_plan, startdate, period) VALUES (:user_id,1, :date_today, 7)"
        db.session.execute(sql, {"user_id":user_id, "date_today":date_today})
        db.session.commit()
        return True
    else:
        return False

def get_default_plan_id(user_id):
    sql = "SELECT id FROM plans WHERE user_id=:user_id AND default_plan=1"
    result = db.session.execute(sql, {"user_id":user_id})
    plan_id = result.fetchone()
    return plan_id[0]

def set_startdate(plan_id, startdate):
    sql = "UPDATE plans SET startdate=:startdate WHERE id=:plan_id"
    db.session.execute(sql, {"startdate":startdate, "plan_id":plan_id})
    db.session.commit()
    return True

def get_startdate(plan_id):
    sql = "SELECT startdate FROM plans WHERE id=:plan_id"
    result = db.session.execute(sql, {"plan_id":plan_id})
    startdate = result.fetchone()
    return startdate[0]

def get_period(plan_id):
    sql = "SELECT period FROM plans WHERE id=:plan_id"
    result = db.session.execute(sql, {"plan_id":plan_id})
    period = result.fetchone()
    return period[0]

def set_period(plan_id, period):
    sql = "UPDATE plans SET period=:period WHERE id=:plan_id"
    db.session.execute(sql, {"period":period, "plan_id":plan_id})
    db.session.commit()
    return True

def get_planning_dates(startdate, period):
    dates = []
    for i in range(period):
        dates.append(startdate + datetime.timedelta(days=i))
    return dates

def get_weekday(weekday_index):
    weekdays = ["maanantai", "tiistai", "keskiviikko", "torstai", "perjantai", "lauantai", "sunnuntai"]
    return weekdays[weekday_index]

def get_notes(plan_id):
    startdate = get_startdate(plan_id)
    period = get_period(plan_id)
    notes_list = []
    for i in range(period):
        plan_row_date = startdate + datetime.timedelta(days=i)
        sql = "SELECT notes FROM plan_rows WHERE plan_id=:plan_id AND plan_row_date=:plan_row_date"
        result = db.session.execute(sql, {"plan_id":plan_id, "plan_row_date":plan_row_date})
        notes = result.fetchone()
        if notes == None:
            notes_list.append("")
        else:
            notes_list.append(notes[0])
    return notes_list

def get_selected_recipes(plan_id):
    startdate = get_startdate(plan_id)
    period = get_period(plan_id)
    selected_recipes_list = [None] * period 
    for i in range(period):
        selected_recipes_list[i] = [""] * 3

    for i in range(period):
        recipe_list = recipes.get_recipes()
        plan_row_date = startdate + datetime.timedelta(days=i)
        sql = "SELECT recipe_0, recipe_1, recipe_2 FROM plan_rows WHERE plan_id=:plan_id AND plan_row_date=:plan_row_date"
        result = db.session.execute(sql, {"plan_id":plan_id, "plan_row_date":plan_row_date})
        recipe = result.fetchone()
        if recipe != None:
            for j in range(3):
                for k in range(len(recipe_list)):
                    if recipe_list[k][1] == recipe[j]:
                        selected_recipes_list[i][j] = recipe_list[k][0]

    return selected_recipes_list


def save_row(plan_id, startdate, plan_row_number, recipes, notes):

    # Find ids for selected recipes
    recipe_ids = [0] * len(recipes)
    sql = "SELECT id FROM recipes WHERE name=:name"
    for i in range(len(recipe_ids)):
        result = db.session.execute(sql, {"name":recipes[i]})
        recipe_id = result.fetchone()
        if recipe_id == None:
            print("Virhe: valitun aterian reseptiä ei löydy")
            return False
        else:
            recipe_ids[i] = recipe_id[0]

    # Check if there is a plan row with this date already
    plan_row_date = startdate + datetime.timedelta(days=plan_row_number)
    plan_row_date = plan_row_date.strftime("%Y-%m-%d")
    sql = "SELECT id FROM plan_rows WHERE plan_id=:plan_id AND plan_row_date=:plan_row_date"
    result = db.session.execute(sql, {"plan_id":plan_id, "plan_row_date":plan_row_date})
    plan_row_id = result.fetchone()

    # Insert or update plan row data to the database
    if plan_row_id == None:
        sql = "INSERT INTO plan_rows (plan_id, plan_row_date, recipe_0, recipe_1, recipe_2, notes) VALUES (:plan_id, :plan_row_date, :recipe_0, :recipe_1, :recipe_2, :notes)"
    else:
        sql = "UPDATE plan_rows SET recipe_0=:recipe_0, recipe_1=:recipe_1, recipe_2=:recipe_2, notes=:notes WHERE plan_id=:plan_id AND plan_row_date=:plan_row_date"
    
    db.session.execute(sql, {"plan_id":plan_id, "plan_row_date":plan_row_date, "recipe_0":recipe_ids[0], "recipe_1":recipe_ids[1], "recipe_2":recipe_ids[2], "notes":notes})
    db.session.commit()

    return True


  
