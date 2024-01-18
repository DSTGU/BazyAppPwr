from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QLabel, QWidget, QHeaderView, QPushButton
from PyQt5.QtCore import *

import EditDatabaseWindow

class UserInfoWindow(QMainWindow):
    def __init__(self, name, population ,data, admin):
        super().__init__()

        self.setWindowTitle("Info Window")
        self.editWindow = None

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

    def dodaj_miasto(self):
        # Nazwa, populacja, Po³o¿enie (point), ID_Gminy (dostaje)
        print("Dodaj")
        self.editWindow = EditDatabaseWindow.EditDatabaseWindow("Dodaj miasto")

    def edytuj_miasto(self):
        print("Edytuj")

    def usun_miasto(self):
        print("Usun")

    def edytuj_gmine(self):
        print("Usun")
