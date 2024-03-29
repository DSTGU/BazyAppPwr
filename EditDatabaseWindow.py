from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QFormLayout, QPushButton
from PyQt5.QtCore import pyqtSignal

class EditDatabaseWindow(QMainWindow):
    action_done = pyqtSignal(str, int, str, str)

    def __init__(self, windowName):
        super().__init__()

        self.setWindowTitle(windowName)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.input_layout = QFormLayout(central_widget)
        
        self.ok_button = QPushButton("OK", self)
        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.exit_window)

        if (str(windowName) != "Usun miasto"):
            self.resize(400, 200)
            self.nazwa_miasta = QLineEdit(self)

            self.populacja_miasta = QLineEdit(self)
            self.polozenieX_miasta = None
            self.polozenieY_miasta = None

            if (str(windowName) != "Edytuj gmine"):
                self.ok_button.clicked.connect(self.check_data)

                self.input_layout.addRow("Nazwa miasta:", self.nazwa_miasta)
                self.input_layout.addRow("Populacja:", self.populacja_miasta)

                self.polozenieX_miasta = QLineEdit(self)
                self.polozenieY_miasta = QLineEdit(self)
                self.input_layout.addRow("Polozenie X:", self.polozenieX_miasta)
                self.input_layout.addRow("Polozenie Y:", self.polozenieY_miasta)
            else:
                self.input_layout.addRow("Nazwa gminy:", self.nazwa_miasta)
                self.input_layout.addRow("ID Powiatu:", self.populacja_miasta)
                self.ok_button.clicked.connect(self.edit_gmina)

        else:
            self.ok_button.clicked.connect(self.delete_thing)
            self.resize(100, 100)

        self.input_layout.addRow(self.ok_button, self.cancel_button)
        

    def check_data(self):
        if (self.nazwa_miasta.displayText() != "" 
                and int(self.populacja_miasta.displayText()) > 0):
            self.action_done.emit(self.nazwa_miasta.displayText().strip('"\''), int(self.populacja_miasta.displayText()),
                                  str(self.polozenieX_miasta.displayText()), str(self.polozenieY_miasta.displayText()))
            self.close()

    def edit_gmina(self):
        self.action_done.emit(self.nazwa_miasta.displayText().strip('"\''), int(self.populacja_miasta.displayText()), "", "")
        self.close()

    def delete_thing(self):
        self.action_done.emit("1", "Usun miasto", str(3.0), str(4.0))
        self.close()

    def exit_window(self):
        self.close()