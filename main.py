import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QComboBox, QWidget, \
    QLineEdit, QStyle
from PyQt5.QtCore import QEventLoop, pyqtSignal
import psycopg2
from psycopg2 import sql
import PostgreSQLConnection
import UserWindow
import UserInfoWindow


class Application():

    def __init__(self):
        f = open("local.ini", "r")

        self.postgres_connection = PostgreSQLConnection.PostgreSQLConnection(
            user = f.readline().replace("\n", ""),
            password = f.readline().replace("\n", ""),
            host = f.readline().replace("\n", ""),
            port = f.readline().replace("\n", ""),
            database = f.readline().replace("\n", ""),
        )
        f.close()

        self.userinfobox = None
        self.userWindow = UserWindow.UserWindow(None, None, self.postgres_connection)
        self.userWindow.loginPassup.connect(self.update_window)
        self.userWindow.searchbox.textChanged.connect(self.update_results)
        self.userWindow.table_widget.cellClicked.connect(self.cell_click_action)
        # self.userWindow.loginPass.connect(self.update_login)
        self.admin = 0

        self.show_database()

        self.kraje = []

    def show_database(self):
        self.postgres_connection.create_connection()

        (self.columns, self.data) = self.run_query('''SELECT *
                                            FROM "Gminy aktualne"''')

        ndata = []
        self.columns = limit_results(self.columns)
        for row in self.data:
            ndata.append(limit_results(row))
        self.data = ndata

        self.update_dropdown_kraje()
        self.update_dropdown_powiaty()
        self.update_results()

    def run_query(self, query):
        select_data_query = sql.SQL(query)
        columns, result = self.postgres_connection.execute_query(select_data_query)
        return (columns, result)

    def cell_click_action(self, row, column):
        print(column)
        if column <= 2:
            self.create_infobox(row,column)
            # TODO: else usun gmine


    def create_infobox(self, row, column):

        name = self.userWindow.table_widget.item(row, 0).text()

        options_query = '''SELECT pokazpodleglemiejscowosci('{}')'''.format(name)

        options_columns, options_result = self.run_query(options_query)
        res = []
        population = 0
        #print(options_result)
        for i in options_result:
            res.append((i[0].split(',')[1], i[0].split(',')[2],
                        (str(i[0].split(',')[3]) + " " + str(i[0].split(',')[4])).replace("\"", "").replace("(",
                                                                                                            "").replace(
                            ")", "")))
            population += int(i[0].split(',')[2])

        self.userinfobox = UserInfoWindow.UserInfoWindow(name, population, res, self.admin)

    def update_results(self):
        selected_option = self.userWindow.dropdown_kraje.currentText()
        selected_powiat = self.userWindow.dropdown_powiaty.currentText()
        data = retain_results(self.data, selected_option, selected_powiat, self.userWindow.searchbox.displayText())

        self.userWindow.table_widget.clear()
        self.userWindow.table_widget.setRowCount(0)
        if (self.admin == 0):
            self.userWindow.table_widget.setColumnCount(len(self.columns))
            self.userWindow.table_widget.setHorizontalHeaderLabels(self.columns)
            for row_index, row in enumerate(data):
                self.userWindow.table_widget.insertRow(row_index)
                for col_index, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    self.userWindow.table_widget.setItem(row_index, col_index, item)

        else:
            columns = self.columns
            columns.append("Delete")
            self.userWindow.table_widget.setColumnCount(len(columns))
            self.userWindow.table_widget.setHorizontalHeaderLabels(columns)
            for row_index, row in enumerate(data):
                self.userWindow.table_widget.insertRow(row_index)
                for col_index, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    self.userWindow.table_widget.setItem(row_index, col_index, item)
                item = QTableWidgetItem("Usun")
                self.userWindow.table_widget.setItem(row_index, 3, item)

    def update_dropdown_kraje(self):
        # Fetch available osptions from the database
        options_query = '''SELECT pokazkrajezwiazkowe()'''
        options_columns, options_result = self.run_query(options_query)
        self.kraje = options_result

        options = [row[0].split(",")[1].replace("\"", "") for row in options_result]
        options.insert(0, "No filter")
        # Populate the dropdown list with options
        self.userWindow.dropdown_kraje.addItems(options)

        # Connect the dropdown's currentIndexChanged signal to a slot (e.g., update_table)
        self.userWindow.dropdown_kraje.currentIndexChanged.connect(self.update_dropdown_powiaty)

    def update_dropdown_powiaty(self):
        self.userWindow.dropdown_powiaty.clear()
        # Fetch available osptions from the database
        selected_option = self.userWindow.dropdown_kraje.currentText()
        options_query = '''SELECT pokazpodleglepowiaty('{}')'''.format(selected_option)
        options_columns, options_result = self.run_query(options_query)
        self.kraje = options_result

        options = [row[0].split(",")[1].replace("\"", "") for row in options_result]
        options.insert(0, "No filter")
        # Populate the dropdown list with options
        self.userWindow.dropdown_powiaty.addItems(options)

        # Connect the dropdown's currentIndexChanged signal to a slot (e.g., update_table)
        self.userWindow.dropdown_powiaty.currentIndexChanged.connect(self.update_results)

    def update_window(self, username, token):


        self.userWindow.close()
        newuserWindow = UserWindow.UserWindow(username, token, self.postgres_connection)
        newuserWindow.show()
        self.userWindow = newuserWindow
        self.userWindow.loginPassup.connect(self.update_window)
        self.userWindow.searchbox.textChanged.connect(self.update_results)
        self.userWindow.table_widget.cellClicked.connect(self.cell_click_action)
        self.admin = 1
        self.show_database()


def limit_results(list):
    return [list[2], list[4], list[6]]


def retain_results(data, kraj, powiat, nazwa):
    if (kraj != "No filter"):
        ndata = []
        for i in data:
            if i[2] == kraj:
                ndata.append(i)
        data = ndata
    if (powiat != "No filter"):
        ndata = []
        for i in data:
            if i[1] == powiat:
                ndata.append(i)
        data = ndata

    ndata = []

    for i in data:
        if nazwa in i[0]:
            ndata.append(i)
    data = ndata
    return data


if __name__ == "__main__":
    app = QApplication(sys.argv)
    application = Application()
    window = application.userWindow.show()
    sys.exit(app.exec_())
