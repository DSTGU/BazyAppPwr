from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QComboBox, \
    QWidget, QLineEdit, QHeaderView, QPushButton

from PyQt5.QtCore import QEventLoop, pyqtSlot, pyqtSignal

import LoginWindow

class UserWindow(QMainWindow):
    loginPass = pyqtSignal(str, str, str, str, str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Database GUI Application")

        # Add a QVBoxLayout to the central widget
        central_layout = QVBoxLayout(self)

        # Add connect to database button
        self.connectDbButton = QPushButton('Connect to database', self)
        central_layout.addWidget(self.connectDbButton)
        self.connectDbButton.clicked.connect(self.showLoginWindow)

        # Add login window
        self.loginWindow = None

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

    def showLoginWindow(self):
        self.loginWindow = LoginWindow.LoginWindow()
        self.loginWindow.show()
        loop = QEventLoop()
        self.loginWindow.destroyed.connect(loop.quit)
        self.loginWindow.button.clicked.connect(self.on_login_confirm)
        loop.exec()

    def on_login_confirm(self, emit): #usr, passw, hst, prt, db):
        self.loginPass.emit(self.loginWindow.username, self.loginWindow.password, self.loginWindow.host, self.loginWindow.port, self.loginWindow.database)