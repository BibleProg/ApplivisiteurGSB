from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QApplication, QStackedWidget
from PyQt5.uic import loadUi
from datetime import date
import json
import sys
import requests
import hashlib


# variable contenant l'url de connection
url = "http://127.0.0.1:5000"


class FenetreConnexion(QDialog):
    def __init__(self):
        super(FenetreConnexion, self).__init__()
        loadUi("UI/fenetre_connexion.ui", self)

        self.loginBouton.clicked.connect(self.connexion)
        # self.loginBouton.clicked.connect(self.aller_vers_fenetre_principale)

    def connexion(self):
        # On saisit le mot-de-passe tel qu'il est
        to_hash = self.champsMDP.text()

        # On l'encode
        encoded_str = to_hash.encode()

        # Ensuite, on l'hache grâce aux fonctions de la librairie "hashlib"
        hash_obj = hashlib.blake2b(encoded_str)

        # Enfin, on le convertit en une valeur hexadécimale
        hexa_value = hash_obj.hexdigest()
        url2 = url + '/GSB/connexion'
        payload = json.dumps({"login": self.champsLogin.text(),"password": hexa_value})
        headers = {'Content-Type': 'application/json'}

        response = requests.request("POST", url2, headers=headers, data=payload)
        check = response.text
        if check != "False" :
            self.aller_vers_fenetre_principale()


    # la méthode statique permet de prévenir la fonction d'altérer la class
    @staticmethod
    def aller_vers_fenetre_principale():
        fenetre_principale = FenetrePrincipale()
        widget.addWidget(fenetre_principale)
        widget.setCurrentIndex(widget.currentIndex()+1)


class FenetrePrincipale(QDialog):
    def __init__(self):
        super(FenetrePrincipale, self).__init__()
        loadUi("UI/fenetre_principale.ui", self)

        self.saisieBouton.clicked.connect(self.aller_vers_fenetresaisie)
        self.consultationBouton.clicked.connect(self.aller_vers_fenetre_consultation)
        self.deconnexion.clicked.connect(self.aller_vers_fenetre_connexion)

    @staticmethod
    def aller_vers_fenetresaisie():
        fenetre_saisie = FenetreSaisie()
        widget.addWidget(fenetre_saisie)
        widget.setCurrentIndex(widget.currentIndex()+1)

    @staticmethod
    def aller_vers_fenetre_connexion():
        fenetre_connexion = FenetreConnexion()
        widget.addWidget(fenetre_connexion)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    @staticmethod
    def aller_vers_fenetre_consultation():
        fenetre_consultation = FenetreConsultation()
        widget.addWidget(fenetre_consultation)
        widget.setCurrentIndex(widget.currentIndex()+1)


class FenetreSaisie(QDialog):
    def __init__(self):
        super(FenetreSaisie, self).__init__()
        loadUi("UI/fenetre_saisie_rapport.ui", self)

        # je renome la fenetre
        self.setWindowTitle("AppliVisiteur")

        # dictionnaire des praticiens et des médicaments
        self.praticiens = {}
        self.medicaments = {}

        # requete pour obtenir les medecins
        requete = requests.get(url + '/GSB/medecin')
        medecins_json = json.loads(requete.text)
        del requete

        # creation d'un dictionnaire pour lier les noms des praticiens avec leur id
        for i in range(len(medecins_json)):
            nom_total = str(medecins_json[i]['Prenom'] + ' ' + medecins_json[i]['Nom'])
            self.praticiens[nom_total] = medecins_json[i]['Id']

        # j'ordonne les noms des praticiens par ordre alphabetique
        self.praticiens_ordonnes = sorted(self.praticiens.keys(), key=lambda x: x.lower())
        for nom_praticien in self.praticiens_ordonnes:
            self.selectionPraticiens.addItem(nom_praticien)

        # création d'un élément null par défaut, ce n'est qu'un simple string
        self.selectionMedicamentNom.addItem('-Aucun-')

        # requete pour obtenir les médicaments
        requete = requests.get(url + '/GSB/medicament')
        medicaments_json = json.loads(requete.text)
        del requete

        # creation d'un dictionnaire pour lier les noms des médicaments avec leur nombre
        for j in range(len(medicaments_json)):
            self.medicaments[medicaments_json[j]["Label"]] = medicaments_json[j]["Id"]

        # j'ordonne les noms des médicaments par ordre alphabetique
        self.medicaments_ordonnes = sorted(self.medicaments.keys(), key=lambda x: x.lower())
        for nom_medicaments in self.medicaments_ordonnes:
            self.selectionMedicamentNom.addItem(nom_medicaments)

        # éléments titres des colones
        # mise en place des colones
        self.colone1_TableauOffreMedicaments = QTableWidgetItem()
        self.colone2_TableauOffreMedicaments = QTableWidgetItem()
        self.tableauOffreMedicaments.setColumnCount(2)

        # titrage des éléments
        self.colone1_TableauOffreMedicaments.setText("Médicament")
        self.colone2_TableauOffreMedicaments.setText("Quantité")

        # positionnement des éléments titres dans le tableau
        self.tableauOffreMedicaments.setHorizontalHeaderItem(0, self.colone1_TableauOffreMedicaments)
        self.tableauOffreMedicaments.setHorizontalHeaderItem(1, self.colone2_TableauOffreMedicaments)

        # mise a jour de la date à la date du jour
        aujourdhui = date.today()
        aujourdhui_formate = aujourdhui.strftime("%d/%m/%Y")
        qdate_aujourdhui_formate = QDate.fromString(aujourdhui_formate, "dd/MM/yyyy")
        self.dateRapport.setDate(qdate_aujourdhui_formate)

        # bouton d'ajout de l'échantillon
        self.boutonAjouterMedicament.clicked.connect(self.ajouter_medicament)

        # attribut bouton pour valider ou non le formulaire
        self.boutonFormulaire.accepted.connect(self.envoyer_rapport)
        self.boutonFormulaire.rejected.connect(self.fermer_fenetre)

    # fonction pour détruire la page
    def fermer_fenetre(self):
        widget.removeWidget(widget.currentWidget())
        self.reject()

    # fonction pour ajouter des medicaments a la liste
    def ajouter_medicament(self):

        # si il y a des éléments de sélectionnés
        if self.selectionMedicamentNom.currentText() != "-Aucun-" and self.selectionMedicamentQuantite.text() != "":

            # je crée un dictionnaire contenant tous les médicaments choisis
            liste_medicament_enregistre = {}
            for i in range(0, self.tableauOffreMedicaments.rowCount()):
                liste_medicament_enregistre[self.tableauOffreMedicaments.item(i, 0).text()] = i

            # si le médicament n'a pas déjà été entré, je l'intègre
            if self.selectionMedicamentNom.currentText() not in liste_medicament_enregistre.keys():
                self.tableauOffreMedicaments.insertRow(self.tableauOffreMedicaments.rowCount())
                self.tableauOffreMedicaments.setItem(self.tableauOffreMedicaments.rowCount() - 1, 0,
                                                     QTableWidgetItem(self.selectionMedicamentNom.currentText()))
                self.tableauOffreMedicaments.setItem(self.tableauOffreMedicaments.rowCount() - 1, 1,
                                                     QTableWidgetItem(self.selectionMedicamentQuantite.text()))

            # sinon je modifie la valeur de la quantité
            else:
                print(liste_medicament_enregistre[self.selectionMedicamentNom.currentText()])
                self.tableauOffreMedicaments.item(liste_medicament_enregistre[self.selectionMedicamentNom.currentText()], 1)\
                    .setText(self.selectionMedicamentQuantite.text())
            del liste_medicament_enregistre
        else:
            print("il manque des informations pour pouvoir ajouter un échantillon")

    # fonction qui va envoyer les informations validées du formulaire
    def envoyer_rapport(self):

        # je collecte l'ensemble des médicaments
        liste_offre_medicaments = {}
        for i in range(self.tableauOffreMedicaments.rowCount()):
            liste_offre_medicaments[
                self.medicaments[self.tableauOffreMedicaments.item(i, 0).text()]] = self.tableauOffreMedicaments.item(i,1).text()

        # debugging
        print("Praticien: {0}".format(self.selectionPraticiens.currentText()),
              "Date du rapport: {0}".format(self.dateRapport.text()),
              "Motif: {0}".format(self.motif.text()),
              "Bilan: {0}".format(self.bilan.toPlainText()),
              "Enorme: {0}".format(liste_offre_medicaments))

        # je construis un dictionnaire pour l'envoyer sous format Json
        rapport_json = {"Medecin": self.praticiens[self.selectionPraticiens.currentText()],
                        "Date": self.dateRapport.text(),
                        "Motif": self.motif.text(),
                        "Bilan": self.bilan.toPlainText(),
                        "Medoc": liste_offre_medicaments}
        requete = requests.post(url+'/GSB/CR/Insert',
                                json=rapport_json,
                                headers={'Content-Type': 'application/json'})
        print(requete.status_code)
        print(requete.text)
        self.fermer_fenetre()


class FenetreConsultation(QDialog):
    def __init__(self):
        super(FenetreConsultation, self).__init__()
        loadUi("UI/fenetre_consultation_rapport.ui", self)

        self.setWindowTitle("AppliVisiteur")

        self.colone1_TableauOffreMedicaments = QTableWidgetItem()
        self.colone2_TableauOffreMedicaments = QTableWidgetItem()

        self.tableauOffreMedicaments.setColumnCount(2)

        self.colone1_TableauOffreMedicaments.setText("Medicament")
        self.colone2_TableauOffreMedicaments.setText("Quantite")
        self.tableauOffreMedicaments.setHorizontalHeaderItem(0, self.colone1_TableauOffreMedicaments)
        self.tableauOffreMedicaments.setHorizontalHeaderItem(1, self.colone2_TableauOffreMedicaments)

        self.validerIdRapport.clicked.connect(self.valider_rapport)
        self.retourConsultation.clicked.connect(self.fermer_fenetre)

    def fermer_fenetre(self):
        widget.removeWidget(widget.currentWidget())
        self.reject()

    def valider_rapport(self):

        # je fais une requete pour obtenir le rapport avec l'ID précédement obtenu
        requete = requests.get(url + '/GSB/CR/' + str(self.idRapport.value()) + '/')
        rapport_json = json.loads(requete.text)

        # j'attribut les valeurs aux champs adéquats
        self.selectionPraticien.setText(rapport_json['Medecin'])
        self.dateRapport.setText(rapport_json["Date"])
        self.motif.setText(rapport_json["Motif"])
        self.bilan.setPlainText(rapport_json["Bilan"])

        # je remplis la liste des médicaments avec les données du JSON
        for i in range(0, len(rapport_json["Medoc"])):
            self.tableauOffreMedicaments.insertRow(self.tableauOffreMedicaments.rowCount())
            self.tableauOffreMedicaments.setItem(self.tableauOffreMedicaments.rowCount() - 1, 0,
                                                 QTableWidgetItem(rapport_json["Medoc"][i]["Label"]))
            self.tableauOffreMedicaments.setItem(self.tableauOffreMedicaments.rowCount() - 1, 1,
                                                 QTableWidgetItem(str(rapport_json["Medoc"][i]["Nombre"])))


app = QApplication(sys.argv)
widget = QStackedWidget()
win = FenetreConnexion()
widget.addWidget(win)
widget.show()

try:
    sys.exit(app.exec_())

finally:
    print("sortie")
