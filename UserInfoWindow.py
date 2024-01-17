from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QLabel, QWidget, QHeaderView
from PyQt5.QtCore import *


class UserInfoWindow(QMainWindow):
    def __init__(self, name, population ,data):
        super().__init__()

        self.setWindowTitle("Info Window")

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


