import sqlite3
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.initUI()

    def initUI(self):
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(0, 0, 800, 568)
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(['ID',
                                                    'Название сорта',
                                                    'Степень обжарки',
                                                    'Молотый/в зернах',
                                                    'Описание вкуса',
                                                    'Цена',
                                                    'Объем упаковки'])

        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        sql = "SELECT * FROM coffees"

        res = cur.execute(sql).fetchall()

        self.tableWidget.setRowCount(len(res))
        for i, elem in enumerate(res):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
