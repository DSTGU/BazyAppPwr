from PyQt5.QtWidgets import QLineEdit, QPushButton, QWidget, QVBoxLayout, QMessageBox, QLabel, QFormLayout, \
 QComboBox, QMainWindow, QDialogButtonBox

from psycopg2 import sql

class DodajGmineWindow(QWidget):

    def __init__(self, connection):

        super().__init__()
        self.connection = connection

        self.layout = QFormLayout();

        self.dropdown_kraje = QComboBox(self)
        self.layout.addRow("Kraj: ", self.dropdown_kraje)

        self.dropdown_powiaty = QComboBox(self)
        self.layout.addRow("Powiat: ", self.dropdown_powiaty)

        self.nazwaGminy = QLineEdit(self)
        self.layout.addRow(self.nazwaGminy)

        self.buttons = QDialogButtonBox(self)
        self.buttons.addButton(QDialogButtonBox.StandardButton.Ok)
        self.buttons.addButton(QDialogButtonBox.StandardButton.Cancel)

        self.buttons.rejected.connect(self.close)
        self.buttons.accepted.connect(self.add)

        self.layout.addRow(self.buttons)

        self.update_dropdown_kraje()
        self.update_dropdown_powiaty()

        self.setLayout(self.layout)


    def update_dropdown_kraje(self):
        # Fetch available osptions from the database
        options_query = '''SELECT pokazkrajezwiazkowe()'''
        options_columns, options_result = self.run_query(options_query)
        options = [row[0].split(",")[1].replace("\"", "") for row in options_result]
        # Populate the dropdown list with options
        self.dropdown_kraje.addItems(options)

        # Connect the dropdown's currentIndexChanged signal to a slot (e.g., update_table)
        self.dropdown_kraje.currentIndexChanged.connect(self.update_dropdown_powiaty)

    def update_dropdown_powiaty(self):
        self.dropdown_powiaty.clear()
        # Fetch available osptions from the database
        selected_option = self.dropdown_kraje.currentText()
        options_query = '''SELECT pokazpodleglepowiaty('{}')'''.format(selected_option)
        options_columns, options_result = self.run_query(options_query)

        options = [row[0].split(",")[1].replace("\"", "") for row in options_result]
        # Populate the dropdown list with options
        self.dropdown_powiaty.addItems(options)


    def run_query(self, query):
        select_data_query = sql.SQL(query)
        columns, result = self.connection.execute_query(select_data_query)
        return (columns, result)


    def add(self):
        kraj = self.dropdown_kraje.currentText()
        powiat = self.dropdown_powiaty.currentText()