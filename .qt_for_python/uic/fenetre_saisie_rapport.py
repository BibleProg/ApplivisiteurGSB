# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\jerom\OneDrive\Documents\GitHub\Applivisiteur\Applivisiteur\UI\fenetre_saisie_rapport.ui'
#
# Created by: PyQt5 UI code generator 5.15.5
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(640, 600)
        Dialog.setMinimumSize(QtCore.QSize(640, 600))
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 123, 641, 41))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_8 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.label_8.setFont(font)
        self.label_8.setAutoFillBackground(False)
        self.label_8.setScaledContents(False)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 0, 0, 1, 1)
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 0, 641, 124))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_9 = QtWidgets.QLabel(self.layoutWidget)
        self.label_9.setMinimumSize(QtCore.QSize(191, 122))
        self.label_9.setMaximumSize(QtCore.QSize(191, 122))
        font = QtGui.QFont()
        font.setKerning(True)
        self.label_9.setFont(font)
        self.label_9.setText("")
        self.label_9.setPixmap(QtGui.QPixmap(":/newPrefix/image/logo.jpg"))
        self.label_9.setScaledContents(True)
        self.label_9.setOpenExternalLinks(False)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout.addWidget(self.label_9)
        self.label_10 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(36)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.label_10.setFont(font)
        self.label_10.setAutoFillBackground(False)
        self.label_10.setScaledContents(False)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout.addWidget(self.label_10)
        self.layoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.layoutWidget_2.setGeometry(QtCore.QRect(30, 190, 596, 271))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.dateRapport = QtWidgets.QDateEdit(self.layoutWidget_2)
        self.dateRapport.setCalendarPopup(True)
        self.dateRapport.setObjectName("dateRapport")
        self.gridLayout.addWidget(self.dateRapport, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget_2)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget_2)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.motif = QtWidgets.QLineEdit(self.layoutWidget_2)
        self.motif.setObjectName("motif")
        self.gridLayout.addWidget(self.motif, 2, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.layoutWidget_2)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget_2)
        self.label_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.bilan = QtWidgets.QPlainTextEdit(self.layoutWidget_2)
        self.bilan.setObjectName("bilan")
        self.gridLayout.addWidget(self.bilan, 3, 1, 1, 1)
        self.selectionPraticiens = QtWidgets.QComboBox(self.layoutWidget_2)
        self.selectionPraticiens.setInputMethodHints(QtCore.Qt.ImhNone)
        self.selectionPraticiens.setEditable(True)
        self.selectionPraticiens.setObjectName("selectionPraticiens")
        self.gridLayout.addWidget(self.selectionPraticiens, 0, 1, 1, 1)
        self.horizontalLayout_2.addLayout(self.gridLayout)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_5 = QtWidgets.QLabel(self.layoutWidget_2)
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 0, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.layoutWidget_2)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 1, 0, 1, 1)
        self.selectionMedicamentQuantite = QtWidgets.QSpinBox(self.layoutWidget_2)
        self.selectionMedicamentQuantite.setObjectName("selectionMedicamentQuantite")
        self.gridLayout_3.addWidget(self.selectionMedicamentQuantite, 1, 1, 1, 1)
        self.boutonAjouterMedicament = QtWidgets.QPushButton(self.layoutWidget_2)
        self.boutonAjouterMedicament.setObjectName("boutonAjouterMedicament")
        self.gridLayout_3.addWidget(self.boutonAjouterMedicament, 2, 0, 1, 2)
        self.label_7 = QtWidgets.QLabel(self.layoutWidget_2)
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 3, 0, 1, 1)
        self.tableauOffreMedicaments = QtWidgets.QTableWidget(self.layoutWidget_2)
        self.tableauOffreMedicaments.setObjectName("tableauOffreMedicaments")
        self.tableauOffreMedicaments.setColumnCount(0)
        self.tableauOffreMedicaments.setRowCount(0)
        self.gridLayout_3.addWidget(self.tableauOffreMedicaments, 3, 1, 1, 1)
        self.selectionMedicamentNom = QtWidgets.QComboBox(self.layoutWidget_2)
        self.selectionMedicamentNom.setEditable(True)
        self.selectionMedicamentNom.setCurrentText("")
        self.selectionMedicamentNom.setObjectName("selectionMedicamentNom")
        self.gridLayout_3.addWidget(self.selectionMedicamentNom, 0, 1, 1, 1)
        self.horizontalLayout_2.addLayout(self.gridLayout_3)
        self.boutonFormulaire = QtWidgets.QDialogButtonBox(Dialog)
        self.boutonFormulaire.setGeometry(QtCore.QRect(190, 490, 251, 61))
        self.boutonFormulaire.setMinimumSize(QtCore.QSize(0, 0))
        self.boutonFormulaire.setOrientation(QtCore.Qt.Horizontal)
        self.boutonFormulaire.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.boutonFormulaire.setCenterButtons(True)
        self.boutonFormulaire.setObjectName("boutonFormulaire")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_8.setText(_translate("Dialog", "Saisie de Rapport"))
        self.label_10.setText(_translate("Dialog", "Applivisiteur"))
        self.dateRapport.setDisplayFormat(_translate("Dialog", "dd/MM/yyyy"))
        self.label_3.setText(_translate("Dialog", "Motif :"))
        self.label_2.setText(_translate("Dialog", "Date du rapport :"))
        self.label.setText(_translate("Dialog", "Praticien :"))
        self.label_4.setText(_translate("Dialog", "Bilan :"))
        self.label_5.setText(_translate("Dialog", "Sélection d\'échantillon :"))
        self.label_6.setText(_translate("Dialog", "Nombre d\'échantillon :"))
        self.boutonAjouterMedicament.setText(_translate("Dialog", "Ajouter"))
        self.label_7.setText(_translate("Dialog", "Liste d\'échantillons :"))
import logoqrc_rc