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
from flask import Response
from flask import session
# from flask.ext.session import Session

from html import escape
from random import randint

from faker import Faker
from faker.providers import DynamicProvider


import pyodbc
import json
import datetime
import hashlib
import unicodedata
import sys 

app = Flask(__name__)
app.config.from_object(__name__)
app.config['ENV'] = 'development'
app.config['PERMANENT_SESSION_LIFETIME'] = 365
app.secret_key = 'secret'
app.config['DATABASE'] = 'SQLITE'
# Session(app)

@app.route('/')
def hello():
    """
    S'execute lorsqu'on appelle la racine du serveur.
    Redirige vers la route /links.
    
    """
    return redirect("/links", code=302)

@app.route("/links")
def list_routes():
    """
    Liste les routes existantes dans l'API.
    
    Returns:
        Un DOM HTML.
    """
    routes = ''

    for rule in app.url_map.iter_rules():
        routes += "<a href='" + str(rule) + "'>" + escape(str(rule)) + "</a>"
        routes += "<br>"

    return routes


def log(text, loglevel=0):
    """
    Fonction de logging.

    Args:
        text (string): le message du log
    """
    loglevel_label = {0 : "INFO    ", 1 : "WARNING ", 2 : "ERROR   "}

    date_heure = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    if "username" in session :
        username   = session["username"].ljust(24)
    else:
        username   = "None".ljust(24)
    url        = request.full_path.ljust(20)
    radr       = request.remote_addr
    entete     = date_heure + " " + username + " " + url + " " + radr + " "
    log        = entete + loglevel_label[loglevel] + text +"\n"
    with open("log/api.log", "a") as f:
        f.write(log)
def get_session():
    """ 
    Check si l'utilisateur s'est connecté avant d'accéder à une ressource (fonction appelée à chaque route).

    Returns:
        bool: l'utilisateur est bien connecté
        erreur: code http 401
    """
    if not "id" in session:
        log("A tenté d'acceder à une ressource sans être connecté")
        abort(401)
    elif str(session['admin']) == '0':
        log("l'utilisateur n'est pas autorisé à accéder à cette ressource")
        abort(401)
    log("l'utilisateur à accedé à une ressources")
    return True

def remove_accents(input_str):
    """
    Purge une chaine de caractères en enlevants les accents.

    Args:
        input_str (string): la chaine à purger
    
    Returns:
        string: input_str sans accents
    """
    nkfd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

def connexion(db_name):
    """
    Fonction de connexion à la base de donnée, elle est appelé à chaque nouvelle connexion.\n
    !!! Le driver ODBC SQLite3 est necessaire à son execution.\n
    !!! La base de donnée doit impérativement se trouver dans ./BDD/

    Args:
        db_name (string): le nom de la base de donnée à laquelle se connecter
    
    Returns:
        object: objet pyodbc 
    """
    
    
    if app.config['DATABASE'] == 'SQLITE':
        dir_path = './BDD/'
        db_path  = dir_path + db_name
        cnxn = pyodbc.connect("Driver=SQLite3 ODBC Driver;Database=" + db_path)
    
    elif app.config['DATABASE'] == 'MYSQL':
        username = "gsb"
        password = "157rmllp"
        database = "Applivisiteur"
        driver   = "MariaDB ODBC 3.0 Driver"
        server   = "localhost"
        cnxn = pyodbc.connect(f"Driver={driver};Database={database};Server={server};Uid={username};pwd={password}")
    
    return cnxn

def query(sql, arg=[], many=False):
    """
    Fonction générale utilisée pour executer les requtêtes sql sur la base de donnée

    Args:
        sql  (string): Ordre SQL à executer
        arg  (list, optional): Liste des arguments de la requête SQL
        many (bool, optional): booleen qui indique si il faut executer la requete pour chaques éléments de arg
    
    Returns:
        dict: Retourne un dictionnaire avec le nom des champs de la table en clé et la valeur du champ en valeur.
        bool: Si il n'y a aucun résultat à la requête retourne False
    """
    try:
        cnxn   = connexion('api.db')
        cursor = cnxn.cursor()
    except pyodbc.Error as e:
        log(f"error : {e}", 2)
        abort(500, f"error : {e}")

    try:
        if arg:
            
            if many:
                cursor.executemany(sql,arg)
            else:
                cursor.execute(sql,*arg)    
        else:
            cursor.execute(sql)
    except pyodbc.Error as e:
        log(f'error with query : \n {sql} \n |{arg}|', 2)
        cursor.rollback()
        log(f"error : {e}", 2)
        abort(500, f"error : {e}")

    cnxn.commit()

    try:
        res = cursor.fetchall()

        columns = [column[0] for column in cursor.description]
        results = []
        
        if len(res) > 1:
            for row in res:
                results.append(dict(zip(columns, row)))
        else:
            results = dict(zip(columns, res[0]))
    except Exception as e:
        results = 0

    cnxn.close()
    
    return results

@app.route("/ping")
def ping():
    """
    Appelée pour tester la connexion à l'API
    """
    log('PING')
    return "Alive !",200

@app.route("/GSB/medecin/<int:Id>/")
def medecin(Id):
    """
    Execute une recherche de praticien.

    Args:
        Id (int): id du praticien concerné
    
    Returns:
        string: JSON avec toutes les informations du praticien
    """
    get_session()
    sql = "SELECT * FROM Praticiens WHERE Id = " + str(Id) 
    results = query(sql)

    if not results :
        return Response('{"erreur" : "Aucun enregistrement pour l\'ID ' + str(Id) + '"}', status=404, mimetype='application/json')
    
    return Response(json.dumps(results), status=200, mimetype='application/json')
@app.route("/GSB/medecins")  #Praticiens
def medecin_all():
    """
    Execute une recherche sur tout les praticiens.
    
    Returns:
        string: JSON avec toutes les informations de tous les praticiens
    """
    get_session()
    sql = "SELECT * from Praticiens ORDER BY Nom"

    results = query(sql)
    
    return Response(json.dumps(results), status=200, mimetype='application/json')


@app.route("/GSB/medicaments")
def medicaments():
    """
    Execute une recherche sur tout les médicaments.
    
    Returns:
        string: JSON avec toutes les informations de tous les médicaments
    """
    get_session()
    sql = "SELECT * FROM Medicaments"

    result = query(sql)
    if result == 0:
        return Response('{"error" : "Aucun enregistrement pour l\'ID ' + str(Id) + '"}', status=404, mimetype='application/json')

    return Response(json.dumps(result), status=200, mimetype='application/json')
@app.route("/GSB/medicament/<int:Id>/")
def medicament(Id):
    """
    Execute une recherche de médicament.

    Args:
        Id (int): id du médicament concerné
    
    Returns:
        string: JSON avec toutes les informations du médicament
    """
    get_session()
    sql = "SELECT * FROM Medicaments WHERE Id = " + str(Id)

    result = query(sql)
    if result == 0:
        return Response('{"error" : "Aucun enregistrement pour l\'ID ' + str(Id) + '"}', status=404, mimetype='application/json')

    return Response(json.dumps(result), status=200, mimetype='application/json')

# @app.route("/GSB/CR/<int:Id>/")
# def CR(Id):
#     """

#     Recherche un compte rendu.
    
#     Args:
#         Id (int): id du compte rendu
    
#     Returns:
#         string: JSON contenant toutes les informations du compte rendu ainsi que les échantillons associés
#     """
#     get_session()
#     sql_CR = """
#     SELECT CR.Id, M.Civilite || ' ' || M.Nom || ' ' || M.Prenom AS Medecin,  CR.Date, CR.Motif, CR.Bilan
#     FROM Compte_rendu CR
#     JOIN Praticiens M ON CR.Medecin_id = M.Id
#     WHERE CR.Id = """ + str(Id)

#     sql_Medoc = """
#     SELECT Medicaments.Label, Echantillons.Nombre
#     FROM Echantillons
#     JOIN Medicaments ON Echantillons.Medicaments_id = Medicaments.Id
#     WHERE Echantillons.CR_id = """ + str(Id)

#     result_CR = query(sql_CR)
#     if not result_CR:
#         return Response('{"error" : "Aucun enregistrement pour l\'ID ' + str(Id) + '"}', status=404, mimetype='application/json')

#     result_Medoc = query(sql_Medoc)
#     if not result_Medoc:
#         return Response('{"error" : "Aucun enregistrement pour l\'ID ' + str(Id) + '"}', status=404, mimetype='application/json')

#     result_CR["Medoc"] = result_Medoc
    
#     return Response(json.dumps(result_CR), status=200, mimetype='application/json')

@app.route("/GSB/CR/medecin/<int:Id>/")
def cr_by_medecin(Id):
    """
    Recherche de compte rendu par medecin.
    
    Args:
        Id (int): id du medecin
    
    Returns:
        string: JSON contenant toutes les informations du compte rendu ainsi que les échantillons associés
    """
    get_session()
    sql_CR = """
    SELECT CR.Id, M.Civilite || ' ' || M.Nom || ' ' || M.Prenom AS Medecin,  CR.Date, CR.Motif, CR.Bilan
    FROM Compte_rendu CR
    JOIN Praticiens M ON CR.Medecin_id = M.Id
    WHERE CR.Medecin_id = """ + str(Id)

    result_CR = query(sql_CR) 
    if not result_CR:
        return Response('{"error" : "Aucun enregistrement pour l\'ID ' + str(Id) + '"}', status=404, mimetype='application/json')

    cpt = 0
    for cr in result_CR : 
        sql_Medoc = """
        SELECT Medicaments.Label, Echantillons.Nombre
        FROM Echantillons
        JOIN Medicaments ON Echantillons.Medicaments_id = Medicaments.Id
        WHERE Echantillons.CR_id = """ + str(cr["Id"])

        result_Medoc = query(sql_Medoc)

        if not result_Medoc:
            result_CR[cpt]["Medoc"] = result_Medoc
        
        cpt+=1
    
    return Response(json.dumps(result_CR), status=200, mimetype='application/json')

@app.route("/GSB/CR/visiteur")
def cr_by_visiteur():
    """
    Recherche de compte rendu par visiteur.

    Returns:
       string: JSON contenant toutes les informations du compte rendu ainsi que les échantillons associés 
    """
    get_session()
    sql_CR = """
    SELECT CR.Id, M.Civilite || ' ' || M.Nom || ' ' || M.Prenom AS Medecin,  CR.Date, CR.Motif, CR.Bilan
    FROM Compte_rendu CR
    JOIN Praticiens M ON CR.Medecin_id = M.Id
    WHERE CR.Visiteur_id = """ + str(session["id"])


    result_CR = query(sql_CR) 
    if not result_CR:
        return Response('{"error" : "Aucun enregistrement pour l\'utilisateur ' + str(session["id"]) + '"}', status=200, mimetype='application/json')
    cpt = 0
    for cr in result_CR : 
        sql_Medoc = """
        SELECT Medicaments.Label, Echantillons.Nombre
        FROM Echantillons
        JOIN Medicaments ON Echantillons.Medicaments_id = Medicaments.Id
        WHERE Echantillons.CR_id = """ + str(cr["Id"])

        result_Medoc = query(sql_Medoc)
        if not result_Medoc:
            result_CR[cpt]["Medoc"] = result_Medoc
        cpt+=1
    
    return Response(json.dumps(result_CR), status=200, mimetype='application/json')

@app.route("/GSB/CR/Insert", methods=['POST'])
def Insert_CR():
    """
    fonction pour créer un compte rendu, la route attend un JSON 

    method:
        POST

    Param:
        JSON : contient les informations du compte rendu, il doit comporter les champs ["Medecin", "Date", "Motif", "Bilan", "Medoc"]
    
    Returns:
        HTTP CODE: 201, 400
    """
    get_session()
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
    
    query_CR    = "INSERT INTO Compte_rendu(Medecin_id, Date, Motif, Bilan, Visiteur_id) VALUES (?,?,?,?,? )"
    query(query_CR, (cr["Medecin"], cr["Date"], cr["Motif"], cr["Bilan"], session["id"]))

    query_Medoc = "INSERT INTO Echantillons(Medicaments_id, Cr_id, Nombre) VALUES (?,?,?)"
    Medoc_list  = []
    for medoc_id, nombre in cr["Medoc"].items():
        Medoc_list += [(medoc_id, Id, nombre)]

    query(query_Medoc, Medoc_list, many=True)

    log(f"Compte rendu inséré avec l'id : {Id}")

    return f"Compte rendu inséré avec l'id : {Id}", 201

@app.route("/GSB/visiteur/secteur_id/<int:Id>/")
def secteur_by_visiteur(Id):
    """
    Recherche de Secteur par visiteur.
    
    Args:
        Id (int): id du visiteur
    
    Returns:
        integer: id du secteur
    """
    sql_sect = """
    SELECT Secteur_id
    FROM Visiteurs
    WHERE id = """ + str(Id)


    result_sect = query(sql_sect)
    return str(result_sect["Secteur_id"])
    cursor.close()


@app.route("/GSB/connexion", methods=['GET'])
def se_connecter():
    """
    Route utilisée pour s'authentifier auprès de l'API
    
    Returns:
        HTTP CODE: 200, 401
    """
    ressources = request.get_json()
    res      = query("SELECT password, id, Secteur_id, nom, prenom, admin FROM Visiteurs WHERE login = ? ", (ressources['login'],) )

    password      = ressources["password"]
    hash_password = hashlib.md5(password.encode("utf-8")).hexdigest()


    if res:
        user_pass = res["password"]
        if user_pass == hash_password:
            session['username'] = ressources['login']
            session['id']       = res['id']
            session['secteur']  = res['Secteur_id']
            session['admin']    = res['admin']
            
            info_util = dict()
            info_util["id"]      = res["id"]
            info_util["nom"]     = res["nom"]
            info_util["prenom"]  = res["prenom"]
            info_util['secteur'] = res['Secteur_id']

            log("UTILISATEUR CONNECTE")
            
            return Response(json.dumps(info_util), status=200, mimetype='application/json')
            return str(res["id"])
        else:
            log("Tentative de connexion avec : " + ressources["login"])
            return "Mauvais nom d'utilisateur/mot de passe", 401
    else:
        log("Tentative de connexion avec : " + ressources["login"])
        return "Mauvais nom d'utilisateur/mot de passe", 401

@app.route("/utils/hashpass/<password>/")
def hashpass(password):
    """
    Affiche le hash d'une chaine de charatère

    Args:
        password(string): mot de passe à asher
    
    Returns:
        string: le mot de passe ashé
    """
    
    hash_password = hashlib.md5(password.encode("utf-8")).hexdigest()

    return str(hash_password)

###OUTILS DE GENERATION DE DONNEE POUR GSB#########

@app.route("/faker/praticien")
def fake_prat():
    """
    Génère 50 faux particiens
    """
    fake = Faker("fr_FR")
    provider = DynamicProvider(provider_name="civilite", elements=["Mr", "Me"])
    fake.add_provider(provider)

    for i in range(50):
        fake_adress = fake.address().split('\n') # ['chemin Jacqueline Noël', '22704 ThomasVille']
        
        fake_ville   = fake_adress[1].split(' ')[1]
        fake_CP      = fake_adress[1].split(' ')[0]
        fake_adresse = fake_adress[0]

        fake_name   = fake.name().split(' ', 1) # ['Audrey', 'de Clerc']

        fake_nom       = fake_name[1]
        fake_prenom    = fake_name[0]
        fake_civilite  = fake.civilite()

        fake_secteur = randint(1,5)
        fake_coef    = randint(1,10)
        sql = f"""INSERT INTO Praticiens(Prenom, Nom, Civilite, Adresse, CP, Ville, CoefNotoriete, Secteur_id) 
        VALUES ('{fake_prenom}', '{fake_nom}', '{fake_civilite}', '{fake_adresse}', '{fake_CP}',' {fake_ville}', '{fake_coef}', '{fake_secteur}')"""
        query(sql)



    return "50 praticiens insérés"

@app.route("/faker/CR")
def fake_cr():
    """
    Genere 50 faux comptes rendus
    """
    fake  = Faker("fr_FR")
    fake2 = Faker('it_IT')
    
    sql = "SELECT Id FROM Praticiens"
    praticien_ids = [el["Id"] for el in query(sql)]
    provider = DynamicProvider(provider_name="praticien", elements=praticien_ids)
    fake.add_provider(provider)

    sql = "SELECT Id FROM Visiteurs"
    visiteur_ids = [el["id"] for el in query(sql)]
    provider = DynamicProvider(provider_name="visiteur", elements=visiteur_ids)
    fake.add_provider(provider)

    sql = "SELECT Id FROM Medicaments"
    medocs_ids = [el["Id"] for el in query(sql)]
    provider = DynamicProvider(provider_name="medicament", elements=medocs_ids)
    fake.add_provider(provider)

    for i in range(50):
        pract_id = fake.praticien()
        visit_id = fake.visiteur()
        date     = fake.date_between('-10y','today').strftime("%d/%m/%Y")
        motif    = "Visite"
        bilan    = fake2.text(500)

        sql = "SELECT seq FROM sqlite_sequence WHERE name = 'Compte_rendu'"
        Id = query(sql)["seq"] + 1

        query_CR    = "INSERT INTO Compte_rendu(Medecin_id, Date, Motif, Bilan, Visiteur_id) VALUES (?,?,?,?,?)"
        query(query_CR, (pract_id, date, motif, bilan, visit_id))

        for y in range(randint(1,10)):
            medicament  = fake.medicament() 
            nombre      = randint(1,5)
            query_Medoc = "INSERT INTO Echantillons(Medicaments_id, Cr_id, Nombre) VALUES (?,?,?)"
            query(query_Medoc, (medicament, Id, nombre))


        
    return "50 comptes rendus créés"

@app.route("/faker/visiteur")
def fake_visiteur():
    """
    Génère 50 faux visiteurs
    """
    fake  = Faker("fr_FR")
    output = ''
    for i in range(50):
        date = fake.date_between('-10y','today')
        date_embauche = date.strftime("%d/%m/%Y")
        mdp  = date.strftime("%d-%b-%Y")

        fake_name      = fake.name().split(' ', 1) # ['Audrey', 'de Clerc']
        fake_nom       = fake_name[1]
        fake_prenom    = fake_name[0]

        login = remove_accents(fake_nom).replace(' ', '')
        admin = 1
        secteur = randint(1,5)

        sql = "INSERT INTO Visiteurs(login,password,Secteur_id, nom, prenom, date_embauche, admin) VALUES(?,?,?,?,?,?,?)"
        try:
            query(sql, (login, mdp, secteur, fake_nom, fake_prenom, date_embauche, admin))
        except Exception as e:
            pass
        output += f'<br> {login} {mdp} {secteur} {fake_nom} {fake_prenom} {date_embauche} {admin} '
        
    return output

        

    



######################################################################






# Test des différentes URL, mettre en paramètre de la fonction url_for() le nom de la fonction appelé pour une ROUTE.
# le debug s'affiche sur la console du serveur
# if (str(app.config['ENV']) == 'development'):
#     with app.test_request_context():
#         try:
#             url_for('medecin_all')
#             url_for('medecin', Id=1)
#             url_for('medicaments')
#             url_for('medicament', Id=1)
#             url_for('CR', Id=1)
#             url_for('cr_by_visiteur', Id=1)
#             url_for('cr_by_medecin', Id=1)
#         except Exception as e:
#             print(f"/!\\ /!\\ /!\\ ERREUR /!\\ /!\\ /!\\ \n################################# \n{e} \n#################################")


if __name__ == '__main__':
    app.run(port=5000,debug=True)


# **NOTES**
# On peut donner Plusieurs fois la même "route" mais en cas de conflit c'est la première qui sera prise en compte 