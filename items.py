from db import db
from flask import session

def item_search(query):
    sql = "SELECT id, name FROM items WHERE name LIKE :query ORDER BY name"
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    items = result.fetchall()
    return items

def get_item(item_id):
    sql = "SELECT id, name, class FROM items WHERE id=:item_id"
    result = db.session.execute(sql, {"item_id":item_id})
    item = result.fetchone()
    return item


def item_change(item_id, item_name, item_class):
    sql = "UPDATE items SET name=:name, class=:class WHERE id=:id"
    db.session.execute(sql, {"id":item_id, "name":item_name, "class":item_class})
    db.session.commit()

    return True    
