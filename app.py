from flask import Flask
from os import getenv

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

import routes
import routes_plan
import routes_shopping_list
import routes_recipe
