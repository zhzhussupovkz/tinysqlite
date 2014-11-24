# -*- coding: utf-8 -*-

# The MIT License (MIT)

# Copyright (c) 2014 Zhassulan Zhussupov

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import sqlite3
from PyQt4 import QtGui, QtCore
from datetime import *

class Main(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.setWindowTitle('Tinysqlite')
        self.setWindowIcon(QtGui.QIcon("icons/db.png"))
        self.resize(640, 480)

        menubar = self.menuBar()
        self.generateTestDb()
        self.generateMenu(menubar)
        self.center()

        self.statusBar().showMessage(u"Готово")

    def generateTestDb(self):
        self.conn = sqlite3.connect("./db/test.db")
        self.conn.close()
        self.conn = False

    def generateMenu(self, menubar):
        file = menubar.addMenu(u"&Файл")
        help = menubar.addMenu(u"&Помощь")
        toolbar = self.addToolBar(u"Главная")

        self.dbAdd = QtGui.QAction(QtGui.QIcon('./icons/menu/db_add.png'), u'Подключиться к БД', self)
        self.dbAdd.setShortcut("Ctrl+O")
        self.dbAdd.setStatusTip(u"Подключиться к базе данных")
        self.dbAdd.triggered.connect(self.connectDb)
        file.addAction(self.dbAdd)
        toolbar.addAction(self.dbAdd)

        self.dbRefresh = QtGui.QAction(QtGui.QIcon('./icons/menu/db_refresh.png'), u'Обновить БД', self)
        self.dbRefresh.setShortcut("Ctrl+R")
        self.dbRefresh.setStatusTip(u"Обновить информацию о базе данных")
        if self.conn:
          self.dbRefresh.setEnabled(True)
        else:
          self.dbRefresh.setEnabled(False)
        file.addAction(self.dbRefresh)
        toolbar.addAction(self.dbRefresh)

        self.dbDelete = QtGui.QAction(QtGui.QIcon('./icons/menu/db_delete.png'), u'Отключиться от БД', self)
        self.dbDelete.setShortcut("Ctrl+D")
        self.dbDelete.setStatusTip(u"Отключиться от базы данных")
        self.dbDelete.triggered.connect(self.disconnectDb)
        if self.conn:
          self.dbDelete.setEnabled(True)
        else:
          self.dbDelete.setEnabled(False)
        file.addAction(self.dbDelete)
        toolbar.addAction(self.dbDelete)

        exit = QtGui.QAction(QtGui.QIcon('./icons/menu/exit.png'), u'Выход', self)
        exit.setShortcut("Ctrl+Q")
        exit.setStatusTip(u"Выход")
        file.addAction(exit)
        toolbar.addAction(exit)
        self.connect(exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))

        about = QtGui.QAction(QtGui.QIcon('./icons/menu/star.png'), u'О программе', self)
        about.setStatusTip(u"Информация о программе")
        about.triggered.connect(self.showAbout)
        help.addAction(about)

    def connectDb(self):
        dbFile = str(QtGui.QFileDialog.getOpenFileName(self, u'Открыть файл'))
        self.conn = sqlite3.connect(dbFile)
        self.dbRefresh.setEnabled(True)
        self.dbDelete.setEnabled(True)
        self.dbAdd.setEnabled(False)
        self.currentDbName = dbFile.split('/')[-1].strip(".db")
        self.showDbStructure()
        self.statusBar().showMessage(u"Соединение с БД %s установлено." % dbFile.split('/')[-1])

    def disconnectDb(self):
        self.conn.close()
        self.dbAdd.setEnabled(True)
        self.dbRefresh.setEnabled(False)
        self.dbDelete.setEnabled(False)
        self.dbTreeWidget.setParent(None)
        self.statusBar().showMessage(u"Соединение с текущей БД разорвано.")

    def showAbout(self):
        about = QtGui.QDialog(self)
        about.setWindowTitle(u"О программе")
        about.setWindowIcon(QtGui.QIcon("./icons/menu/star.png"))

        pixmap = QtGui.QPixmap("./icons/db.png")
        imgLabel = QtGui.QLabel(about)
        imgLabel.setPixmap(pixmap)
        imgLabel.move(225, 15)

        label = QtGui.QLabel(u"<center>Tinysqlite - программа для</center>\n<center>\
            работы с базой данных SQLite</center>\n<center>\
            Исходники проекта:</center>\n<center>\
            <a href='https://github.com/zhzhussupovkz/tinysqlite'>\
            https://github.com/zhzhussupovkz/tinysqlite</a></center>\n\n<center>\
            Автор: </center>\n<center><a href='mailto:zhzhussupovkz@gmail.com'>zhzhussupovkz@gmail.com</a></center>", about)
        label.move(100, 50)

        license = QtGui.QLabel(u"<center>Распространяется под</center>\n<center>\
            лицензией MIT License</center>\n<center>%s</center>" % datetime.now().year, about)
        license.move(150, 200)

        about.resize(480, 240)
        about.show()

    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width())/2, (screen.height() - size.height())/2)

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, u"Сообщение", u"Покинуть приложение?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            if self.conn:
                self.conn.close()
            event.accept()
        else:
            event.ignore()

    def showDbStructure(self):
        c = self.conn.cursor()
        c.execute("select name from sqlite_master where type = 'table';")
        tables = c.fetchall()
        data = {}
        for k in tables:
            data[k[0]] = [u"Данные", u"Схема"]
        self.dbTreeWidget = QtGui.QTreeWidget()
        header = QtGui.QTreeWidgetItem([u"База данных %s" % self.currentDbName])
        self.dbTreeWidget.clear()
        self.dbTreeWidget.setHeaderItem(header)
        self.dbTreeWidget.setFixedHeight(128)
        self.fillDbStructure(self.dbTreeWidget.invisibleRootItem(), data)
        self.setCentralWidget(self.dbTreeWidget)

    def fillDbStructure(self, item, value):
        item.setExpanded(False)
        if type(value) is dict:
            for key, val in sorted(value.iteritems()):
                child = QtGui.QTreeWidgetItem()
                child.setIcon(0, QtGui.QIcon("./icons/table/table.png"))
                child.setText(0, unicode(key))
                self.currentTableName = unicode(key)
                item.addChild(child)
                self.fillDbStructure(child, val)
        elif type(value) is list:
            for val in value:
                child = QtGui.QTreeWidgetItem()
                item.addChild(child)
                if val == u"Данные":
                    child.setIcon(0, QtGui.QIcon("./icons/table/data.png"))
                    self.connect(self.dbTreeWidget, QtCore.SIGNAL("itemClicked(QTreeWidgetItem*, int)"), self.getTableData)
                elif val == u"Схема":
                    child.setIcon(0, QtGui.QIcon("./icons/table/structure.png"))
                    self.connect(self.dbTreeWidget, QtCore.SIGNAL("itemClicked(QTreeWidgetItem*, int)"), self.getTableData)
                child.setText(0, unicode(val))
                child.setExpanded(True)

    def getTableData(self, item, column):
        getSelected = self.dbTreeWidget.selectedItems()
        if getSelected:
            tableProperty = unicode(getSelected[0].text(0))
            if tableProperty == u"Данные":
                self.currentTableName = item.parent().text(0)
                c = self.conn.execute("SELECT * FROM %s" % self.currentTableName)
                p = self.conn.execute("PRAGMA table_info(%s)" % self.currentTableName)
                data = c.fetchall()
                if filter(None, data):
                    self.statusBar().showMessage(u"В таблице %s - %s записей" % (self.currentTableName, len(data)))
                    self.table = QtGui.QTableWidget()
                    self.table.setSortingEnabled(True)
                    self.table.setWindowTitle('Tinysqlite - %s.%s' % (self.currentDbName, self.currentTableName))
                    self.table.setWindowIcon(QtGui.QIcon("icons/db.png"))
                    self.table.setRowCount(0)
                    self.table.setColumnCount(len(p.fetchall()))
                    for i, row in enumerate(data):
                        self.table.insertRow(i)
                        for j, val in enumerate(row):
                            self.table.setItem(i, j, QtGui.QTableWidgetItem(str(val)))

                    screen = QtGui.QDesktopWidget().screenGeometry()
                    size = self.table.geometry()
                    self.table.move((screen.width() - size.width())/2, (screen.height() - size.height())/2)
                    self.table.resize(480, 480)
                    self.table.show()
                else:
                    self.statusBar().showMessage(u"В таблице %s нет записей" % self.currentTableName)
                c.close()
            elif tableProperty == u"Схема":
                self.currentTableName = item.parent().text(0)
                c = self.conn.execute("SELECT * FROM %s LIMIT 1" % self.currentTableName)
                c.close()

app = QtGui.QApplication(sys.argv)
mw = Main()
mw.show()
sys.exit(app.exec_())
