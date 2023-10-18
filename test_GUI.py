from Applivisiteur import *
import unittest
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QApplication, QMainWindow
from PyQt5.uic import loadUi



class TestStringMethods(unittest.TestCase):

    def test_stackedWidgetDeFenetreMaitresse(self):
        widget = QDialog()
        fen1 = FenetreMaitresse()

        fen1.stackedWidget.addWidget(widget)
        fen1.stackedWidget.setCurrentWidget(widget)
        self.assertEqual(fen1.stackedWidget.currentWidget(), widget)

    def test_check_code_status(self):
        dict_code = {200: True, 201: True, 401: False, 404: False, 500: False, 1000: False}
        pass_bool = True
        for k,v in dict_code.items():
            get = check_code_status(k)
            if get['status'] != v:
                pass_bool = False
        self.assertEqual(pass_bool, True)

    def test_nettoyage_str(self):
        str_input = " azertyuiopQSDFGHJKLMù%^^¨¨$$££µµ***{{{{''''21021455877 \n"

        self.assertEqual(nettoyage_str(str_input, 1), "azertyuiopQSDFGHJKLMù%^^¨¨$$££µµ***{{{{''''21021455877")
        self.assertEqual(nettoyage_str(str_input, 0, 1), " azertyuiopqsdfghjklmù%^^¨¨$$££µµ***{{{{''''21021455877 \n")
        self.assertEqual(nettoyage_str(str_input, 0, 0, 1), "azertyuiopQSDFGHJKLMùµµ21021455877")

    def test_ouverture_fermeture(self):
        win2 = FenetreMaitresse()
        win3 = FenetreConsultation()
        win2.stackedWidget.addWidget(win3)
        win2.stackedWidget.setCurrentWidget(win3)
        self.assertEqual(str(win2.stackedWidget.currentWidget()).split()[0], '<Applivisiteur.FenetreConsultation')


if __name__ == '__main__':
    unittest.main()

