from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QComboBox, \
    QWidget, QLineEdit, QHeaderView, QPushButton, QFormLayout

from PyQt5.QtCore import QEventLoop, pyqtSlot, pyqtSignal

import LoginWindow

class UserWindow(QMainWindow):
    loginPassup = pyqtSignal(str, str)#([username, token])
    def __init__(self, username, token, connection):
        self.connection = connection
        super().__init__()



        if (username is None or token is None):
            self.admin = 0
        else:
            self.admin = 1

        self.setWindowTitle("Database GUI Application")

        # Add a QVBoxLayout to the central widget
        main_layout = QVBoxLayout(self)
        central_layout = QVBoxLayout(self)
        top_layout = QFormLayout(self)

        if (self.admin == 0):
            # Add connect to database button
            self.loginButton = QPushButton('Login', self)
            top_layout.addWidget(self.loginButton)
            self.loginButton.clicked.connect(self.showLoginWindow)

            # Add login window
            self.loginWindow = None

            # Add the searchbox
        self.searchbox = QLineEdit(self)
        top_layout.addRow("Wyszukaj: ", self.searchbox)

        # Create and add a QComboBox
        self.dropdown_kraje = QComboBox(self)
        top_layout.addRow("Kraj: ", self.dropdown_kraje)
        # central_layout.addWidget(self.dropdown_kraje)

        # Create and add a QComboBox
        self.dropdown_powiaty = QComboBox(self)
        top_layout.addRow("Powiat: ", self.dropdown_powiaty)
        # central_layout.addWidget(self.dropdown_powiaty)

        # Add a QTableWidget to the central widget
        self.table_widget = QTableWidget(self)
        central_layout.addWidget(self.table_widget)
        
        # Set the central widget to use the QVBoxLayout
        central_widget = QWidget(self)
        main_layout.addLayout(top_layout)
        main_layout.addLayout(central_layout)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.resize(600, 600)


    def showLoginWindow(self):
        self.loginWindow = LoginWindow.LoginWindow(self, self.connection)
        self.loginWindow.loginPass.connect(self.passup)
        self.loginWindow.show()
        loop = QEventLoop()
        self.loginWindow.destroyed.connect(loop.quit)
        loop.exec()

    def passup(self, username, token):
        print("Passed one")
        self.loginPassup.emit(username,token)