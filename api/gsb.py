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

import pyodbc
import sqlite3
import json
import pprint
import datetime

app = Flask(__name__)

@app.route("/links")
def list_routes():
    routes = ''

    for rule in app.url_map.iter_rules():
        routes += "<a href='" + str(rule) + "'>" + escape(str(rule)) + "</a>"
        routes += "<br>"

    return routes

#############################GSB_POC##################################

def connexion(db_name):
    
    dir_path = './'
    db_path  = dir_path + db_name
    
    cnxn = pyodbc.connect("Driver=SQLite3 ODBC Driver;Database=" + db_path)
    return cnxn.cursor()

def query(sql, arg=False):

    try:
        cursor = connexion('api.db')
    except pyodbc.Error as e:
        return f"error : {e}"

    try:
        if arg:
            if type(arg) == type(list()):
                cursor.executemany(sql,arg)
            else:
                print(sql, arg)
                cursor.execute(sql,*arg)    
        else:
            print('2')
            cursor.execute(sql)
    except pyodbc.Error as e:
        cursor.rollback()
        return f"error : {e}"

    cursor.commit()

    try:
        res = cursor.fetchall()

        columns = [column[0] for column in cursor.description]
        results = []
        
        if len(res) > 1:
            for row in res:
                results.append(dict(zip(columns, row)))
        else:
            results = dict(zip(columns, res[0]))
    except pyodbc.ProgrammingError as e:
        results = cursor.rowcount 

    cursor.close()
    
    return results

@app.route("/test")
def test():
    sql = "SELECT seq FROM sqlite_sequence WHERE name = ? AND 1 = ?"
    Id = query(sql, ('Compte_rendu', 1))
    return str(Id)

@app.route("/GSB/medecin/<int:Id>/")
@app.route("/GSB/medecin")  #Praticiens
def medecin(Id = 0):
    if Id == 0 :
        sql = "SELECT * from Praticiens ORDER BY Nom"
    else:
        sql = "SELECT * FROM Praticiens WHERE Id = " + str(Id)

    results = query(sql)

    if len(results) == 0:
        return Response('{"erreur" : "Aucun enregistrement pour l\'ID ' + str(Id) + '"}', status=404, mimetype='application/json')
    
    return Response(json.dumps(results), status=202, mimetype='application/json')


@app.route("/GSB/medicament")
@app.route("/GSB/medicament/<int:Id>/")
def medicament(Id = 0):

    if Id == 0 :
        sql = "SELECT * from Medicaments"
    else:
        sql = "SELECT * FROM Medicaments WHERE Id = " + str(Id)

    result = query(sql)
    if len(result) == 0:
        return Response('{"error" : "Aucun enregistrement pour l\'ID ' + str(Id) + '"}', status=404, mimetype='application/json')

    return Response(json.dumps(result), status=202, mimetype='application/json')

@app.route("/GSB/CR/<int:Id>/")
def CR(Id = 0):
    sql_CR = """
    SELECT CR.Id, M.Civilite || ' ' || M.Nom || ' ' || M.Prenom AS Medecin,  CR.Date, CR.Motif, CR.Bilan
    FROM Compte_rendu CR
    JOIN Praticiens M ON CR.Medecin_id = M.Id
    WHERE CR.Id = """ + str(Id)

    sql_Medoc = """
    SELECT Medicaments.Label, Echantillons.Nombre
    FROM Echantillons
    JOIN Medicaments ON Echantillons.Medicaments_id = Medicaments.Id
    WHERE Echantillons.CR_id = """ + str(Id)

    result_CR = query(sql_CR)
    if len(result_CR) == 0:
        return Response('{"error" : "Aucun enregistrement pour l\'ID ' + str(Id) + '"}', status=404, mimetype='application/json')

    result_Medoc = query(sql_Medoc)
    if len(result_Medoc) == 0:
        return Response('{"error" : "Aucun enregistrement pour l\'ID ' + str(Id) + '"}', status=404, mimetype='application/json')

    result_CR["Medoc"] = result_Medoc
    
    return Response(json.dumps(result_CR), status=200, mimetype='application/json')

@app.route("/GSB/CR/medecin/<int:Id>/")
def cr_by_medecin(Id):
    sql_CR = """
    SELECT CR.Id, M.Civilite || ' ' || M.Nom || ' ' || M.Prenom AS Medecin,  CR.Date, CR.Motif, CR.Bilan
    FROM Compte_rendu CR
    JOIN Praticiens M ON CR.Medecin_id = M.Id
    WHERE CR.Medecin_id = """ + str(Id)

    result_CR = query(sql_CR) 
    if len(result_CR) == 0:
        return Response('{"error" : "Aucun enregistrement pour l\'ID ' + str(Id) + '"}', status=400, mimetype='application/json')

    cpt = 0
    for cr in result_CR : 
        sql_Medoc = """
        SELECT Medicaments.Label, Echantillons.Nombre
        FROM Echantillons
        JOIN Medicaments ON Echantillons.Medicaments_id = Medicaments.Id
        WHERE Echantillons.CR_id = """ + str(cr["Id"])

        result_Medoc = query(sql_Medoc)

        if len(result_Medoc) != 0:
            result_CR[cpt]["Medoc"] = result_Medoc
        
        cpt+=1
    
    return Response(json.dumps(result_CR), status=200, mimetype='application/json')

@app.route("/GSB/CR/visiteur/<int:Id>/")
def cr_by_visiteur(Id):
    sql_CR = """
    SELECT CR.Id, M.Civilite || ' ' || M.Nom || ' ' || M.Prenom AS Medecin,  CR.Date, CR.Motif, CR.Bilan
    FROM Compte_rendu CR
    JOIN Praticiens M ON CR.Medecin_id = M.Id
    WHERE CR.Visiteur_id = """ + str(Id)


    result_CR = query(sql_CR) 
    if len(result_CR) == 0:
        return Response('{"error" : "Aucun enregistrement pour l\'ID ' + str(Id) + '"}', status=400, mimetype='application/json')
    cpt = 0
    for cr in result_CR : 
        sql_Medoc = """
        SELECT Medicaments.Label, Echantillons.Nombre
        FROM Echantillons
        JOIN Medicaments ON Echantillons.Medicaments_id = Medicaments.Id
        WHERE Echantillons.CR_id = """ + str(cr["Id"])

        result_Medoc = query(sql_Medoc)
        if len(result_Medoc) != 0:
            result_CR[cpt]["Medoc"] = result_Medoc
        cpt+=1
    
    cursor.close()
    return Response(json.dumps(result_CR), status=200, mimetype='application/json')

@app.route("/GSB/CR/Insert", methods=['POST'])
def Insert_CR():

    cr = request.get_json()
    
    if not cr :
    	if request.headers['Content-Type'] != 'application/json':
    		return 'Le Content-Type doit être application/json', 400
    	else :
        	abort(400)

    filtre = ["Medecin", "Date", "Motif", "Bilan", "Medoc"]

    for el in filtre:
    	if el not in cr.keys():
    		return 'Il manque "'+ el +'" dans le JSON', 400
    try:
    	datetime.datetime.strptime(cr["Date"], "%d/%m/%Y")
    except ValueError:
    	return "La Date n'est pas au bon format, le bon format est : DD/MM/YYYY", 400
    
    # exemple : {"Medecin": 1, "Date": "21/07/2021", "Motif": "Visite", "Bilan": "Bla Bla Bla...", "Medoc": {"1": 1, "2" : 1, "3" : 5}}
    sql = "SELECT seq FROM sqlite_sequence WHERE name = 'Compte_rendu'"
    Id = query(sql)["seq"] + 1
    
    query_CR    = "INSERT INTO Compte_rendu(Medecin_id, Date, Motif, Bilan) VALUES (?,?,?,? )"
    query(query_CR, (cr["Medecin"], cr["Date"], cr["Motif"], cr["Bilan"]))

    query_Medoc = "INSERT INTO Echantillons(Medicaments_id, Cr_id, Nombre) VALUES (?,?,?)"
    Medoc_list  = []
    for medoc_id, nombre in cr["Medoc"].items():
        Medoc_list += [(medoc_id, Id, nombre)]

    total = query(query_Medoc, Medoc_list)

    return f"{total} Compte rendu inséré avec l'id : {Id}", 201

@app.route("/GSB/connexion", methods=['GET'])
def se_connecter():
    ressources = request.get_json()
    query      = "SELECT * FROM Visiteurs WHERE login = '{}' AND password = '{}'".format(ressources['login'], ressources['password'])

    result = query(query)
    if result:
        return str(result["id"])
    else:
        return "False"




######################################################################


app.run(port=80,debug=True)




# Test des différentes URL, mettre en paramètre de la fonction url_for() le nom de la fonction appelé pour une ROUTE.
# le debug s'affiche sur la console du serveur
# if (str(app.config['ENV']) == 'development'):
    # with app.test_request_context():
    #     url_for('index')
    #     url_for('hello')
    #     url_for('salut_x', name='test')





# **NOTES**
# On peut donner Plusieurs fois la même "route" mais en cas de conflit c'est la première qui sera prise en compte 