# IMPORTANT setup :
# set FLASK_APP   = <nom_du_script> (sans l'extention)
# set FLASK_ENV   = development | production (default = production)
# set FLASK_DEBUG = true | false (default = false)
# in code exemple : app.config['DEBUG'] = True
# liste conf      : https://flask.palletsprojects.com/en/2.0.x/config/

# commandes utiles :
# flask run -h 127.0.0.1 -p 3000 # demmarre le serveur avec l'host 'localhost' et sur le port 3000

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

app = Flask(__name__)

######## CATCH et REMPLACE les erreurs HTTP  ####################
@app.errorhandler(404)
def page_not_found(error):
    # if app.config['ENV'] == 'development':
    #    return redirect("/links")
    return "hey je suis l'erreur 404", 404
#################################################################

@app.route("/", methods=['POST', 'GET', 'TRACE'])
def index():
    return "Welcome to our " + app.config['ENV'] + " server"

@app.route("/links")
def list_routes():
    routes = ''

    for rule in app.url_map.iter_rules():
        routes += "<a href='" + str(rule) + "'>" + escape(str(rule)) + "</a>"
        routes += "<br>"

    return routes

@app.route("/tellmemore")
def hello():
    return "<p>not todey</p>"

######### Codes d'erreur HTTP #################################

@app.route("/erreur_HTTP")
def num_error():
    return render_template('erreur_HTTP.html') # toutes les templates doivent se trouver dans le dossier templates/

@app.route("/erreur_HTTP/<int:num>")
def my_error(num):
    abort(num)
    return "Ceci n'est pas sensé s'afficher"

######### JSON time ############################################
@app.route("/cava")
def oui():
    # ATTENTION simple quotes dehors et double quotes dedans sinon error JSON Parse !!!
    return Response('{"reponse" : "oui cimer bro"}', status=200, mimetype='application/json')

######### Test des variables en GET ############################

@app.route("/hello/") # On set 2 routes pour pouvoir appeler la route avec la valuer par défaut
@app.route("/hello/<name>")
def salut_x(name='Bob marley'):
    alias = request.args.get('alias', 'l\'idiot de service')
    return "hello " + name + " aka " + alias


######### Test des différentes méthodes (POST, GET)########################

@app.route("/test/POST", methods=['POST', 'GET'])
def test_post():
    if request.method == 'POST':
        return "Bien tu a réussi à faire une requète en post"
    if request.method == 'GET':
        return "Boulet, tu m'as interrogé en GET"

@app.route("/test/GET", methods=['POST', 'GET'])
def test_get():
    if request.method == 'GET':
        return "Bien joué tu gères le GET dis moi"
    if request.method == 'POST':
        return "No POST for me pls"

# Quand on ne définit qu'une seule méthode, si la mauvaise est utilisé on a une erreure 405
@app.route("/test/strict/GET", methods=['GET'])
def test_strict_get():
    return "Hello du GET"

@app.route("/test/strict/POST", methods=['POST'])
def test_strict_post():
    return "Hello du POST"


######### TP the H4CKERMAN ########################
# @app.route("/pass/generate")
# def test():
#     return "yo"

@app.route("/pass/generate")
def generate_pass():
    the_password = ''
    for i in range(4):
        the_password += str(randint(0,9))
    app.config['PASS'] = the_password
    return the_password


@app.route("/pass/guess/<password>")
def you_should_not_pass(password):
    if password == app.config['PASS'] :
        return "", 200
    else:
        abort(423)


#############################GSB_POC##################################

def connexion(db_name):
    try:
        sqliteConnection             = sqlite3.connect(db_name)
        sqliteConnection.row_factory = sqlite3.Row
        cursor                       = sqliteConnection.cursor()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)

    return sqliteConnection

    

@app.route("/GSB/medecin/<int:Id>/")
@app.route("/GSB/medecin")
def medecin(Id = 0):
    cursor = connexion('api.db').cursor()
    if Id == 0 :
        sql = "SELECT * from Medecins ORDER BY Nom"
    else:
        sql = "SELECT * FROM Medecins WHERE Id = " + str(Id)
    cursor.execute(sql)
    result = cursor.fetchall()
    if len(result) == 0:
        return Response('{"error" : "Aucun enregistrement pour l\'ID ' + str(Id) + '"}', status=404, mimetype='application/json')
    cursor.close()
    #return json.dumps([dict(ix) for ix in result])
    return Response(json.dumps([dict(ix) for ix in result]), status=202, mimetype='application/json')

@app.route("/GSB/medicament")
@app.route("/GSB/medicament/<int:Id>/")
def medicament(Id = 0):
    cursor = connexion('api.db').cursor()
    if Id == 0 :
        sql = "SELECT * from Medicament"
    else:
        sql = "SELECT * FROM Medicament WHERE Id = " + str(Id)
    cursor.execute(sql)
    result = cursor.fetchall()
    if len(result) == 0:
        return Response('{"error" : "Aucun enregistrement pour l\'ID ' + str(Id) + '"}', status=404, mimetype='application/json')
    cursor.close()
    #return json.dumps([dict(ix) for ix in result])
    return Response(json.dumps([dict(ix) for ix in result]), status=202, mimetype='application/json')

@app.route("/GSB/CR/<int:Id>/")
@app.route("/GSB/CR/<int:Id>")
def CR(Id = 0):
    cursor = connexion('api.db').cursor()

    sql_CR = """
    SELECT CR.Id, M.Civilite || ' ' || M.Nom || ' ' || M.Prenom AS Medecin,  CR.Date, CR.Motif, CR.Bilan
    FROM Compte_rendu CR
    JOIN Medecins M ON CR.Medecin_id = M.Id
    WHERE CR.Id = """ + str(Id)

    sql_Medoc = """
    SELECT Medicament.Label, Medocs.Nombre
    FROM Medocs
    JOIN Medicament ON Medocs.Medicament_id = Medicament.Id
    WHERE Medocs.CR_id = """ + str(Id)
    try:
        cursor.execute(sql_CR)
    except sqlite3.Error as error:
        return "Error while connecting to sqlite " + error

    result_CR = cursor.fetchall() 
    if len(result_CR) == 0:
        return Response('{"error" : "Aucun enregistrement pour l\'ID ' + str(Id) + '"}', status=400, mimetype='application/json')
    output_CR = [dict(ix) for ix in result_CR][0]
    
    try:
        cursor.execute(sql_Medoc)
    except sqlite3.Error as error:
        return "Error while connecting to sqlite " + error

    result_Medoc = cursor.fetchall()
    if len(result_Medoc) == 0:
        return Response('{"error" : "Aucun enregistrement pour l\'ID ' + str(Id) + '"}', status=400, mimetype='application/json')
    output_Medoc = [dict(ix) for ix in result_Medoc]
    output_CR["Medoc"] = output_Medoc
    
    cursor.close()
    return Response(json.dumps(output_CR), status=200, mimetype='application/json')
    return output_CR  

@app.route("/GSB/CR/Insert", methods=['POST'])
def Insert_CR():
    conn = connexion('api.db')
    cursor = conn.cursor()
    cr = request.get_json()
    if not cr :
        return 'nope', 404

    # return jsonify(cr)
    # cr = '{"Id": 1, "Medecin": 1, "Date": "21/07/2021", "Motif": "Visite", "Bilan": "Bla Bla Bla...", "Medoc": [{"Id": 1, "Nombre": 2}, {"Id": 3, "Nombre": 5}, {"Id": 4, "Nombre": 1}]}'
    # cr = json.loads(cr)
    cursor.execute("SELECT seq FROM sqlite_sequence WHERE name = 'Compte_rendu'")
    
    Id = cursor.fetchall()[0][0] + 1
    
    query_CR    = "INSERT INTO Compte_rendu(Medecin_id, Date, Motif, Bilan) VALUES (?,?,?,? )"
    cursor.execute(query_CR, (cr["Medecin"], cr["Date"], cr["Motif"], cr["Bilan"]))

    query_Medoc = "INSERT INTO Medocs(Medicament_id, Cr_id, Nombre) VALUES (?,?,?)"
    Medoc_list  = list()
    for medoc_id, nombre in cr["Medoc"].items():
        Medoc_list.append ([medoc_id, Id, nombre])

    cursor.executemany(query_Medoc, Medoc_list)

    conn.commit()
    cursor.close()

    return str(Id), 200



######################################################################







# Test des différentes URL, mettre en paramètre de la fonction url_for() le nom de la fonction appelé pour une ROUTE.
# le debug s'affiche sur la console du serveur
if (str(app.config['ENV']) == 'development'):
    with app.test_request_context():
        url_for('index')
        url_for('hello')
        url_for('salut_x', name='test')

generate_pass()




# **NOTES**
# On peut donner Plusieurs fois la même "route" mais en cas de conflit c'est la première qui sera prise en compte 
