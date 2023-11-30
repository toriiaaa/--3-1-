import pyodbc


class DataBase:
    PATH = r'C:\Users\Georges\Documents\Work\self\master-access-pyqt6\Northwind.accdb'
    DRIVERS = '*.mdb, *.accdb'

    def __init__(self):
        connection_str = (
            r"DRIVER={Microsoft Access Driver (" + self.DRIVERS + ")};"
            rf"DBQ={self.PATH};"
        )
        self.connection = pyodbc.connect(connection_str)
        self.cursor = self.connection.cursor()
