#from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QHeaderView, QTableWidget, QTableWidgetItem, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit, QVBoxLayout)
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from datetime import date
import json
import socket
import sys
from random import randint
import requests


url = "http://127.0.0.1:5000"

menu_test = int(input("1 pour la saisie du rapport ou 2 pour la consultation :\n"))

if menu_test == 1:
    class Dialog(QDialog):

        def __init__(self):
            super(Dialog, self).__init__()

            self.setWindowTitle("AppliVisiteur")

            self.comboboxP = QComboBox()
            self.Praticien = []
            r = requests.get(url + '/GSB/medecin')
            medecin_js = json.loads(r.text)
            for i in range(len(medecin_js)):
                nom_total = str(medecin_js[i]['Id']) + ' - ' + medecin_js[i]['Prenom'] + ' ' + medecin_js[i]['Nom']
                self.Praticien.append(nom_total)

            for nom_praticien in self.Praticien:
                self.comboboxP.addItem(nom_praticien)

            self.date_rapport = QLineEdit()

            self.motif = QLineEdit()

            self.Bilan = QTextEdit()

            self.offre_med = QTableWidget()

            self.column1title = QTableWidgetItem()
            self.column2title = QTableWidgetItem()

            self.createFormGroupBox()

            self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            self.buttonBox.accepted.connect(self.getInfo)
            self.buttonBox.rejected.connect(self.reject)

            mainLayout = QVBoxLayout()
            mainLayout.addWidget(self.formGroupBox)
            mainLayout.addWidget(self.buttonBox)
            self.setLayout(mainLayout)

        def getInfo(self):
            print("Praticien: {0}".format(self.comboboxP.currentText()))
            print("Date du rapport: {0}".format(self.date_rapport.text()))
            print("Motif: {0}".format(self.motif.text()))
            print("Bilan: {0}".format(self.Bilan.toPlainText()))
            print("Enorme: {0}".format(self.offre_med))

            self.close()

        def createFormGroupBox(self):
            self.formGroupBox = QGroupBox("Rapport")
            layout = QFormLayout()
            layout.addRow(QLabel("Praticien:"), self.comboboxP)

            today = date.today()
            format_today = today.strftime("%d/%m/%y")
            self.date_rapport.setText(format_today)

            layout.addRow(QLabel("Date du rapport:"), self.date_rapport)
            layout.addRow(QLabel("Motif Visite:"), self.motif)
            layout.addRow(QLabel("Bilan:"), self.Bilan)

            self.offre_med.setRowCount(4)
            self.offre_med.setColumnCount(2)

            self.column1title.setText("med")
            self.column2title.setText("num")
            self.offre_med.setHorizontalHeaderItem(0, self.column1title)
            self.offre_med.setHorizontalHeaderItem(1, self.column2title)

            for i in range(0, self.offre_med.rowCount()):
                med = QComboBox()
                med.addItem('none')
                r = requests.get(url + '/GSB/medicament')
                medoc_js = json.loads(r.text)
                for j in range(len(medoc_js)):
                    med.addItem(str(medoc_js[j]["Id"]) + ' - ' + medoc_js[j]["Label"])
                self.offre_med.setCellWidget(i, 0, med)
            layout.addRow(QLabel("Offre d'échantillons:"), self.offre_med)

            self.formGroupBox.setLayout(layout)


    if __name__ == '__main__':
        app = QApplication(sys.argv)
        dialog = Dialog()
        sys.exit(dialog.exec_())

if menu_test == 2:

    class Dialog2(QDialog) :

        def __init__(self):
            super(Dialog2, self).__init__()

            self.setWindowTitle("AppliVisiteur")

            r = requests.get(url+'/GSB/CR/2/')
            self.cr = json.loads(r.text)

            self.comboboxP = QLineEdit()

            self.date_rapport = QLineEdit()

            self.motif = QLineEdit()

            self.Bilan = QTextEdit()

            self.offre_med = QTableWidget()

            self.column1title = QTableWidgetItem()
            self.column2title = QTableWidgetItem()


            self.createFormGroupBox()

            self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            self.buttonBox.accepted.connect(self.getInfo)
            self.buttonBox.rejected.connect(self.reject)

            mainLayout = QVBoxLayout()
            mainLayout.addWidget(self.formGroupBox)
            mainLayout.addWidget(self.buttonBox)
            self.setLayout(mainLayout)

        def getInfo(self):
            print("Praticien: {0}".format(self.comboboxP.text()))
            print("Date du rapport: {0}".format(self.date_rapport.text()))
            print("Motif: {0}".format(self.motif.text()))
            print("Bilan: {0}".format(self.Bilan.toPlainText()))
            print("Enorme: {0}".format(self.offre_med))

            self.close()

        def createFormGroupBox(self):
            self.formGroupBox = QGroupBox("Rapport")
            layout = QFormLayout()

            nom_total = str(self.cr['Id']) + ' - ' + self.cr['Medecin']
            self.comboboxP.setText(nom_total)

            layout.addRow(QLabel("Praticien:"), self.comboboxP)

            self.date_rapport.setText(self.cr["Date"])
            self.motif.setText(self.cr["Motif"])
            self.Bilan.setText(self.cr["Bilan"])



            layout.addRow(QLabel("Date du rapport:"), self.date_rapport)
            layout.addRow(QLabel("Motif Visite:"), self.motif)
            layout.addRow(QLabel("Bilan:"), self.Bilan)

            self.offre_med.setRowCount(4)
            self.offre_med.setColumnCount(2)

            self.column1title.setText("med")
            self.column2title.setText("num")
            self.offre_med.setHorizontalHeaderItem(0, self.column1title)
            self.offre_med.setHorizontalHeaderItem(1, self.column2title)

            for i in range(0,self.offre_med.rowCount()):
                med = QComboBox()
                for j in range(len(self.cr['Medoc'])):
                    med.addItem(self.cr['Medoc'][j]['Label']+' - '+str(self.cr['Medoc'][j]['Nombre']))
                self.offre_med.setCellWidget(i, 0, med)
            layout.addRow(QLabel("Offre d'échantillons:"), self.offre_med)

            self.formGroupBox.setLayout(layout)


    if __name__ == '__main__':
        app = QApplication(sys.argv)
        dialog2 = Dialog2()
        sys.exit(dialog2.exec_())

if menu_test != 1 or menu_test != 2:
    print("mauvais input")
    exit()