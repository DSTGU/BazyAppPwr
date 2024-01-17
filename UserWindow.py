from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QComboBox, \
    QWidget, QLineEdit

class UserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Database GUI Application")

        # Add a QVBoxLayout to the central widget
        central_layout = QVBoxLayout(self)

        # Add the searchbox
        self.searchbox = QLineEdit(self)
        central_layout.addWidget(self.searchbox)

        # Create and add a QComboBox
        self.dropdown_kraje = QComboBox(self)
        central_layout.addWidget(self.dropdown_kraje)

        # Create and add a QComboBox
        self.dropdown_powiaty = QComboBox(self)
        central_layout.addWidget(self.dropdown_powiaty)

        # Add a QTableWidget to the central widget
        self.table_widget = QTableWidget(self)
        central_layout.addWidget(self.table_widget)

        # Set the central widget to use the QVBoxLayout
        central_widget = QWidget(self)
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

        self.resize(450,600)