from PyQt5.QtWidgets import QLineEdit, QPushButton, QWidget, QVBoxLayout, QMessageBox, QLabel, QFormLayout
from PyQt5.QtCore import pyqtSlot, pyqtSignal

class LoginWindow(QWidget):
    loginPass = pyqtSignal(bool)#([str, str, str, str, str])

    def __init__(self):
        super().__init__()
        
        # Defaults
        self.username = "postgres"
        self.password = "postgres"
        self.host = "localhost"
        self.port = "5432"
        self.database = "postgres"

        # layout = QVBoxLayout()
        layout = QFormLayout()

        self.usernameText = QLineEdit(self)
        self.usernameText.move(20, 20)
        self.usernameText.resize(280, 40)

        self.passwordText = QLineEdit(self)
        self.passwordText.move(20, 80)
        self.passwordText.resize(280, 40)

        self.hostText = QLineEdit(self)
        self.hostText.move(20, 140)
        self.hostText.resize(280, 40)

        self.portText = QLineEdit(self)
        self.portText.move(20, 200)
        self.portText.resize(280, 40)

        self.databaseText = QLineEdit(self)
        self.databaseText.move(20, 260)
        self.databaseText.resize(280, 40)

        self.button = QPushButton('Login', self)
        self.button.move(20, 320)

        self.button.clicked.connect(self.on_click)

        layout.addRow("User", self.usernameText)
        layout.addRow("Password", self.passwordText)
        # layout.addWidget(self.usernameText)
        # layout.addWidget(self.passwordText)
        layout.addRow("Host", self.hostText)
        layout.addRow("Port", self.portText)
        layout.addRow("Database", self.databaseText)

        layout.addWidget(self.button)

        self.setLayout(layout)

    @pyqtSlot()
    def on_click(self):
        self.username = self.usernameText.text()
        self.password = self.passwordText.text()
        self.host = self.hostText.text()
        self.port = self.portText.text()
        self.database = self.databaseText.text()

        # QMessageBox.question(self, 'MSBox', "Napisales: " + self.usernameText.text(), QMessageBox.Ok, QMessageBox.Ok)
        # self.usernameText.setText("")
        self.loginPass.emit(True)
        self.close()