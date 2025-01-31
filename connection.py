# -*- coding: utf-8 -*-
"""
Created on Wed Dec 01 14:25:59 2023

@author: Dr Charles NKUNA
"""
import sys
import sqlite3

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtWidgets import QApplication
from os import path
from PyQt5.uic import loadUiType
from PyQt5.QtCore import Qt
from dashboard import Ui_dashboard_window


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = path.abspath(".")

    return path.join(base_path, relative_path)


FORM_CLASS, _ = loadUiType(resource_path("login_csmcg.ui"))


class Main(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_Buttons()

        # Fixer la taille de la fenêtre (par exemple, 800x600)
        self.setFixedSize(800, 610)

        # Centrer la fenêtre
        self.center_window()

    def center_window(self):
        # Récupérer la géométrie de l'écran
        screen_geometry = QApplication.desktop().availableGeometry(self)
        window_geometry = self.frameGeometry()

        # Calculer le centre de l'écran
        screen_center = screen_geometry.center()

        # Déplacer le rectangle de la fenêtre pour le centrer sur l'écran
        window_geometry.moveCenter(screen_center)

        # Positionner la fenêtre
        self.move(window_geometry.topLeft())

    def retranslateUi(self, LoginWindow):
        _translate = QtCore.QCoreApplication.translate
        LoginWindow.setWindowTitle(_translate("LoginWindow", "Centre des Soins Médicaux la Croix Glorieuse -CSM-CG"))
        self.label_titre_cx.setText(_translate("LoginWindow", "Vous devez vous connecter"))
        self.infos_csmcg_lbl.setText(_translate("LoginWindow",
                                                "Cabinet de Soins Médicaux \"LA CROIX GLORIEUSE\" Secteur 16 - Song Naba - 05 bp 6592 Ouagadougou - Tél. +226 70 27 05 02 / 77 25 76 65 - Email : santeglorieuse@yahoo.fr"))
        self.infos_csmcg_lbl_2.setText(_translate("LoginWindow", "Cabinet de Soins Médicaux \"LA CROIX GLORIEUSE\" "))
        self.cx_btn.setText(_translate("LoginWindow", "Se Connecter"))
        self.comboBox_niveau.setItemText(0, _translate("LoginWindow", "Choisir votre niveau de rôle"))
        self.comboBox_niveau.setItemText(1, _translate("LoginWindow", "Administrateur - 0"))
        self.comboBox_niveau.setItemText(2, _translate("LoginWindow", "Superviseur - 1"))
        self.comboBox_niveau.setItemText(3, _translate("LoginWindow", "Utilisateur - 2"))
        self.comboBox_niveau.setStyleSheet(_translate("LoginWindow", "font: 10pt Montserrat;\n"
                                                                     " background-color: rgb(186, 209, 248);\n"
                                                                     "color: rgb(0, 1, 146);"))
        self.user_level_lbl.setText(_translate("LoginWindow", "Niveau"))
        self.login_lbl.setText(_translate("LoginWindow", "Login"))
        self.login_lineEdit.setPlaceholderText(_translate("LoginWindow", "Nom d\'utilisateur"))
        self.mdp_lbl.setText(_translate("LoginWindow", "Mot de passe"))
        self.mdp_lineEdit.setPlaceholderText(_translate("LoginWindow", "Mot de passe"))
        self.Consultation_lbl.setText(_translate("LoginWindow", "Consultation médical"))
        self.label.setText(_translate("LoginWindow",
                                      "<html><head/><body><div align=\"center\">Cabinet de Soins Médicaux</div><div align=\"center\"><strong>LA CROIX GLORIEUSE</strong></div></body></html>"))

    def showEvent(self, event):
        super(Main, self).showEvent(event)
        self.login_lineEdit.setFocus()

    def Handle_Buttons(self):
        # self.cx_btn.clicked.connect(self.connexion_bdd)
        self.cx_btn.clicked.connect(lambda: self.connexion_bdd(self.login_lineEdit.text(),
                                                               self.mdp_lineEdit.text(),
                                                               self.comboBox_niveau.currentText(),
                                                               self))
        # Associez la touche Entrée (Return) comme raccourci pour le bouton cx_btn
        self.cx_btn.setShortcut(Qt.Key_Return)

        # Connectez la méthode returnButtonPressed au clic du bouton return_btn
        self.cx_btn.clicked.connect(self.returnButtonPressed)

    def connexion_bdd(self, login_lineEdit, mdp_lineEdit, comboBox_niveau, LoginWindow):
        db = sqlite3.connect(resource_path("croixg.db"))
        cursor = db.cursor()

        # Vérifier les identifiants de connexion dans la base de données
        cursor.execute(
            "SELECT login, niveauutilisateur FROM cg_connexion WHERE login = ? AND motdepasse = ? AND "
            "niveauutilisateur = ?",
            (login_lineEdit, mdp_lineEdit, comboBox_niveau)
        )
        result = cursor.fetchone()

        if result:
            # Récupérer le nom de l'utilisateur et son niveau d'autorisation
            username = result[0]  # `login` (nom de l'utilisateur)
            authorization_level = result[1]  # `niveauutilisateur` (niveau d'autorisation)

            # Transformer username et authorization_level
            formatted_username = username.capitalize()  # Mettre la première lettre en majuscule
            formatted_auth_level = authorization_level[
                                   :-4].capitalize()  # Supprimer les 4 derniers caractères et capitaliser

            # Masquer la fenêtre de connexion
            self.hide()

            # Ouvrir la fenêtre de tableau de bord
            self.dashboard_window = QtWidgets.QMainWindow()
            self.dashboard_ui = Ui_dashboard_window()
            self.dashboard_ui.setupUi(self.dashboard_window)

            # Passer les informations au tableau de bord
            self.dashboard_ui.set_user_info(username, authorization_level)

            # Afficher le nom de l'utilisateur et son niveau d'autorisation
            # self.dashboard_ui.name_user_auth_lbl.setText(f"{username} - {authorization_level}")

            # Mettre à jour le QLabel
            self.dashboard_ui.name_user_auth_lbl.setText(f"{formatted_username} - {formatted_auth_level}")
            self.dashboard_ui.name_user_auth_lbl.setStyleSheet("font-size: 16px; font-style: italic; color: #ff0000;")

            # Afficher la fenêtre du tableau de bord
            self.dashboard_window.show()
        else:
            # msg = QMessageBox.warning(self, "Échec de la connexion", "Identifiants incorrects, réessayez encore !")
            msg = QMessageBox(self)
            msg.setWindowTitle("Échec de la connexion")
            msg.setText("Identifiants incorrects, réessayez encore !")
            # Mettre en forme le message
            msg.setStyleSheet(
                """
                QMessageBox {
                    background-color: rgb(186, 209, 248);
                    color: rgb(0, 1, 146);
                    font-size: 12px;
                    font-weight: normal;
                }
                QMessageBox QLabel {
                    color: rgb(0, 1, 146);
                }
                QMessageBox QPushButton {
                    background-color: rgb(0, 1, 146);
                    color: white;
                    border-radius: 5px;
                    padding: 5px;
                }
                QMessageBox QPushButton:hover {
                    background-color: rgb(0, 0, 100);
                }
                """
            )
            msg.exec_()
            return True

    def show_mes_consultations_window(self):
        # print("Ouverture de la fenêtre ConsultationMain")
        self.login_lineEdit = self.login_lineEdit.text()
        self.user_level = self.comboBox_niveau.currentText()[:-4]

        # Passez l'information de l'utilisateur connecté
        self.mes_consultations_window.set_connected_user(self.login_lineEdit, self.user_level)
        # Affichez la fenêtre secondaire
        self.mes_consultations_window.show()

    def dash(self):
        pass

    def returnButtonPressed(self):
        pass


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Appliquer le style "Fusion" à l'application
    window = Main()
    window.show()
    sys.exit(app.exec_())
    # app.exec()


if __name__ == '__main__':
    main()
