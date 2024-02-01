from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QFormLayout, QPushButton
from PyQt5.QtCore import pyqtSignal

class DeleteConfirmWindow(QMainWindow):
    delete = pyqtSignal(str)

    def __init__(self, windowName):
        super().__init__()

        self.setWindowTitle(windowName)
        self.name = windowName

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.input_layout = QFormLayout(central_widget)
        
        self.ok_button = QPushButton("OK", self)
        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.exit_window)
        self.ok_button.clicked.connect(self.delete_thing)
            
        self.resize(350, 75)
        self.input_layout.addRow(self.ok_button, self.cancel_button)

    def delete_thing(self):
        self.delete.emit(self.name)
        self.close()

    def exit_window(self):
        self.close()