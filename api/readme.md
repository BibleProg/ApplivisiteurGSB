---
description: |
    API documentation for modules: gsb.

lang: en

classoption: oneside
geometry: margin=1in
papersize: a4

linkcolor: blue
links-as-notes: true
...


    
# Module `gsb` {#id}






    
## Functions


    
### Function `CR` {#id}




>     def CR(
>         Id
>     )


Recherche un compte rendu.


Args
-----=
**```Id```** :&ensp;<code>int</code>
:   id du compte rendu



Returns
-----=
<code>string</code>
:   JSON contenant toutes les informations du compte rendu ainsi que les échantillons associés



    
### Function `Insert_CR` {#id}




>     def Insert_CR()


fonction pour créer un compte rendu, la route attend un JSON 

method:
    POST


Param
-----=
JSON : contient les informations du compte rendu, il doit comporter les champs ["Medecin", "Date", "Motif", "Bilan", "Medoc"]


Returns
-----=
<code>HTTP CODE</code>
:   201, 400



    
### Function `connexion` {#id}




>     def connexion(
>         db_name
>     )


Fonction de connexion à la base de donnée, elle est appelé à chaque nouvelle connexion.

!!! Le driver ODBC SQLite3 est necessaire à son execution.

!!! La base de donnée doit impérativement se trouver dans ./BDD/


Args
-----=
**```db_name```** :&ensp;<code>string</code>
:   le nom de la base de donnée à laquelle se connecter



Returns
-----=
<code>object</code>
:   objet pyodbc



    
### Function `cr_by_medecin` {#id}




>     def cr_by_medecin(
>         Id
>     )


Recherche de compte rendu par medecin.


Args
-----=
**```Id```** :&ensp;<code>int</code>
:   id du medecin



Returns
-----=
<code>string</code>
:   JSON contenant toutes les informations du compte rendu ainsi que les échantillons associés



    
### Function `cr_by_visiteur` {#id}




>     def cr_by_visiteur(
>         Id
>     )


Recherche de compte rendu par visiteur.


Args
-----=
**```Id```** :&ensp;<code>int</code>
:   id du visiteur



Returns
-----=
<code>string</code>
:   JSON contenant toutes les informations du compte rendu ainsi que les échantillons associés



    
### Function `fake_cr` {#id}




>     def fake_cr()


Genere 50 faux comptes rendus

    
### Function `fake_prat` {#id}




>     def fake_prat()


Génère 50 faux particiens

    
### Function `fake_visiteur` {#id}




>     def fake_visiteur()


Génère 50 faux visiteurs

    
### Function `get_session` {#id}




>     def get_session()


Check si l'utilisateur s'est connecté avant d'accéder à une ressource (fonction appelée à chaque route).


Returns
-----=
<code>bool</code>
:   l'utilisateur est bien connecté


<code>erreur</code>
:   code http 401



    
### Function `hashpass` {#id}




>     def hashpass(
>         password
>     )


Affiche le hash d'une chaine de charatère


Args
-----=
**```password```** :&ensp;<code>string</code>
:   mot de passe à asher



Returns
-----=
<code>string</code>
:   le mot de passe ashé



    
### Function `hello` {#id}




>     def hello()


S'execute lorsqu'on appelle la racine du serveur.
Redirige vers la route /links.

    
### Function `list_routes` {#id}




>     def list_routes()


Liste les routes existantes dans l'API.


Returns
-----=
Un DOM HTML.

    
### Function `log` {#id}




>     def log(
>         text
>     )


Fonction de logging.


Args
-----=
**```text```** :&ensp;<code>string</code>
:   le message du log



    
### Function `medecin` {#id}




>     def medecin(
>         Id
>     )


Execute une recherche de praticien.


Args
-----=
**```Id```** :&ensp;<code>int</code>
:   id du praticien concerné



Returns
-----=
<code>string</code>
:   JSON avec toutes les informations du praticien



    
### Function `medecin_all` {#id}




>     def medecin_all()


Execute une recherche sur tout les praticiens.


Returns
-----=
<code>string</code>
:   JSON avec toutes les informations de tous les praticiens



    
### Function `medicament` {#id}




>     def medicament(
>         Id
>     )


Execute une recherche de médicament.


Args
-----=
**```Id```** :&ensp;<code>int</code>
:   id du médicament concerné



Returns
-----=
<code>string</code>
:   JSON avec toutes les informations du médicament



    
### Function `medicaments` {#id}




>     def medicaments()


Execute une recherche sur tout les médicaments.


Returns
-----=
<code>string</code>
:   JSON avec toutes les informations de tous les médicaments



    
### Function `ping` {#id}




>     def ping()


Appelée pour tester la connexion à l'API

    
### Function `query` {#id}




>     def query(
>         sql,
>         arg=[],
>         many=False
>     )


Fonction générale utilisée pour executer les requtêtes sql sur la base de donnée.


Args
-----=
**```sql```** :&ensp;<code>string</code>
:   Ordre SQL à executer


**```arg```** :&ensp;<code>list</code>, optional
:   Liste des arguments de la requête SQL


**```many```** :&ensp;<code>bool</code>, optional
:   booleen qui indique si il faut executer la requete pour chaques éléments de arg



Returns
-----=
<code>dict</code>
:   Retourne un dictionnaire avec le nom des champs de la table en clé et la valeur du champ en valeur.


<code>bool</code>
:   Si il n'y a aucun résultat à la requête retourne False



    
### Function `remove_accents` {#id}




>     def remove_accents(
>         input_str
>     )


Purge une chaine de caractères en enlevants les accents.


Args
-----=
**```input_str```** :&ensp;<code>string</code>
:   la chaine à purger



Returns
-----=
<code>string</code>
:   input_str sans accents



    
### Function `se_connecter` {#id}




>     def se_connecter()


Route utilisée pour s'authentifier auprès de l'API


Returns
-----=
<code>HTTP CODE</code>
:   200, 401



    
### Function `secteur_by_visiteur` {#id}




>     def secteur_by_visiteur(
>         Id
>     )


Recherche de Secteur par visiteur.


Args
-----=
**```Id```** :&ensp;<code>int</code>
:   id du visiteur



Returns
-----=
<code>integer</code>
:   id du secteur





-----
Generated by *pdoc* 0.10.0 (<https://pdoc3.github.io>).
