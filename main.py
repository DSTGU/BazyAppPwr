import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QComboBox, QWidget, \
    QLineEdit
from PyQt5.QtCore import QEventLoop, pyqtSignal
import psycopg2
from psycopg2 import sql
import PostgreSQLConnection
import UserWindow
import UserInfoWindow


class Application():

    def __init__(self):
        self.postgres_connection = PostgreSQLConnection.PostgreSQLConnection(
            user="postgres", #"Javascript",
            password="postgres", #"javascript",
            host="localhost",
            port="5432", # "42069",
            database="postgres",
        )

        self.userinfobox = None
        self.userWindow = UserWindow.UserWindow(None, None, self.postgres_connection)
        self.userWindow.loginPassup.connect(self.update_window)
        self.userWindow.searchbox.textChanged.connect(self.update_results)
        self.userWindow.table_widget.cellClicked.connect(self.create_infobox)
        # self.userWindow.loginPass.connect(self.update_login)

        self.selected_view = "Gminy" # self.userWindow.dropdown_view.currentText()
        self.userWindow.dropdown_view.currentIndexChanged.connect(self.update_dropdown_view)

        self.show_database()

        self.kraje = []

    def show_database(self):
        # print("show_database")
        self.postgres_connection.create_connection()

        match self.selected_view:
            case "Miejscowosci":
                self.show_miejscowosci_aktualne()
            case "Gminy":
                self.show_gminy_aktualne()
            case "Powiaty":
                self.show_powiaty_aktualne()
            case "Kraje":
                self.show_kraje_aktualne()
            case _:
                print("Default show database")

        self.update_results()

    def show_miejscowosci_aktualne(self):
        (self.columns, self.data) = self.run_query('''SELECT * 
                                                FROM "Miejscowosci aktualne"''')
        ndata = []
        for row in self.data:
            ndata.append(row)

        self.data = ndata

        self.update_dropdown_kraje()
        # self.update_dropdown_powiaty()
        # self.update_dropdown_gminy()

    def show_gminy_aktualne(self):
        (self.columns, self.data) = self.run_query('''SELECT *
                                            FROM "Gminy aktualne"''')

        ndata = []
        self.columns = limit_results(self.columns)
        for row in self.data:
            ndata.append(limit_results(row))
        self.data = ndata

        self.update_dropdown_kraje()
        self.update_dropdown_powiaty()

    def show_powiaty_aktualne(self):
        (self.columns, self.data) = self.run_query('''SELECT *
                                            FROM "Powiaty aktualne"''')

        # print("Powiaty aktualne")
        ndata = []
        for row in self.data:
            ndata.append(row)

        self.data = ndata

        self.update_dropdown_kraje()
        # self.update_dropdown_powiaty()

    def show_kraje_aktualne(self):
        (self.columns, self.data) = self.run_query('''SELECT *
                                            FROM "Kraje aktualne"''')
        # print("Kraje aktualne")
        ndata = []
        for row in self.data:
            ndata.append(row)

        self.data = ndata

        # self.update_dropdown_kraje()

    def run_query(self, query):
        select_data_query = sql.SQL(query)
        columns, result = self.postgres_connection.execute_query(select_data_query)
        return (columns, result)

    def create_infobox(self, row, column):

        name = self.userWindow.table_widget.item(row, 0).text()

        options_query = '''SELECT pokazpodleglemiejscowosci('{}')'''.format(name)
        # print("pokazpodleglemiejscowosci")
        options_columns, options_result = self.run_query(options_query)
        res = []
        population = 0
        print(options_result)
        for i in options_result:
            res.append((i[0].split(',')[1], i[0].split(',')[2],
                        (str(i[0].split(',')[3]) + " " + str(i[0].split(',')[4])).replace("\"", "").replace("(",
                                                                                                            "").replace(
                            ")", "")))
            population += int(i[0].split(',')[2])

        self.userinfobox = UserInfoWindow.UserInfoWindow(name, population, res)

    def update_results(self):
        # print("update_results")
        self.userWindow.table_widget.clear()
        self.userWindow.table_widget.setRowCount(0)
        self.userWindow.table_widget.setColumnCount(len(self.columns))
        self.userWindow.table_widget.setHorizontalHeaderLabels(self.columns)

        selected_kraj = self.userWindow.dropdown_kraje.currentText()
        selected_powiat = self.userWindow.dropdown_powiaty.currentText()
        selected_gmina = self.userWindow.dropdown_gminy.currentText()
        
        match self.selected_view:
            case "Miejscowosci":
                self.update_results_view_miejscowosci(selected_kraj, selected_powiat, selected_gmina)
            case "Gminy":
                self.update_results_view_gminy(selected_kraj, selected_powiat)
            case "Powiaty":
                self.update_results_view_powiaty(selected_kraj)
            case "Kraje":
                self.update_results_view_kraje()
            case _:
                print("Default update results")
                self.update_results_view_miejscowosci(selected_kraj, selected_powiat, selected_gmina)

        '''
        selected_option = self.userWindow.dropdown_kraje.currentText()
        selected_powiat = self.userWindow.dropdown_powiaty.currentText()
        if (self.selected_view != "Miejscowosci"):
            data = retain_results(self.data, selected_option, selected_powiat, self.userWindow.searchbox.displayText())

        self.userWindow.table_widget.clear()
        self.userWindow.table_widget.setRowCount(0)
        self.userWindow.table_widget.setColumnCount(len(self.columns))
        self.userWindow.table_widget.setHorizontalHeaderLabels(self.columns)
        if (self.selected_view != "Miejscowosci"):
            for row_index, row in enumerate(data):
                self.userWindow.table_widget.insertRow(row_index)
                for col_index, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    self.userWindow.table_widget.setItem(row_index, col_index, item)
        else:
            for row_index, row in enumerate(self.data):
                self.userWindow.table_widget.insertRow(row_index)
                for col_index, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    self.userWindow.table_widget.setItem(row_index, col_index, item)
        '''

    def update_results_view_miejscowosci(self, selected_kraj, selected_powiat, selected_gmina):
        # Own retain results
        data = self.data
        
        if (selected_kraj != "No filter"):
            ndata = []
            for i in data:
                if i[8] == selected_kraj:
                    ndata.append(i)
            data = ndata

        if (selected_powiat != "No filter"):
            ndata = []
            for i in data:
                if i[6] == selected_powiat:
                    ndata.append(i)
            data = ndata

        if (selected_gmina != "No filter"):
            ndata = []
            for i in data:
                if i[4] == selected_powiat:
                    ndata.append(i)
            data = ndata

        ndata = []

        for i in data:
            if self.userWindow.searchbox.displayText() in i[1]:
                ndata.append(i)
        data = ndata

        for row_index, row in enumerate(data):
            self.userWindow.table_widget.insertRow(row_index)
            for col_index, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.userWindow.table_widget.setItem(row_index, col_index, item)

    def update_results_view_gminy(self, selected_option, selected_powiat):
        data = retain_results(self.data, selected_option, selected_powiat, self.userWindow.searchbox.displayText())

        for row_index, row in enumerate(data):
            self.userWindow.table_widget.insertRow(row_index)
            for col_index, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.userWindow.table_widget.setItem(row_index, col_index, item)

    def update_results_view_powiaty(self, selected_kraj):
        # print("update_results_view_powiaty")
        
        # Own retain results
        data = self.data
        
        if (selected_kraj != "No filter"):
            ndata = []
            for i in data:
                if i[4] == selected_kraj:
                    ndata.append(i)
            data = ndata

        ndata = []

        for i in data:
            if self.userWindow.searchbox.displayText() in i[2]:
                ndata.append(i)
        data = ndata

        for row_index, row in enumerate(data):
            self.userWindow.table_widget.insertRow(row_index)
            for col_index, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.userWindow.table_widget.setItem(row_index, col_index, item)

    def update_results_view_kraje(self):
        for row_index, row in enumerate(self.data):
            self.userWindow.table_widget.insertRow(row_index)
            for col_index, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.userWindow.table_widget.setItem(row_index, col_index, item)

    def update_dropdown_kraje(self):
        # self.userWindow.dropdown_kraje.clear()
        # Fetch available osptions from the database
        options_query = '''SELECT pokazkrajezwiazkowe()'''
        # print("pokazkrajezwiazkowe")
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
        # print("pokazpodleglepowiaty")
        options_columns, options_result = self.run_query(options_query)
        self.kraje = options_result

        options = [row[0].split(",")[1].replace("\"", "") for row in options_result]
        options.insert(0, "No filter")
        # Populate the dropdown list with options
        self.userWindow.dropdown_powiaty.addItems(options)

        # Connect the dropdown's currentIndexChanged signal to a slot (e.g., update_table)
        self.userWindow.dropdown_powiaty.currentIndexChanged.connect(self.update_results)#self.update_dropdown_gminy)

    def update_dropdown_gminy(self):
        self.userWindow.dropdown_gminy.clear()

        # Fetch available osptions from the database
        selected_option = self.userWindow.dropdown_powiaty.currentText()
        options_query = '''SELECT pokazpodleglegminy('{}')'''.format(selected_option)
        options_columns, options_result = self.run_query(options_query)
        self.kraje = options_result

        options = [row[0].split(",")[1].replace("\"", "") for row in options_result]
        options.insert(0, "No filter")
        # Populate the dropdown list with options
        self.userWindow.dropdown_gminy.addItems(options)

        # Connect the dropdown's currentIndexChanged signal to a slot (e.g., update_table)
        self.userWindow.dropdown_gminy.currentIndexChanged.connect(self.update_results)

    def update_dropdown_view(self):
        # Fetch available osptions from the database
        self.selected_view = self.userWindow.dropdown_view.currentText()

        self.userWindow.dropdown_view.currentIndexChanged.connect(self.update_dropdown_kraje)
        
        match self.selected_view:
            case "Miejscowosci":
                self.show_miejscowosci_aktualne()
            case "Gminy":
                self.show_gminy_aktualne()
            case "Powiaty":
                # self.userWindow.dropdown_kraje.currentIndexChanged.disconnect()#self.update_dropdown_powiaty)
                self.show_powiaty_aktualne()
            case "Kraje":
                # self.userWindow.dropdown_powiaty.currentIndexChanged.disconnect()# self.update_results)
                self.show_kraje_aktualne()
            case _:
                print("Default show database")
                
        # self.update_results()

    def update_window(self, username, token):


        self.userWindow.close()
        newuserWindow = UserWindow.UserWindow(username, token, self.postgres_connection)
        newuserWindow.show()
        self.userWindow = newuserWindow
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
