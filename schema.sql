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

CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);
