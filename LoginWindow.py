from PyQt5.QtWidgets import QLineEdit, QPushButton, QWidget, QVBoxLayout, QMessageBox, QLabel, QFormLayout
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from psycopg2 import sql

class LoginWindow(QWidget):
    loginPass = pyqtSignal(str, str)#([username, token])

    def __init__(self, userWindow, connection):
        super().__init__()
        self.connection = connection

        self.username = ""
        self.password = ""
        
        self.setWindowTitle("Login window")

        layout = QFormLayout()

        self.usernameText = QLineEdit(self)
        self.usernameText.move(20, 20)
        self.usernameText.resize(280, 40)

        self.passwordText = QLineEdit(self)
        self.passwordText.move(20, 80)
        self.passwordText.resize(280, 40)

        self.button = QPushButton('Login', self)
        self.button.move(20, 320)

        self.button.clicked.connect(self.on_click)

        layout.addRow("User", self.usernameText)
        layout.addRow("Password", self.passwordText)

        layout.addWidget(self.button)
        self.setLayout(layout)

        self.userWindow = userWindow
        self.resize(375, 75)

    @pyqtSlot()
    def on_click(self):
        self.username = self.usernameText.text()
        self.password = self.passwordText.text()

        columns, result = self.connection.execute_query(sql.SQL("Select zaloguj('{}','{}')".format(self.username, self.password)))

        if(result[0][0] is not None):
            self.loginPass.emit(self.username, result[0][0])
            self.close()