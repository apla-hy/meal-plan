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
    sql = "SELECT name FROM item_classes ORDER BY class_order"
    result = db.session.execute(sql)
    item_classes = result.fetchall()
    class_list = []
    for item_class in item_classes:
        class_list.append(item_class[0])
    return class_list

def get_item_classes():
    sql = "SELECT id, name, class_order FROM item_classes ORDER BY class_order"
    result = db.session.execute(sql)
    item_classes = result.fetchall()
    return item_classes

def item_class_move_up(class_id):
    sql = "SELECT id, name, class_order FROM item_classes ORDER BY class_order"
    result = db.session.execute(sql)
    item_classes = result.fetchall()

    # Find row and move it one step up
    for i in range(len(item_classes)):
        if item_classes[i][0] == class_id:
            if i == 0:
                return False
            previous_row_id = item_classes[i-1][0]
            previous_row_order = item_classes[i-1][2]
            current_row_id = item_classes[i][0]
            current_row_order = item_classes[i][2]
            sql = "UPDATE item_classes SET class_order=:class_order WHERE id=:id"
            result = db.session.execute(sql, {"class_order":0, "id":previous_row_id})
            sql = "UPDATE item_classes SET class_order=:class_order WHERE id=:id"
            result = db.session.execute(sql, {"class_order":previous_row_order, "id":current_row_id})
            sql = "UPDATE item_classes SET class_order=:class_order WHERE id=:id"
            result = db.session.execute(sql, {"class_order":current_row_order, "id":previous_row_id})
            db.session.commit()
    
    return True

def item_class_move_down(class_id):
    sql = "SELECT id, name, class_order FROM item_classes ORDER BY class_order"
    result = db.session.execute(sql)
    item_classes = result.fetchall()

    # Find row and move it one step down
    for i in range(len(item_classes)-1):
        if item_classes[i][0] == class_id:
            next_row_id = item_classes[i+1][0]
            next_row_order = item_classes[i+1][2]
            current_row_id = item_classes[i][0]
            current_row_order = item_classes[i][2]
            sql = "UPDATE item_classes SET class_order=:class_order WHERE id=:id"
            result = db.session.execute(sql, {"class_order":0, "id":next_row_id})
            sql = "UPDATE item_classes SET class_order=:class_order WHERE id=:id"
            result = db.session.execute(sql, {"class_order":next_row_order, "id":current_row_id})
            sql = "UPDATE item_classes SET class_order=:class_order WHERE id=:id"
            result = db.session.execute(sql, {"class_order":current_row_order, "id":next_row_id})
            db.session.commit()
    
    return True



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
    try:
        sql = "UPDATE items SET name=:name, class_id=:class_id WHERE id=:id"
        db.session.execute(sql, {"id":item_id, "name":item_name, "class_id":item_class_id})
        db.session.commit()
    except:
        db.session.rollback()
        return False

    return True    

def item_new(item_name, item_class):
    sql = "SELECT id FROM item_classes WHERE name=:item_class"
    result = db.session.execute(sql, {"item_class":item_class})
    item_class_id = result.fetchone()[0]
    try:
        sql = "INSERT INTO items (name, class_id, default_item) VALUES (:name, :class_id, 0) RETURNING id"
        result = db.session.execute(sql, {"name":item_name, "class_id":item_class_id})
        item_id = result.fetchone()[0]
        db.session.commit()
    except:
        db.session.rollback()
        return False

    return item_id

