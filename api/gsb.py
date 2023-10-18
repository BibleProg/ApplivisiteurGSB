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
    try:
        sqliteConnection             = sqlite3.connect(db_name)
        sqliteConnection.row_factory = sqlite3.Row
        cursor                       = sqliteConnection.cursor()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)

    return sqliteConnection

    

@app.route("/GSB/medecin/<int:Id>/")
@app.route("/GSB/medecin")  #medecins
def medecin(Id = 0):
    cursor = connexion('api.db').cursor()
    if Id == 0 :
        sql = "SELECT * from Medecins ORDER BY Nom"
    else:
        sql = "SELECT * FROM Medecins WHERE Id = " + str(Id)
    cursor.execute(sql)
    result = cursor.fetchall()
    if len(result) == 0:
        return Response('{"erreur" : "Aucun enregistrement pour l\'ID ' + str(Id) + '"}', status=404, mimetype='application/json')
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

@app.route("/GSB/CR/medecin/<int:Id>")
def cr_by_medecin(Id):
    cursor = connexion('api.db').cursor()
    sql_CR = """
    SELECT CR.Id, M.Civilite || ' ' || M.Nom || ' ' || M.Prenom AS Medecin,  CR.Date, CR.Motif, CR.Bilan
    FROM Compte_rendu CR
    JOIN Medecins M ON CR.Medecin_id = M.Id
    WHERE CR.Medecin_id = """ + str(Id)

    try:
        cursor.execute(sql_CR)
    except sqlite3.Error as error:
        return "Error while connecting to sqlite " + error

    result_CR = cursor.fetchall() 
    if len(result_CR) == 0:
        return Response('{"error" : "Aucun enregistrement pour l\'ID ' + str(Id) + '"}', status=400, mimetype='application/json')
    output_CR = [dict(ix) for ix in result_CR]

    cpt = 0
    for cr in output_CR : 
        sql_Medoc = """
        SELECT Medicament.Label, Medocs.Nombre
        FROM Medocs
        JOIN Medicament ON Medocs.Medicament_id = Medicament.Id
        WHERE Medocs.CR_id = """ + str(cr["Id"])
        # print(sql_Medoc)


        
        try:
            cursor.execute(sql_Medoc)
        except sqlite3.Error as error:
            return "Error while connecting to sqlite " + error

        result_Medoc = cursor.fetchall()
        if len(result_Medoc) != 0:
            output_Medoc = [dict(ix) for ix in result_Medoc]
            output_CR[cpt]["Medoc"] = output_Medoc
        # print(len(result_Medoc) )
            # return Response('{"error" : "Aucun enregistrement pour l\'ID ' + str(Id) + '"}', status=400, mimetype='application/json')
        cpt+=1
    
    cursor.close()
    return Response(json.dumps(output_CR), status=200, mimetype='application/json')

@app.route("/GSB/CR/visiteur/<int:Id>")
def cr_by_visiteur(Id):
    cursor = connexion('api.db').cursor()
    sql_CR = """
    SELECT CR.Id, M.Civilite || ' ' || M.Nom || ' ' || M.Prenom AS Medecin,  CR.Date, CR.Motif, CR.Bilan
    FROM Compte_rendu CR
    JOIN Medecins M ON CR.Medecin_id = M.Id
    WHERE CR.Visiteur_id = """ + str(Id)

    try:
        cursor.execute(sql_CR)
    except sqlite3.Error as error:
        return "Error while connecting to sqlite " + error

    result_CR = cursor.fetchall() 
    if len(result_CR) == 0:
        return Response('{"error" : "Aucun enregistrement pour l\'ID ' + str(Id) + '"}', status=400, mimetype='application/json')
    output_CR = [dict(ix) for ix in result_CR]

    cpt = 0
    for cr in output_CR : 
        sql_Medoc = """
        SELECT Medicament.Label, Medocs.Nombre
        FROM Medocs
        JOIN Medicament ON Medocs.Medicament_id = Medicament.Id
        WHERE Medocs.CR_id = """ + str(cr["Id"])
        # print(sql_Medoc)


        
        try:
            cursor.execute(sql_Medoc)
        except sqlite3.Error as error:
            return "Error while connecting to sqlite " + error

        result_Medoc = cursor.fetchall()
        if len(result_Medoc) != 0:
            output_Medoc = [dict(ix) for ix in result_Medoc]
            output_CR[cpt]["Medoc"] = output_Medoc
        # print(len(result_Medoc) )
            # return Response('{"error" : "Aucun enregistrement pour l\'ID ' + str(Id) + '"}', status=400, mimetype='application/json')
        cpt+=1
    
    cursor.close()
    return Response(json.dumps(output_CR), status=200, mimetype='application/json')


@app.route("/GSB/CR/Insert", methods=['POST'])
def Insert_CR():
    conn = connexion('api.db')
    cursor = conn.cursor()
    cr = request.get_json()
    
    if not cr :
    	if request.headers['Content-Type'] != 'application/json':
    		return 'Le Content-Type doit être application/json', 400
    	else :
        	abort(400)

    filtre = ["Medecin", "Date", "Motif", "Bilan", "Medoc"]
    # champ_maquant = list()
    for el in filtre:
    	if el not in cr.keys():
            # champ_maquant.append(el)
    		return 'Il manque "'+ el +'" dans le JSON', 400
    try:
    	datetime.datetime.strptime(cr["Date"], "%d/%m/%Y")
    except ValueError:
    	return "La Date n'est pas au bon format, le bon format est : DD/MM/YYYY"
    
    # exemple : {"Medecin": 1, "Date": "21/07/2021", "Motif": "Visite", "Bilan": "Bla Bla Bla...", "Medoc": {"1": 1, "2" : 1, "3" : 5}}
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

@app.route("/GSB/connexion", methods=['POST'])
def se_connecter():
    ressources = request.get_json()
    cursor     = connexion('api.db').cursor()
    query      = "SELECT * FROM Visiteurs WHERE login = '{}' AND password = '{}'".format(ressources['login'], ressources['password'])
    cursor.execute(query)
    result = cursor.fetchone()
    if result:
        return str(result["id"])
    else:
        return "False"




######################################################################







# Test des différentes URL, mettre en paramètre de la fonction url_for() le nom de la fonction appelé pour une ROUTE.
# le debug s'affiche sur la console du serveur
# if (str(app.config['ENV']) == 'development'):
    # with app.test_request_context():
    #     url_for('index')
    #     url_for('hello')
    #     url_for('salut_x', name='test')





# **NOTES**
# On peut donner Plusieurs fois la même "route" mais en cas de conflit c'est la première qui sera prise en compte 