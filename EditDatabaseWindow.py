from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QFormLayout, QPushButton
from PyQt5.QtCore import pyqtSignal

class EditDatabaseWindow(QMainWindow):
    action_done = pyqtSignal(str, int, float, float)

    def __init__(self, windowName):
        super().__init__()

        self.setWindowTitle(windowName)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.input_layout = QFormLayout(central_widget)
        
        self.nazwa_miasta = QLineEdit(self)
        self.input_layout.addRow("Nazwa miasta:", self.nazwa_miasta)

        self.populacja_miasta = QLineEdit(self)
        self.input_layout.addRow("Populacja:", self.populacja_miasta)

        self.polozenieX_miasta = QLineEdit(self)
        self.polozenieY_miasta = QLineEdit(self)
        self.input_layout.addRow("Polozenie X:", self.polozenieX_miasta)
        self.input_layout.addRow("Polozenie Y:", self.polozenieY_miasta)

        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.check_data)
        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.exit_window)
        self.input_layout.addRow(self.ok_button, self.cancel_button)

    def check_data(self):
        if (self.nazwa_miasta.displayText() != "" 
                and int(self.populacja_miasta.displayText()) > 0
                and self.polozenieX_miasta.displayText() != ""
                and self.polozenieY_miasta.displayText() != ""):
            print("dobrze")
            self.action_done.emit(self.nazwa_miasta.displayText(), int(self.populacja_miasta.displayText()),
                                  float(self.polozenieX_miasta.displayText()), float(self.polozenieY_miasta.displayText()))
            self.close()

    def exit_window(self):
        self.close()