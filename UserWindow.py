from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QComboBox, \
    QWidget, QLineEdit, QHeaderView, QPushButton

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
        central_layout = QVBoxLayout(self)

        if (self.admin == 0):
            # Add connect to database button
            self.loginButton = QPushButton('Login', self)
            central_layout.addWidget(self.loginButton)
            self.loginButton.clicked.connect(self.showLoginWindow)

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

        self.resize(450, 600)


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