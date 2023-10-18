---
description: |
    API documentation for modules: Applivisiteur.

lang: en

classoption: oneside
geometry: margin=1in
papersize: a4

linkcolor: blue
links-as-notes: true
...


    
# Module `Applivisiteur` {#id}






    
## Functions


    
### Function `check_code_status` {#id}




>     def check_code_status(
>         status_code
>     )


Fonction de nettoyage des chaines de caractères

Si la code correspond a une confirmation,
alors on retourne un booléen True
sinon on retourne un booléen False avec un message d'erreur

###### Parameters

**```status_code```** :&ensp;<code>int</code>
:   code que renvoie la api

###### Returns

<code>liste\_retournee</code>
:   &nbsp;



    
### Function `nettoyage_str` {#id}




>     def nettoyage_str(
>         texte,
>         escape=False,
>         lower=False,
>         alphanum=False
>     )


Fonction de nettoyage des chaines de caractères

Si escape, lower et alphanum sont placés en paramètre,
alors les différentes opérations de nettoyage associées seront appliquées

###### Parameters

**```texte```** :&ensp;<code>str</code>, optional
:   Texte cible du nettoyage


**```escape```** :&ensp;<code>str</code>, optional
:   Option pour enlever les échappements


**```lower```** :&ensp;<code>str</code>, optional
:   Option pour mettre le texte en minuscule


**```alphanum```** :&ensp;<code>str</code>, optional
:   Option pour enlever tous les caractères qui ne sont pas du type alphanumérique

###### Returns

<code>texte</code>
:   &nbsp;




    
## Classes


    
### Class `FenetreConnexion` {#id}




>     class FenetreConnexion


class qui crée une fenêtre pour se connecter a l'application

...

#### Attributes

**```champsLogin```** :&ensp;<code>obj</code>
:   un champ de saisie pour le login du visiteur


**```champsMDP```** :&ensp;<code>obj</code>
:   un champ de saisie pour le mot de passe du visiteur


**```loginBouton```** :&ensp;<code>obj</code>
:   un bouton pour permettre de se connecter

#### Methods

connexion (self): 
    methode permettant d'initialiser la connexion avec l'api
aller_vers_fenetre_principale () :
    methode permettant de transitionner de fenetre vers fenetre_principale

constructeur des attributs de l'objet FenetreConnexion


    
#### Ancestors (in MRO)

* [PyQt5.QtWidgets.QDialog](#PyQt5.QtWidgets.QDialog)
* [PyQt5.QtWidgets.QWidget](#PyQt5.QtWidgets.QWidget)
* [PyQt5.QtCore.QObject](#PyQt5.QtCore.QObject)
* [sip.wrapper](#sip.wrapper)
* [PyQt5.QtGui.QPaintDevice](#PyQt5.QtGui.QPaintDevice)
* [sip.simplewrapper](#sip.simplewrapper)





    
#### Static methods


    
##### `Method aller_vers_fenetre_principale` {#id}




>     def aller_vers_fenetre_principale()


Fonction de redirection vers la fenetre principale

###### Returns

<code>None</code>
:   &nbsp;




    
#### Methods


    
##### Method `connexion` {#id}




>     def connexion(
>         self
>     )


Fonction de connexion à l'API

###### Returns

<code>None</code>
:   &nbsp;



    
### Class `FenetreConsultation` {#id}




>     class FenetreConsultation


class pour creer une fenetre qui permet de saisir un compte rendu

...

#### Attributes

**```validerIdRapport```** :&ensp;<code>obj</code>
:   un bouton de validation du rapport


**```retourConsultation```** :&ensp;<code>dict</code>
:   un bouton de fermeture de la fenetre retourConsultation

#### Methods

fermer_fenetre (self) :
    Ferme la fenetre la plus récente
valider_rapport (self) :
    Permet d'afficher toutes les informations du rapport

constructeur des attributs de l'objet FenetreConsultation


    
#### Ancestors (in MRO)

* [PyQt5.QtWidgets.QDialog](#PyQt5.QtWidgets.QDialog)
* [PyQt5.QtWidgets.QWidget](#PyQt5.QtWidgets.QWidget)
* [PyQt5.QtCore.QObject](#PyQt5.QtCore.QObject)
* [sip.wrapper](#sip.wrapper)
* [PyQt5.QtGui.QPaintDevice](#PyQt5.QtGui.QPaintDevice)
* [sip.simplewrapper](#sip.simplewrapper)






    
#### Methods


    
##### Method `fermer_fenetre` {#id}




>     def fermer_fenetre(
>         self
>     )


Fonction de fermeture de la fenetre

###### Returns

<code>None</code>
:   &nbsp;



    
##### Method `valider_rapport` {#id}




>     def valider_rapport(
>         self
>     )


Fonction d'affichage du rapport

###### Returns

<code>None</code>
:   &nbsp;



    
### Class `FenetreInformation` {#id}




>     class FenetreInformation


class pour creer une fenetre qui affiche les informations des médecins

...

#### Attributes

**```SelectionInfo```** :&ensp;<code>obj</code>
:   un objet menu déroulant permettant de choisir entre les infos praticiens et médicamments


**```listWidgetInfo```** :&ensp;<code>obj</code>
:   un objet liste permettant de choisir entre les différentes infos praticiens et médicamments


**```RetourInformation```** :&ensp;<code>obj</code>
:   un objet bouton permettant de fermer la fenetre

#### Methods

sur_changement (self) :
    Change la liste listWidgetInfo avec la bonne table d'informations sélectionnée dans SelectionInfo
fermer_fenetre (self) :
    Ferme la fenetre la plus récente
afficher_informations (self) :
    Affiche les informations des praticiens et des médicamments

constructeur des attributs de l'objet FenetreInformation


    
#### Ancestors (in MRO)

* [PyQt5.QtWidgets.QDialog](#PyQt5.QtWidgets.QDialog)
* [PyQt5.QtWidgets.QWidget](#PyQt5.QtWidgets.QWidget)
* [PyQt5.QtCore.QObject](#PyQt5.QtCore.QObject)
* [sip.wrapper](#sip.wrapper)
* [PyQt5.QtGui.QPaintDevice](#PyQt5.QtGui.QPaintDevice)
* [sip.simplewrapper](#sip.simplewrapper)






    
#### Methods


    
##### Method `afficher_informations` {#id}




>     def afficher_informations(
>         self
>     )


Fonction d'affichage des informations médecins/médicaments

###### Returns

<code>None</code>
:   &nbsp;



    
##### Method `fermer_fenetre` {#id}




>     def fermer_fenetre(
>         self
>     )


Fonction de fermeture de la fenetre

###### Returns

<code>None</code>
:   &nbsp;



    
##### Method `sur_changement` {#id}




>     def sur_changement(
>         self
>     )


Fonction de sélection de l'information demandée

###### Returns

<code>None</code>
:   &nbsp;



    
### Class `FenetreMaitresse` {#id}




>     class FenetreMaitresse


class utilisée pour contenir les autres objets Fenetre

...

#### Attributes

**```stackedWidget```** :&ensp;<code>obj</code>
:   un objet enfant permettant de contenir des objets (ici des fenêtres)


constructeur des attributs de l'objet FenetreMaitresse


    
#### Ancestors (in MRO)

* [PyQt5.QtWidgets.QMainWindow](#PyQt5.QtWidgets.QMainWindow)
* [PyQt5.QtWidgets.QWidget](#PyQt5.QtWidgets.QWidget)
* [PyQt5.QtCore.QObject](#PyQt5.QtCore.QObject)
* [sip.wrapper](#sip.wrapper)
* [PyQt5.QtGui.QPaintDevice](#PyQt5.QtGui.QPaintDevice)
* [sip.simplewrapper](#sip.simplewrapper)






    
### Class `FenetrePrincipale` {#id}




>     class FenetrePrincipale


class pour créer une fenêtre pour se connecter a l'application

...

#### Attributes

**```NomVisiteur```** :&ensp;<code>obj</code>
:   une ligne de texte affichant le nom du visiteur


**```SaisieBouton```** :&ensp;<code>obj</code>
:   un bouton pour permettre de saisir un rapport


**```ConsultationBouton```** :&ensp;<code>obj</code>
:   un bouton pour permettre de consulter les rapport


**```DeconnexionBouton```** :&ensp;<code>obj</code>
:   un bouton pour permettre de se déconnecter


**```InformationsBouton```** :&ensp;<code>obj</code>
:   un bouton pour permettre d'afficher les informations praticiens/médicamments

#### Methods

@staticmethod
aller_vers_fenetre_saisie () :
    methode permettant de transitionner de fenetre vers fenetre_saisie
@staticmethod
aller_vers_fenetre_connexion () :
    methode permettant de transitionner de fenetre vers fenetre_connexion
@staticmethod
aller_vers_fenetre_consultation () :
    methode permettant de transitionner de fenetre vers fenetre_consultation
@staticmethod
aller_vers_fenetre_information () :
    methode permettant de transitionner de fenetre vers fenetre_information

constructeur des attributs de l'objet FenetrePrincipale


    
#### Ancestors (in MRO)

* [PyQt5.QtWidgets.QDialog](#PyQt5.QtWidgets.QDialog)
* [PyQt5.QtWidgets.QWidget](#PyQt5.QtWidgets.QWidget)
* [PyQt5.QtCore.QObject](#PyQt5.QtCore.QObject)
* [sip.wrapper](#sip.wrapper)
* [PyQt5.QtGui.QPaintDevice](#PyQt5.QtGui.QPaintDevice)
* [sip.simplewrapper](#sip.simplewrapper)





    
#### Static methods


    
##### `Method aller_vers_fenetre_connexion` {#id}




>     def aller_vers_fenetre_connexion()


Fonction de redirection vers la fenetre connexion

###### Returns

<code>None</code>
:   &nbsp;



    
##### `Method aller_vers_fenetre_consultation` {#id}




>     def aller_vers_fenetre_consultation()


Fonction de redirection vers la fenetre consultation

###### Returns

<code>None</code>
:   &nbsp;



    
##### `Method aller_vers_fenetre_information` {#id}




>     def aller_vers_fenetre_information()


Fonction de redirection vers la fenetre information

###### Returns

<code>None</code>
:   &nbsp;



    
##### `Method aller_vers_fenetre_saisie` {#id}




>     def aller_vers_fenetre_saisie()


Fonction de redirection vers la fenetre saisie

###### Returns

<code>None</code>
:   &nbsp;




    
### Class `FenetreSaisie` {#id}




>     class FenetreSaisie


class pour creer une fenetre qui permet de saisir un compte rendu

...

#### Attributes

**```praticiens```** :&ensp;<code>dict</code>
:   un dictionnaire de praticiens


**```medicaments```** :&ensp;<code>dict</code>
:   un dictionnaire de medicaments


**```SelectionPraticiens```** :&ensp;<code>obj</code>
:   Liste déroulante pour sélectionner les praticiens

#### Methods

fermer_fenetre (self) :
    Ferme la fenetre la plus récente
ajouter_medicament (self) :
    Permet d'ajouter un médicament sélectionné dans la liste TableauOffreMedicaments
envoyer_rapport (self) :
    Permet d'envoyer toutes les informations sélectionnées a l'API

constructeur des attributs de l'objet FenetreSaisie


    
#### Ancestors (in MRO)

* [PyQt5.QtWidgets.QDialog](#PyQt5.QtWidgets.QDialog)
* [PyQt5.QtWidgets.QWidget](#PyQt5.QtWidgets.QWidget)
* [PyQt5.QtCore.QObject](#PyQt5.QtCore.QObject)
* [sip.wrapper](#sip.wrapper)
* [PyQt5.QtGui.QPaintDevice](#PyQt5.QtGui.QPaintDevice)
* [sip.simplewrapper](#sip.simplewrapper)






    
#### Methods


    
##### Method `ajouter_medicament` {#id}




>     def ajouter_medicament(
>         self
>     )


Fonction d'ajout de médicament dans le rapport'

###### Returns

<code>None</code>
:   &nbsp;



    
##### Method `envoyer_rapport` {#id}




>     def envoyer_rapport(
>         self
>     )


Fonction d'envoi du rapport

###### Returns

<code>None</code>
:   &nbsp;



    
##### Method `fermer_fenetre` {#id}




>     def fermer_fenetre(
>         self
>     )


Fonction de fermeture de la fenetre

###### Returns

<code>None</code>
:   &nbsp;



    
### Class `Visiteur` {#id}




>     class Visiteur(
>         id,
>         nom,
>         prenom,
>         secteur,
>         token
>     )


class utilisee pour contenir les informations du visiteur connecté

...

#### Attributes

**```id```** :&ensp;<code>int</code>
:   &nbsp;


   contient l'id du visiteur
**```nom```** :&ensp;<code>str</code>
:   &nbsp;


   contient le nom du visiteur
**```prenom```** :&ensp;<code>str</code>
:   &nbsp;


   contient le prenom du visiteur
**```secteur```** :&ensp;<code>int</code>
:   &nbsp;


   contient le secteur du visiteur
**```token```** :&ensp;<code>str</code>
:   &nbsp;


   contient le token de session du visiteur

constructeur des attributs de l'objet Visiteur








-----
Generated by *pdoc* 0.10.0 (<https://pdoc3.github.io>).
