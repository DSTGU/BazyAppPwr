from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

class EditDatabaseWindow(QMainWindow):
    def __init__(self, windowName):
        super().__init__()

        self.setWindowTitle(windowName)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.main_layout = QVBoxLayout(central_widget)