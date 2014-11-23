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

class Main(QtGui.QMainWindow):

  def __init__(self):
    QtGui.QMainWindow.__init__(self)

    self.setWindowTitle('DBAdmin')
    self.setWindowIcon(QtGui.QIcon("icons/db.png"))
    self.resize(640, 480)

    menubar = self.menuBar()
    self.generate_menu(menubar)
    self.generate_test_db()
    self.center()

    self.statusBar().showMessage(u"Готово")

  def generate_test_db(self):
    conn = sqlite3.connect("./db/test.db")
    conn.close()

  def generate_menu(self, menubar):
    file = menubar.addMenu(u"&Файл")
    help = menubar.addMenu(u"&Помощь")
    toolbar = self.addToolBar(u"Главная")

    dbAdd = QtGui.QAction(QtGui.QIcon('./icons/db_add.png'), u'Подключиться к БД', self)
    dbAdd.setShortcut("Ctrl+C")
    dbAdd.setStatusTip(u"Подключиться к базе данных")
    file.addAction(dbAdd)
    toolbar.addAction(dbAdd)

    dbRefresh = QtGui.QAction(QtGui.QIcon('./icons/db_refresh.png'), u'Обновить БД', self)
    dbRefresh.setShortcut("Ctrl+R")
    dbRefresh.setStatusTip(u"Обновить информацию о базе данных")
    file.addAction(dbRefresh)
    toolbar.addAction(dbRefresh)

    dbDelete = QtGui.QAction(QtGui.QIcon('./icons/db_delete.png'), u'Отключиться от БД', self)
    dbDelete.setShortcut("Ctrl+D")
    dbDelete.setStatusTip(u"Отключиться от базы данных")
    file.addAction(dbDelete)
    toolbar.addAction(dbDelete)

    exit = QtGui.QAction(QtGui.QIcon('./icons/exit.png'), u'Выход', self)
    exit.setShortcut("Ctrl+Q")
    exit.setStatusTip(u"Выход")
    file.addAction(exit)
    toolbar.addAction(exit)
    self.connect(exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))

    about = QtGui.QAction(QtGui.QIcon('./icons/star.png'), u'О программе', self)
    about.setStatusTip(u"Информация о программе")
    help.addAction(about)

  def center(self):
    screen = QtGui.QDesktopWidget().screenGeometry()
    size = self.geometry()
    self.move((screen.width() - size.width())/2, (screen.height() - size.height())/2)

  def closeEvent(self, event):
    reply = QtGui.QMessageBox.question(self, u"Сообщение", u"Покинуть приложение?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
    if reply == QtGui.QMessageBox.Yes:
      event.accept()
    else:
      event.ignore()

app = QtGui.QApplication(sys.argv)
mw = Main()
mw.show()
sys.exit(app.exec_())
