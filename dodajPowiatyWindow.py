from PyQt5.QtWidgets import QLineEdit, QPushButton, QWidget, QVBoxLayout, QMessageBox, QLabel, QFormLayout, \
 QComboBox, QMainWindow, QDialogButtonBox
from PyQt5.QtCore import pyqtSignal

from psycopg2 import sql

class DodajPowiatyWindow(QWidget):
    refreshpowiaty = pyqtSignal()
    def __init__(self, connection, username, token):

        super().__init__()
        self.username = username
        self.token = token
        self.connection = connection

        self.layout = QFormLayout();

        self.dropdown_kraje = QComboBox(self)
        self.layout.addRow("Kraj: ", self.dropdown_kraje)

        self.nazwaPowiatu = QLineEdit(self)
        self.layout.addRow(self.nazwaPowiatu)

        self.buttons = QDialogButtonBox(self)
        self.buttons.addButton(QDialogButtonBox.StandardButton.Ok)
        self.buttons.addButton(QDialogButtonBox.StandardButton.Cancel)

        self.buttons.rejected.connect(self.close)
        self.buttons.accepted.connect(self.add)

        self.layout.addRow(self.buttons)

        self.update_dropdown_kraje()

        self.setLayout(self.layout)


    def update_dropdown_kraje(self):
        # Fetch available osptions from the database
        options_query = '''SELECT pokazkrajezwiazkowe()'''
        options_columns, options_result = self.run_query(options_query)
        options = [row[0].split(",")[1].replace("\"", "") for row in options_result]
        # Populate the dropdown list with options
        self.dropdown_kraje.addItems(options)


    def run_query(self, query):
        select_data_query = sql.SQL(query)
        columns, result = self.connection.execute_query(select_data_query)
        return (columns, result)

    def run_call(self, call):
        select_call = sql.SQL(call)
        self.connection.execute_call(select_call)

    def add(self):
        kraj = self.dropdown_kraje.currentText()

        idkraju = self.run_query('''SELECT *
            FROM "Kraje aktualne"
            WHERE "nazwa_kraju" = '{}';'''.format(kraj))
        idkraju = idkraju[1][0][1]
        print(idkraju)
        call = '''CALL "dodajPowiat"('{}',{},'{}','{}')'''.format(self.nazwaPowiatu.text(), idkraju, self.username, self.token)
        print(call)
        self.run_call(call)
        self.refreshpowiaty.emit()
        self.close()

