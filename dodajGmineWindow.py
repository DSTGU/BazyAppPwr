from PyQt5.QtWidgets import QLineEdit, QPushButton, QWidget, QVBoxLayout, QMessageBox, QLabel, QFormLayout, QComboBox, QMainWindow

class DodajGmineWindow(QWidget):

    def __init__(self):

        super().__init__()


        layout = QFormLayout();

        # Example: Adding a QLabel to the layout
        label = QLabel("Hello, this is a QLabel")
        layout.addRow("Label:", label)


        self.setLayout(layout)
        print(2)
        self.show()
        print(2)