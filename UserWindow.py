import dodajPowiatyWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QComboBox, \
    QWidget, QLineEdit, QHeaderView, QPushButton, QFormLayout, QHBoxLayout, QLabel, QStyle
from PyQt5.QtCore import QEventLoop, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QIcon
from psycopg2 import sql

import LoginWindow
import PostgreSQLConnection
import dodajGmineWindow

class UserWindow(QMainWindow):
    loginPassup = pyqtSignal(str, str)#([username, token])
    refresh = pyqtSignal()
    def __init__(self, username, token, connection):
        self.connection = connection
        super().__init__()

        self.setWindowTitle("Database GUI Application")

        # Add a QVBoxLayout to the central widget
        self.main_layout = QVBoxLayout(self)
        self.central_layout = QVBoxLayout(self)
        self.top_layout = QFormLayout(self)

        self.dodajGmineWindow = None
        self.dodajPowiatyWindow = None
        self.loginButton = None
        self.loginWindow = None
        self.searchbox = None
        self.dropdown_kraje = None
        self.dropdown_powiaty = None
        self.table_widget = None
        self.username = username
        self.token = token

        if (username is None or token is None):
            self.admin = 0
            self.nonAdminWindowInit()
        else:
            self.admin = 1
            self.adminWindowInit()

        self.resize(600, 600)

    def nonAdminWindowInit(self):

        # Add connect to database button
        self.loginButton = QPushButton('Login', self)
        self.top_layout.addWidget(self.loginButton)
        self.loginButton.clicked.connect(self.showLoginWindow)

        # Add login window
        self.loginWindow = None
        # Add the searchbox
        self.searchbox = QLineEdit(self)
        self.top_layout.addRow("Wyszukaj: ", self.searchbox)

        # Create and add a QComboBox
        self.dropdown_kraje = QComboBox(self)
        self.top_layout.addRow("Kraj: ", self.dropdown_kraje)
        # central_layout.addWidget(self.dropdown_kraje)

        # Create and add a QComboBox
        self.dropdown_powiaty = QComboBox(self)
        self.top_layout.addRow("Powiat: ", self.dropdown_powiaty)
        # central_layout.addWidget(self.dropdown_powiaty)

        # Add a QTableWidget to the central widget
        self.table_widget = QTableWidget(self)
        self.central_layout.addWidget(self.table_widget)

        # Set the central widget to use the QVBoxLayout
        self.central_widget = QWidget(self)
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addLayout(self.central_layout)
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

    def adminWindowInit(self):

        # Add the searchbox
        self.searchbox = QLineEdit(self)
        self.top_layout.addRow("Wyszukaj: ", self.searchbox)


        krajeHBox = QHBoxLayout(self)
        textK = QLabel(self)
        textK.setText("Kraj:")
        krajeHBox.addWidget(textK)

        self.dropdown_kraje = QComboBox(self)
        krajeHBox.addWidget(self.dropdown_kraje)
        # central_layout.addWidget(self.dropdown_kraje)

        edytujKrajButton = QPushButton(self)
        edytujKrajButton.setIcon(self.style().standardIcon(QStyle.SP_FileDialogInfoView))
        krajeHBox.addWidget(edytujKrajButton)
        self.top_layout.addRow(krajeHBox)
        edytujKrajButton.clicked.connect(self.showEdytujKrajWindow)


        powiatyHBox = QHBoxLayout(self)
        textP = QLabel(self)
        textP.setText("Powiaty:")
        powiatyHBox.addWidget(textP)
        # Create and add a QComboBox
        self.dropdown_powiaty = QComboBox(self)
        powiatyHBox.addWidget(self.dropdown_powiaty)
        # central_layout.addWidget(self.dropdown_kraje)

        dodajPowiatButton = QPushButton(self)
        dodajPowiatButton.setIcon(self.style().standardIcon(QStyle.SP_DialogApplyButton))
        powiatyHBox.addWidget(dodajPowiatButton)
        dodajPowiatButton.clicked.connect(self.showDodajPowiatWindow)

        usunPowiatButton = QPushButton(self)
        usunPowiatButton.setIcon(self.style().standardIcon(QStyle.SP_DialogDiscardButton))
        powiatyHBox.addWidget(usunPowiatButton)
        usunPowiatButton.clicked.connect(self.usunPowiat)

        edytujPowiatButton = QPushButton(self)
        edytujPowiatButton.setIcon(self.style().standardIcon(QStyle.SP_FileDialogInfoView))
        powiatyHBox.addWidget(edytujPowiatButton)
        edytujPowiatButton.clicked.connect(self.showEdytujPowiatWindow)

        self.top_layout.addRow(powiatyHBox)

        dodajGmineButton = QPushButton(self)
        dodajGmineButton.setIcon(self.style().standardIcon(QStyle.SP_DialogApplyButton))
        dodajGmineButton.setText("Dodaj Gminę")
        dodajGmineButton.clicked.connect(self.showDodajGmineWindow)
        self.top_layout.addRow(dodajGmineButton)


        # Add a QTableWidget to the central widget
        self.table_widget = QTableWidget(self)
        self.central_layout.addWidget(self.table_widget)

        # Set the central widget to use the QVBoxLayout
        self.central_widget = QWidget(self)
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addLayout(self.central_layout)
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

    def showLoginWindow(self):
        self.loginWindow = LoginWindow.LoginWindow(self, self.connection)
        self.loginWindow.loginPass.connect(self.passup)
        self.loginWindow.show()
        loop = QEventLoop()
        self.loginWindow.destroyed.connect(loop.quit)
        loop.exec()

    def showDodajGmineWindow(self):
        self.dodajGmineWindow = dodajGmineWindow.DodajGmineWindow(self.connection, self.username, self.token)
        self.dodajGmineWindow.show()
        self.dodajGmineWindow.refreshgminy.connect(self.dodajGmineWindowSignal)

    def dodajGmineWindowSignal(self):
        self.refresh.emit()

    def showDodajPowiatWindow(self):
        self.dodajPowiatyWindow = dodajPowiatyWindow.DodajPowiatyWindow(self.connection, self.username, self.token)
        self.dodajPowiatyWindow.show()
        self.dodajPowiatyWindow.refreshpowiaty.connect(self.dodajGmineWindowSignal)

    def usunGmine(self, row):
        name = self.table_widget.item(row, 0).text()
        print("CALL \"usunGmina\"('{}','{}','{}');".format(name, self.username, self.token))
        self.run_call("CALL \"usunGmina\"('{}','{}','{}');".format(name, self.username, self.token))
        self.refresh.emit()

    def usunPowiat(self):
        name = self.dropdown_powiaty.currentText()
        print("CALL \"usunPowiat\"('{}','{}','{}');".format(name, self.username, self.token))
        self.run_call("CALL \"usunPowiat\"('{}','{}','{}');".format(name, self.username, self.token))
        self.refresh.emit()

    def showEdytujPowiatWindow(self):
        print("7")
    def showEdytujKrajWindow(self):
        print("8")


    def passup(self, username, token):
        print("Passed one")
        self.loginPassup.emit(username,token)




    def run_query(self, query):
        select_data_query = sql.SQL(query)
        columns, result = self.connection.execute_query(select_data_query)
        return (columns, result)

    def run_call(self, call):
        select_call = sql.SQL(call)
        self.connection.execute_call(select_call)
