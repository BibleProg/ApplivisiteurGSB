from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QApplication, QMainWindow
from PyQt5.uic import loadUi
from datetime import date
import json
import sys
import requests
from PyQt5.QtGui import QIcon

# variable contenant l'url de connection
import configparser
config = configparser.ConfigParser()
config.read('config.ini')
serveur = config['SERVEUR']

id_visiteur = ''


class FenetreMaitresse(QMainWindow):
    """
    class utilisee pour contenir les autres objets fenetre

    ...

    Attributes
    ----------
    stackedWidget : obj
        un objet enfant permettant de contenir des objets (ici des fenetres)

    """
    def __init__(self):
        """
        Parameters
        ----------
        stackedWidget : obj
            un objet permettant de contenir des objets (ici des fenetres)
        """
        super(FenetreMaitresse, self).__init__()
        loadUi("UI/fenetre_maitresse.ui", self)
        fenetre_connexion = FenetreConnexion()
        # fenetre_connexion = FenetrePrincipale()
        self.stackedWidget.addWidget(fenetre_connexion)
        self.stackedWidget.setCurrentWidget(fenetre_connexion)




class FenetreInformation(QDialog):
    """
    class pour creer une fenetre qui affiche les informations des médecins

    ...

    Attributes
    ----------
    RobertBouton(afficher_information_praticien()) : obj
        un objet bouton permettant de changer de fenetre
    CelineBouton(afficher_information_praticien()) : obj
        un objet bouton permettant de changer de fenetre
    HugeBouton(afficher_information_praticien()) : obj
        un objet bouton permettant de changer de fenetre
    RetourInformationMedecin(afficher_information_praticien()) : obj
        un objet bouton permettant de fermer la fenetre

    Methods
    -------
    fermer_fenetre(self)
        Ferme la fenetre la plus récente
    afficher_information_medecin(self, id)
        Affiche les informations des praticiens
    """
    def __init__(self):
        """
        Parameters
        ----------
        RobertBouton(afficher_information_praticien()) : obj
            un objet bouton permettant de changer de fenetre
        CelineBouton(afficher_information_praticien()) : obj
            un objet bouton permettant de changer de fenetre
        HugeBouton(afficher_information_praticien()) : obj
            un objet bouton permettant de changer de fenetre
        RetourInformationMedecin(self.fermer_fenetre()) : obj
            un objet bouton permettant de fermer la fenetre
        """
        super(FenetreInformation, self).__init__()
        loadUi("UI/fenetre_information.ui", self)
        self.RetourInformation.clicked.connect(self.fermer_fenetre)

        self.SelectionInfo.addItem('-Praticiens-')
        self.SelectionInfo.addItem('-Médicaments-')

        self.sur_changement()
        self.SelectionInfo.currentTextChanged.connect(self.sur_changement)
        self.listWidgetInfo.itemClicked.connect(self.afficher_information)

    def sur_changement(self):

        self.listWidgetInfo.clear()

        if self.SelectionInfo.currentText() == '-Praticiens-':

            self.infoPraticiens = {}

            requete_info = requests.get(serveur['protocole'] + '://' + serveur['host'] + ':' + serveur['port'] + '/GSB/medecins')
            if requete_info.status_code == 200:

                medecins_json = json.loads(requete_info.text)

                for i in range(len(medecins_json)):
                    nom_total = str(medecins_json[i]['Prenom'] + ' ' + medecins_json[i]['Nom'])
                    self.infoPraticiens[nom_total] = medecins_json[i]

                # j'ordonne les noms des praticiens par ordre alphabetique
                infoPraticiens_ordonnes = sorted(self.infoPraticiens.keys(), key=lambda x: x.lower())

                for nom_praticien in infoPraticiens_ordonnes:
                    self.listWidgetInfo.addItem(nom_praticien)

            else:
                pass

        if self.SelectionInfo.currentText() == '-Médicaments-':

            self.infoMedicament = {}

            requete_info = requests.get(serveur['protocole'] + '://' + serveur['host'] + ':' + serveur['port'] + '/GSB/medicament')
            medicaments_json = json.loads(requete_info.text)

            for i in range(len(medicaments_json)) :
                self.infoMedicament[str(medicaments_json[i]['Label'])] = medicaments_json[i]

            # j'ordonne les noms des praticiens par ordre alphabetique
            self.infoMedicament_ordonnes = sorted(self.infoMedicament.keys(), key=lambda x: x.lower())

            for nom_medicament in self.infoMedicament_ordonnes:
                self.listWidgetInfo.addItem(nom_medicament)

        return 0

    # fonction pour détruire la page
    def fermer_fenetre(self):
        """
        Methods
        -------
        fermer_fenetre(self)
            Ferme la fenetre la plus récente
        """
        win.stackedWidget.removeWidget(self)
        self.reject()

    def afficher_information(self):
        """
        Methods
        -------
        afficher_information_medecin(self, id)
            Affiche les informations des praticiens
        """

        if self.SelectionInfo.currentText() == '-Praticiens-':
            widget_info_medecin = loadUi("UI/widgets/widget_info_medecin.ui")
            self.StackedWidgetInfo.addWidget(widget_info_medecin)
            self.StackedWidgetInfo.setCurrentWidget(widget_info_medecin)

            if self.listWidgetInfo.count() is not None:

                widget_info_medecin.InfoPrenomPraticien.setText(
                    str(self.infoPraticiens[self.listWidgetInfo.currentItem().text()]['Prenom']))
                widget_info_medecin.InfoNomPraticien.setText(
                    str(self.infoPraticiens[self.listWidgetInfo.currentItem().text()]['Nom']))
                widget_info_medecin.InfoCvPraticien.setText(
                    str(self.infoPraticiens[self.listWidgetInfo.currentItem().text()]['Civilite']))
                widget_info_medecin.InfoAdressePraticien.setText(
                    str(self.infoPraticiens[self.listWidgetInfo.currentItem().text()]['Adresse']))
                widget_info_medecin.InfoCPPraticien.setText(
                    str(self.infoPraticiens[self.listWidgetInfo.currentItem().text()]['CP']))
                widget_info_medecin.InfoVillePraticien.setText(
                    str(self.infoPraticiens[self.listWidgetInfo.currentItem().text()]['Ville']))
                widget_info_medecin.InfoCNPraticien.setText(
                    str(self.infoPraticiens[self.listWidgetInfo.currentItem().text()]['CoefNotoriete']))
                widget_info_medecin.InfoSecteurPraticien.setText(
                    str(self.infoPraticiens[self.listWidgetInfo.currentItem().text()]['Secteur_id']))

        if self.SelectionInfo.currentText() == '-Médicaments-':
            widget_info_medicament = loadUi("UI/widgets/widget_info_medicament.ui")
            self.StackedWidgetInfo.addWidget(widget_info_medicament)
            self.StackedWidgetInfo.setCurrentWidget(widget_info_medicament)

            if self.listWidgetInfo.count() is not None:

                widget_info_medicament.InfoLabelPraticien.setText(
                    str(self.infoMedicament[self.listWidgetInfo.currentItem().text()]['Label']))
                widget_info_medicament.InfoDatePraticien.setText(
                    str(self.infoMedicament[self.listWidgetInfo.currentItem().text()]['Date']))
                widget_info_medicament.InfoCompPraticien.setText(
                    str(self.infoMedicament[self.listWidgetInfo.currentItem().text()]['Composition']))
                widget_info_medicament.InfoEffetPraticien.setText(
                    str(self.infoMedicament[self.listWidgetInfo.currentItem().text()]['Effets']))
                widget_info_medicament.InfoCIPraticien.setText(
                    str(self.infoMedicament[self.listWidgetInfo.currentItem().text()]['ContreIndic']))
                widget_info_medicament.InfoPrixPraticien.setText(
                    str(self.infoMedicament[self.listWidgetInfo.currentItem().text()]['Prix']))
                widget_info_medicament.InfoStockPraticien.setText(
                    str(self.infoMedicament[self.listWidgetInfo.currentItem().text()]['Stock']))


class FenetreConnexion(QDialog):
    """
        class qui creer une fenetre pour se connecter a l'application

        ...

        Attributes
        ----------
        champsMDP : obj
            a formatted string to print out what the animal says
        name : str
            the name of the animal
        sound : str
            the sound that the animal makes
        num_legs : int
            the number of legs the animal has (default 4)

        Methods
        -------
        says(sound=None)
            Prints the animals name and what sound it makes
        """
    def __init__(self):
        super(FenetreConnexion, self).__init__()
        loadUi("UI/fenetre_connexion.ui", self)

        self.loginBouton.clicked.connect(self.connexion)
        # self.loginBouton.clicked.connect(self.aller_vers_fenetre_principale)

    def connexion(self):

        global id_visiteur

        # je construis un dictionnaire pour l'envoyer sous format Json
        login_json = {"Login": self.champsLogin.text(),
                        "Password": self.champsMDP.text()}
        requete = requests.get(
            serveur['protocole'] + '://' + serveur['host'] + ':' + serveur['port'] + '/GSB/connexion',
            json=login_json,
            headers={'Content-Type': 'application/json'})

        if requete.status_code == '200':
            infos_visiteur = json.loads(requete.text)
            id_visiteur = infos_visiteur['Id']
            self.aller_vers_fenetre_principale(infos_visiteur['Nom'], infos_visiteur['Prenom'])
        else:
            self.champsMDP.setText('')


    # la méthode statique permet de prévenir la fonction d'altérer la class
    @staticmethod
    def aller_vers_fenetre_principale(nom, prenom):
        fenetre_principale = FenetrePrincipale(nom, prenom)
        win.stackedWidget.addWidget(fenetre_principale)
        win.stackedWidget.setCurrentWidget(fenetre_principale)


class FenetrePrincipale(QDialog):
    global id_visiteur

    def __init__(self, nom, prenom):
        super(FenetrePrincipale, self).__init__()
        loadUi("UI/fenetre_principale.ui", self)
        self.nom = nom
        self.prenom = prenom

        self.nomVisiteur.setText(self.nom + ' - ' + self.prenom)
        self.SaisieBouton.clicked.connect(self.aller_vers_fenetresaisie)
        self.ConsultationBouton.clicked.connect(self.aller_vers_fenetre_consultation)
        self.DeconnexionBouton.clicked.connect(self.aller_vers_fenetre_connexion)
        self.InformationsBouton.clicked.connect(self.aller_vers_fenetre_information)

    @staticmethod
    def aller_vers_fenetresaisie():
        fenetre_saisie = FenetreSaisie()
        win.stackedWidget.addWidget(fenetre_saisie)
        win.stackedWidget.setCurrentWidget(fenetre_saisie)

    @staticmethod
    def aller_vers_fenetre_connexion():
        fenetre_connexion = FenetreConnexion()
        win.stackedWidget.addWidget(fenetre_connexion)
        win.stackedWidget.setCurrentWidget(fenetre_connexion)

    @staticmethod
    def aller_vers_fenetre_consultation():
        fenetre_consultation = FenetreConsultation()
        win.stackedWidget.addWidget(fenetre_consultation)
        win.stackedWidget.setCurrentWidget(fenetre_consultation)

    @staticmethod
    def aller_vers_fenetre_information():
        fenetre_information = FenetreInformation()
        win.stackedWidget.addWidget(fenetre_information)
        win.stackedWidget.setCurrentWidget(fenetre_information)


class FenetreSaisie(QDialog):
    global id_visiteur
    def __init__(self):
        super(FenetreSaisie, self).__init__()
        loadUi("UI/fenetre_saisie_rapport_layouted.ui", self)

        # dictionnaire des praticiens et des médicaments
        self.praticiens = {}
        self.medicaments = {}

        # requete pour obtenir les medecins
        requete = requests.get(serveur['protocole'] + '://' + serveur['host'] + ':' + serveur['port'] + '/GSB/medecin')
        medecins_json = json.loads(requete.text)
        del requete

        # creation d'un dictionnaire pour lier les noms des praticiens avec leur id
        for i in range(len(medecins_json)):
            nom_total = str(medecins_json[i]['Prenom'] + ' ' + medecins_json[i]['Nom'])
            self.praticiens[nom_total] = {"Id": medecins_json[i]['Id'], "Secteur_id": medecins_json[i]['Secteur_id']}

        # j'ordonne les noms des praticiens par ordre alphabetique
        self.praticiens_ordonnes = sorted(self.praticiens.keys(), key=lambda x: x.lower())

        requete_secteur = requests.get(serveur['protocole'] + '://' + serveur['host'] + ':' + serveur['port'] + '/GSB/visiteur/secteur_id/'+str(id_visiteur))

        # j'ajoute les praticiens ordonnés en fonction du secteur du visiteur
        for nom_praticien in self.praticiens_ordonnes:
            if int(self.praticiens[nom_praticien].get('Secteur_id')) == int(requete_secteur.text):
                self.SelectionPraticiens.addItem(nom_praticien)

        # requete pour obtenir les médicaments
        requete = requests.get(serveur['protocole'] + '://' + serveur['host'] + ':' + serveur['port'] + '/GSB/medicament')
        medicaments_json = json.loads(requete.text)
        del requete

        # creation d'un dictionnaire pour lier les noms des médicaments avec leur nombre
        for j in range(len(medicaments_json)):
            self.medicaments[medicaments_json[j]["Label"]] = medicaments_json[j]["Id"]

        # j'ordonne les noms des médicaments par ordre alphabetique
        self.medicaments_ordonnes = sorted(self.medicaments.keys(), key=lambda x: x.lower())
        for nom_medicaments in self.medicaments_ordonnes:
            self.SelectionMedicamentNom.addItem(nom_medicaments)

        # mise a jour de la date à la date du jour
        aujourdhui = date.today()
        aujourdhui_formate = aujourdhui.strftime("%d/%m/%Y")
        qdate_aujourdhui_formate = QDate.fromString(aujourdhui_formate, "dd/MM/yyyy")
        self.DateRapport.setDate(qdate_aujourdhui_formate)

        self.BoutonAjouterMedicament.clicked.connect(self.ajouter_medicament)

        # attribut bouton pour valider ou non le formulaire
        self.BoutonFormulaire.accepted.connect(self.envoyer_rapport)
        self.BoutonFormulaire.rejected.connect(self.fermer_fenetre)

    # fonction pour détruire la page
    def fermer_fenetre(self):
        win.stackedWidget.removeWidget(self)
        self.reject()

    # fonction pour ajouter des medicaments a la liste
    def ajouter_medicament(self):

        # si il y a des éléments de sélectionnés
        if self.SelectionMedicamentNom.currentText() != "-Aucun-" and self.SelectionMedicamentQuantite.text() != "":

            # je crée un dictionnaire contenant tous les médicaments choisis
            liste_medicament_enregistre = {}
            for i in range(0, self.TableauOffreMedicaments.rowCount()):
                liste_medicament_enregistre[self.TableauOffreMedicaments.item(i, 0).text()] = i

            # si le médicament n'a pas déjà été entré, je l'intègre
            if self.SelectionMedicamentNom.currentText() not in liste_medicament_enregistre.keys():
                self.TableauOffreMedicaments.insertRow(self.TableauOffreMedicaments.rowCount())
                self.TableauOffreMedicaments.setItem(self.TableauOffreMedicaments.rowCount() - 1, 0,
                                                     QTableWidgetItem(self.SelectionMedicamentNom.currentText()))
                self.TableauOffreMedicaments.setItem(self.TableauOffreMedicaments.rowCount() - 1, 1,
                                                     QTableWidgetItem(self.SelectionMedicamentQuantite.text()))

            # sinon je modifie la valeur de la quantité
            else:
                self.TableauOffreMedicaments.item(
                    liste_medicament_enregistre[self.SelectionMedicamentNom.currentText()], 1) \
                    .setText(self.SelectionMedicamentQuantite.text())
            del liste_medicament_enregistre
        else:
            print("il manque des informations pour pouvoir ajouter un échantillon")

    # fonction qui va envoyer les informations validées du formulaire
    def envoyer_rapport(self):

        # je collecte l'ensemble des médicaments
        liste_offre_medicaments = {}
        for i in range(self.TableauOffreMedicaments.rowCount()):
            liste_offre_medicaments[
                self.medicaments[self.TableauOffreMedicaments.item(i, 0).text()]] = self.TableauOffreMedicaments.item(i,1).text()

        # je construis un dictionnaire pour l'envoyer sous format Json
        rapport_json = {"Medecin": self.praticiens[self.SelectionPraticiens.currentText()],
                        "Date": self.DateRapport.text(),
                        "Motif": self.Motif.text(),
                        "Bilan": self.Bilan.toPlainText(),
                        "Medoc": liste_offre_medicaments}
        requete = requests.post(serveur['protocole'] + '://' + serveur['host'] + ':' + serveur['port'] + '/GSB/CR/Insert',
                                json=rapport_json,
                                headers={'Content-Type': 'application/json'})
        self.fermer_fenetre()


class FenetreConsultation(QDialog):
    def __init__(self):
        super(FenetreConsultation, self).__init__()
        loadUi("UI/fenetre_consultation_rapport.ui", self)

        self.setWindowTitle("AppliVisiteur")

        self.validerIdRapport.clicked.connect(self.valider_rapport)
        self.retourConsultation.clicked.connect(self.fermer_fenetre)

    def fermer_fenetre(self):
        win.stackedWidget.removeWidget(self)
        self.reject()

    def valider_rapport(self):

        # je fais une requete pour obtenir le rapport avec l'ID précédement obtenu
        requete = requests.get(serveur['protocole'] + '://' + serveur['host'] + ':' + serveur['port'] + '/GSB/CR/' + str(self.idRapport.value()) + '/')
        rapport_json = json.loads(requete.text)

        # j'attribut les valeurs aux champs adéquats
        self.SelectionPraticien.setText(rapport_json['Medecin'])
        self.DateRapport.setText(rapport_json["Date"])
        self.Motif.setText(rapport_json["Motif"])
        self.Bilan.setPlainText(rapport_json["Bilan"])

        # je remplis la liste des médicaments avec les données du JSON
        for i in range(0, len(rapport_json["Medoc"])):
            self.TableauOffreMedicaments.insertRow(self.TableauOffreMedicaments.rowCount())
            self.TableauOffreMedicaments.setItem(self.TableauOffreMedicaments.rowCount() - 1, 0,
                                                 QTableWidgetItem(rapport_json["Medoc"][i]["Label"]))
            self.TableauOffreMedicaments.setItem(self.TableauOffreMedicaments.rowCount() - 1, 1,
                                                 QTableWidgetItem(str(rapport_json["Medoc"][i]["Nombre"])))


app = QApplication(sys.argv)

win = FenetreMaitresse()

# je renome la fenetre
win.setWindowTitle("AppliVisiteur")
#win.showMaximized()


win.show()

if __name__ == '__main__':
    try:
        sys.exit(app.exec_())

    finally:
        print("sortie")
