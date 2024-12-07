import sqlite3
import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QWidget

from main_ui import Ui_MainWindow
from addEditCoffeeForm import Ui_Form


class AddEdit(QWidget, Ui_Form):
    def __init__(self, main):
        super().__init__()
        self.main = main

        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.addButton.clicked.connect(self.addCoffee)
        self.editButton.clicked.connect(self.editCoffee)
        self.editID.textChanged.connect(self.change_labels)

    def change_labels(self):
        con = sqlite3.connect('data/coffee.sqlite')
        cur = con.cursor()
        sql = '''
        SELECT sort_name, roasting_degree, state, taste_description, price, packaging_volume
        FROM coffees
        WHERE id = ?'''

        info = cur.execute(sql, (self.editID.text(),)).fetchone()
        if info:
            for i in enumerate([self.editSort, self.editRoast, self.editState,
                                self.editTaste, self.editPrice, self.editVolume]):
                i[1].setText(str(info[i[0]]))
        else:
            for i in [self.editSort, self.editRoast, self.editState,
                      self.editTaste, self.editPrice, self.editVolume]:
                i.setText('Нет такого ID')

    def addCoffee(self):
        con = sqlite3.connect('data/coffee.sqlite')
        cur = con.cursor()
        sql = '''INSERT INTO 
        coffees(sort_name, roasting_degree, state, taste_description, price, packaging_volume) 
        VALUES (?, ?, ?, ?, ?, ?)'''

        cur.execute(sql, (self.addSort.text(),
                          self.addRoast.text(),
                          self.addState.text(),
                          self.addTaste.text(),
                          self.addPrice.text(),
                          self.addVolume.text())).fetchall()
        con.commit()
        con.close()
        self.close()

    def editCoffee(self):
        con = sqlite3.connect('data/coffee.sqlite')
        cur = con.cursor()
        sql = '''UPDATE coffees
        SET sort_name = ?, roasting_degree = ?, state = ?, 
        taste_description = ?, price = ?, packaging_volume = ?
        WHERE id = ?'''

        if self.editSort.text() != 'Нет такого ID':
            cur.execute(sql, (self.editSort.text(),
                              self.editRoast.text(),
                              self.editState.text(),
                              self.editTaste.text(),
                              self.editPrice.text(),
                              self.editVolume.text(),
                              self.editID.text())).fetchall()
            con.commit()
            con.close()
            self.close()

    def closeEvent(self, a0, QCloseEvent=None):
        self.main.update_table()
        self.main.show()


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.add_edit = AddEdit(self)

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
        self.update_table()
        self.pushButton.clicked.connect(self.change_info)

    def change_info(self):
        self.hide()
        self.add_edit.show()

    def update_table(self):
        con = sqlite3.connect('data/coffee.sqlite')
        cur = con.cursor()
        sql = "SELECT * FROM coffees"

        res = cur.execute(sql).fetchall()

        self.tableWidget.setRowCount(len(res))
        for i, elem in enumerate(res):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        con.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())