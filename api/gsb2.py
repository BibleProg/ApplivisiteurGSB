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


class Medecin:
    
    def liste():
        connexion = Connexion()
        curseur   = connexion.seconnecter('api.db').cursor()
        
        req_liste_med = "SELECT * from Medecins ORDER BY Nom"
        curseur.execute(sql)
        result = curseur.fetchall()
        
        if len(result) == 0:
            curseur.close()
            return False
        
        curseur.close()
        return json.dumps([dict(ix) for ix in result])
    
    def information(id):
        req_liste_med = "SELECT * from Medecins ORDER BY Nom"


class Medicament:

    def liste():
        connexion = Connexion()
        curseur   = connexion.seconnecter('api.db').cursor()
        req_liste_medicament = "SELECT * from Medicament"
        curseur.execute(sql)
        result = curseur.fetchall()
        if len(result) == 0:
            curseur.close()
            return False
        
        curseur.close()
        return json.dumps([dict(ix) for ix in result])

class CR:

    last_error = str()

    def get_CR(Id):

        connexion = Connexion()
        curseur   = connexion.seconnecter('api.db').cursor()

        sql_CR = """
        SELECT CR.Id, M.Civilite || ' ' || M.Nom || ' ' || M.Prenom AS Medecin,  CR.Date, CR.Motif, CR.Bilan
        FROM Compte_rendu CR
        JOIN Medecins M ON CR.Medecin_id = M.Id
        WHERE CR.Id = ?""" 

        sql_Medoc = """
        SELECT Medicament.Label, Medocs.Nombre
        FROM Medocs
        JOIN Medicament ON Medocs.Medicament_id = Medicament.Id
        WHERE Medocs.CR_id = ?"""

        try:
            cruseur.execute(sql_CR, (Id))
        except sqlite3.Error as error:
            self.last_error = error
            return False

        result_CR = curseur.fetchall() 

        if len(result_CR) == 0:
            self.last_error = "Aucun enregistrement pour l'Id : {}".format(Id)
            return False
        output_CR = [dict(ix) for ix in result_CR][0]

        try:    
            curseur.execute(sql_Medoc)
        except sqlite3.Error as error:
            self.last_error = error
            return False
        
        result_Medoc = curseur.fetchall()

        if len(result_Medoc) == 0:
            self.last_error = "Aucun enregistrement pour l'Id : {}".format(Id)
            return False

        output_Medoc = [dict(ix) for ix in result_Medoc]
        output_CR["Medoc"] = output_Medoc

        curseur.close()
        return Response(json.dumps(output_CR), status=200, mimetype='application/json')

    def get_CR_by_medecin(Id_med):

        connexion = Connexion()
        curseur   = connexion.seconnecter('api.db').cursor()
        
        sql_CR = """
        SELECT CR.Id, M.Civilite || ' ' || M.Nom || ' ' || M.Prenom AS Medecin,  CR.Date, CR.Motif, CR.Bilan
        FROM Compte_rendu CR
        JOIN Medecins M ON CR.Medecin_id = M.Id
        WHERE CR.Medecin_id = ?""" 

        sql_Medoc = """
        SELECT Medicament.Label, Medocs.Nombre
        FROM Medocs
        JOIN Medicament ON Medocs.Medicament_id = Medicament.Id
        WHERE Medocs.CR_id = ?"""

        # Tout les rapports du medecin
        pass
    def get_CR_by_visiteur(Id_vis):
        # Tout les rapports du viditeur
        pass




    

class Connexion:
    
    def seconnecter(db_name)
        try:
            sqliteConnection             = sqlite3.connect(db_name)
            sqliteConnection.row_factory = sqlite3.Row
            cursor                       = sqliteConnection.cursor()

        except sqlite3.Error as error:
            print("Erreur de connexion à la base de donnée", error)
            return False

        return sqliteConnection

################################LINKS_HELPER####################################

@app.route("/links")
def list_routes():
    routes = ''

    for rule in app.url_map.iter_rules():
        routes += "<a href='" + str(rule) + "'>" + escape(str(rule)) + "</a>"
        routes += "<br>"

    return routes

#############################GSB_POC##################################

@app.route("/GSB/medecin")
def medecin():
    
    medecin   = Medecin()
    liste_med = medecin.liste()

    if liste_med:
        return Response(liste_med, status=202, mimetype='application/json')
    else:
        return Response('{"erreur" : "Impossible de lister les medecins de la base de donnée"}', status=404, , mimetype='application/json')
    

@app.route("/GSB/medicament")
@app.route("/GSB/medicament/<int:Id>/")
def medicament():

    medicament   = Medicament()
    liste_medicament = medicament.liste()

    if liste_medicament:
        return Response(liste_medicament, status=202, mimetype='application/json')
    else:
        return Response('{"error" : "Impossible de lister les medicaments de la base de donnée"}', status=404, mimetype='application/json')

@app.route("/GSB/CR/<int:Id>/")
@app.route("/GSB/CR/<int:Id>")
def CR(Id = 0):
    cursor = connexion('api.db').cursor()

    
    
    
    return output_CR  

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
    if len(Medoc_list) > 2 :
        return 'Un compte rendu ne peut avoir que 2 echantillons max !! Ici '+ lstr(en(Medoc_list)), 400

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