from flask import Flask
from flask import jsonify
from flask import url_for
from flask import request
from flask import abort
from flask import redirect
from flask import render_template
from flask import Response

from html import escape
from random import randint

import sqlite3
import json
import pprint
import datetime

@app.route("/GSB/connexion", methods=['POST'])
def se_connecter():
    # {"login" : "hello", "password" : "world"}
    ressources = request.get_json()
    cursor     = connexion('api.db').cursor()
    query      = "SELECT * FROM Visiteurs WHERE login = '{}' AND password = '{}'".format(ressources['login'], ressources['password'])
    cursor.execute(query)
    result = cursor.fetchone()
    if result:
        return str(result["id"])
    else:
        return "False"