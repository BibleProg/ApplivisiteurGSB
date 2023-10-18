import sqlite3
from flask import Flask
from flask import render_template, request, redirect, url_for, g, jsonify
from functools import wraps
import datetime
import jwt
import json

app = Flask(__name__)

DATABASE= "db/data.db"

app.config['SECRET_KEY'] = 'secret'

def check_for_token(func):
    @wraps(func) 
    def wrapped(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'Il manque le token'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Token non valide'}),403
        return func(*args, **kwargs)
    return wrapped


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def change_db(query,args=()):
    cur = get_db().execute(query, args)
    get_db().commit()
    cur.close()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Routage des URL et traitement
@app.route('/')
def index():
    utilisateur_list=query_db("SELECT * FROM utilisateur")
    return render_template("index.html",utilisateur_list=utilisateur_list)
    if request.form['user'] == utilisateur.user and request.form['password'] == utilisateur.password:
        session['logged_in'] = True
        token = jwt.encode({
            'user': request.form['user'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=120)
            },
            app.config['SECRET_KEY'])
        

@app.route('/bdd', methods=['GET', 'POST'])
def bdd():
    return render_template("bdd.html",utilisateur_list=utilisateur_list)

@app.route('/create', methods=['GET', 'POST'])
def create():

    if request.method == "GET":
        return render_template("create.html",utilisateur=None)

    if request.method == "POST":
        utilisateur=request.form.to_dict()
        values=[utilisateur["user"],utilisateur["password"]]
        change_db("INSERT INTO utilisateur (user,password) VALUES (?,?)",values)
        return redirect(url_for("bdd"))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def udpate(id):

    if request.method == "GET":
        utilisateur=query_db("SELECT * FROM utilisateur WHERE id=?",[id],one=True)
        return render_template("update.html",utilisateur_list=utilisateur_list)

    if request.method == "POST":
        utilisateur=request.form.to_dict()
        values=[utilisateur["user"],utilisateur["password"],utilisateur["token"],id]
        change_db("UPDATE utilisateur SET user=?, password=?, token=?, WHERE ID=?",values)
        return redirect(url_for("bdd"))
        
        

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):

    if request.method == "GET":
        utilisateur=query_db("SELECT * FROM utilisateur WHERE id=?",[id],one=True)
        return render_template("delete.html",utilisateur_list=utilisateur_list)

    if request.method == "POST":
        change_db("DELETE FROM utilisateur WHERE id = ?",[id])
        return redirect(url_for("bdd"))

app.run(port=5000,debug=True)