from db import db
from flask import session
import datetime

def create_default_plan(user_id):
    # Check if there is a default plan already
    sql = "SELECT id FROM plans WHERE user_id=:user_id AND default_plan=1"
    result = db.session.execute(sql, {"user_id":user_id})
    plan_id = result.fetchone()
    # If not, create default plan
    if plan_id == None:
        date_today = datetime.date.today().strftime("%d.%m.%Y")
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
