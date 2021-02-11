CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE plans (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    default_plan INTEGER,
    startdate DATE,
    period INTEGER
);

CREATE TABLE item_classes (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    class_id INTEGER REFERENCES item_classes,
    name TEXT UNIQUE,
    default_item INTEGER
);

CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE recipe_rows (
    id SERIAL PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipes,
    item_id INTEGER REFERENCES items,
    amount TEXT
);

CREATE TABLE plan_rows (
    id SERIAL PRIMARY KEY,
    plan_id INTEGER REFERENCES plans,
    plan_row_date DATE,
    recipe_0 INTEGER REFERENCES recipes,
    recipe_1 INTEGER REFERENCES recipes,
    recipe_2 INTEGER REFERENCES recipes,
    notes TEXT
);


