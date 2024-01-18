import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QLabel, QWidget, QHeaderView, QPushButton
from PyQt5.QtCore import *
import psycopg2
from psycopg2 import sql

import EditDatabaseWindow

class UserInfoWindow(QMainWindow):
    def __init__(self, name, population ,data, admin, connection):
        super().__init__()
        print(name)
        self.setWindowTitle("Info Window")
        self.editWindow = None
        self.rowSelected = 0
        self.connection = connection

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.layout = QVBoxLayout(central_widget)

        self.label1 = QLabel("Gmina: {}".format(name), central_widget)
        self.label1.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label1)

        if population is not None:
            if population != 0:
                self.label2 = QLabel("Populacja: {}".format(population), central_widget)
                self.label2.setAlignment(Qt.AlignCenter)
                self.layout.addWidget(self.label2)

        # If admin add edit buttons
        if (admin == True):
            self.dodaj_miastoButton = QPushButton('Dodaj miasto', self)
            self.layout.addWidget(self.dodaj_miastoButton)
            self.dodaj_miastoButton.clicked.connect(self.dodaj_miasto)

            self.edytuj_miastoButton = QPushButton('Edytuj miasto', self)
            self.layout.addWidget(self.edytuj_miastoButton)
            self.edytuj_miastoButton.clicked.connect(self.edytuj_miasto)

            self.usun_miastoButton = QPushButton('Usun miasto', self)
            self.layout.addWidget(self.usun_miastoButton)
            self.usun_miastoButton.clicked.connect(self.usun_miasto)

            self.edytuj_gmineButton = QPushButton('Edytuj gmine', self)
            self.layout.addWidget(self.edytuj_gmineButton)            
            self.edytuj_gmineButton.clicked.connect(self.edytuj_gmine)

        # Add a QTableWidget to the central widget
        self.table_widget = QTableWidget(self)
        self.layout.addWidget(self.table_widget)
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(['Miasto','Populacja', 'Polozenie'])
        self.table_widget.cellClicked.connect(self.cell_click_action)

        for row_index, row in enumerate(data):
            self.table_widget.insertRow(row_index)
            for col_index, value in enumerate(row):
                if value == "" or value == " ":
                    value = "No value"
                item = QTableWidgetItem(str(value))
                self.table_widget.setItem(row_index, col_index, item)

        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

        self.setLayout(self.layout)
        self.resize(450,450)


        self.show()

    def cell_click_action(self, row, column):
        self.rowSelected = row

    def run_query(self, query):
        select_data_query = sql.SQL(query)
        columns, result = self.connection.execute_query(select_data_query)
        return (columns, result)

    def dodaj_miasto(self):
        # Nazwa, populacja, Po³o¿enie (point), ID_Gminy (dostaje)
        self.editWindow = EditDatabaseWindow.EditDatabaseWindow("Dodaj miasto")
        self.editWindow.action_done.connect(self.query_dodaj_miasto)
        self.editWindow.show()

        loop = QEventLoop()
        self.editWindow.destroyed.connect(loop.quit)
        loop.exec()

    def query_dodaj_miasto(self, nazwa, populacja, gpsX, gpsY):
        print("query dodaj miasto")
        options_query = '''CALL "dodajMiejscowosc"();'''.format(name)


    def edytuj_miasto(self):
        self.editWindow = EditDatabaseWindow.EditDatabaseWindow("Edytuj miasto")
        
        name = self.table_widget.item(self.rowSelected, 0).text()
        print(name)
        options_query = '''SELECT * FROM "Miejscowosci aktualne" m WHERE 
                            m."nazwa" = '{}';'''.format(name)

        options_columns, options_result = self.run_query(options_query)
        print(options_result)
        res = []
        for i in options_result:
            res.append((i[0].split(',')[1], i[0].split(',')[2],
                        (str(i[0].split(',')[3]) + " " + str(i[0].split(',')[4])).replace("\"", "").replace("(",
                                                                                                            "").replace(
                            ")", "")))
            population += int(i[0].split(',')[2])

        print(res)
        self.editWindow.nazwa_miasta.setText(res[1])
        self.editWindow.show()

        loop = QEventLoop()
        self.editWindow.destroyed.connect(loop.quit)
        loop.exec()

    def usun_miasto(self):
        print("Usun")

    def edytuj_gmine(self):
        print("Usun")
