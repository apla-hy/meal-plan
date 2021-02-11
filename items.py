from db import db
from flask import session

def item_search(query):
    sql = "SELECT id, name FROM items WHERE LOWER(name) LIKE LOWER(:query) AND default_item = 0 ORDER BY name"
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    items = result.fetchall()
    return items

def get_item(item_id):
    sql = "SELECT I.id, I.name, I.class_id, IC.name AS class_name FROM items I LEFT JOIN item_classes IC ON I.class_id=IC.id WHERE I.id=:item_id"
    result = db.session.execute(sql, {"item_id":item_id})
    item = result.fetchone()
    return item

def get_default_item_id():
    sql = "SELECT id FROM items WHERE default_item = 1"
    result = db.session.execute(sql)
    item_id = result.fetchone()[0]
    return item_id

def get_item_names():
    sql = "SELECT name FROM items"
    result = db.session.execute(sql)
    item_names = result.fetchall()
    name_list = []
    for name in item_names:
        name_list.append(name[0])
    return name_list

def get_class_names():
    sql = "SELECT name FROM item_classes ORDER BY name"
    result = db.session.execute(sql)
    item_classes = result.fetchall()
    class_list = []
    for item_class in item_classes:
        class_list.append(item_class[0])
    return class_list

def is_default_item(item_id):
   sql = "SELECT id FROM items WHERE default_item=1"
   result = db.session.execute(sql)
   default_item_id = result.fetchone()[0]
   if item_id == default_item_id:
       return True
   return False

def item_change(item_id, item_name, item_class):
    sql = "SELECT id FROM item_classes WHERE name=:item_class"
    result = db.session.execute(sql, {"item_class":item_class})
    item_class_id = result.fetchone()[0]

    sql = "UPDATE items SET name=:name, class_id=:class_id WHERE id=:id"
    db.session.execute(sql, {"id":item_id, "name":item_name, "class_id":item_class_id})
    db.session.commit()

    return True    

def item_new(item_name, item_class):
    sql = "SELECT id FROM item_classes WHERE name=:item_class"
    result = db.session.execute(sql, {"item_class":item_class})
    item_class_id = result.fetchone()[0]

    sql = "INSERT INTO items (name, class_id, default_item) VALUES (:name, :class_id, 0) RETURNING id"
    result = db.session.execute(sql, {"name":item_name, "class_id":item_class_id})
    item_id = result.fetchone()[0]
    db.session.commit()

    return item_id

