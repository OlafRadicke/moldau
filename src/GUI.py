#!/usr/bin/python

# Sempel Source: http://www.saltycrane.com/blog/2008/01/pyqt-43-simple-qabstractlistmodel/
# http://zetcode.com/tutorials/pyqt4/german/menusandtoolbars/
# http://stackoverflow.com/questions/1100775/create-pyqt-menu-from-a-list-of-strings

import sys
from PyQt4.QtCore import * 
from PyQt4.QtGui import * 
from PyQt4 import QtGui


#################################################################### 
def main(): 
    app = QApplication(sys.argv) 
    w = MainWindow() 
    w.show() 
    sys.exit(app.exec_()) 

#################################################################### 
class MainWindow(QtGui.QMainWindow): 
    def __init__(self, *args): 
        QWidget.__init__(self, *args) 

        # pseudo data
        _list_data = [1,2,3,4]
        _lm = MyListModel(_list_data, self)


        # Main layout
        _hMainLayout = QHBoxLayout()
        self.setCentralWidget(_hMainLayout)

	# VBox left
        _vListLayoutL = QVBoxLayout()
        _hMainLayout.addLayout(_vListLayoutL) 

        # create table
        _listview = QListView()
        _listview.setModel(_lm)
        _vListLayoutL.addWidget(_listview)


	# VBox Right
        _vListLayoutR = QVBoxLayout()
        _hMainLayout.addLayout(_vListLayoutR) 

        # create Rigth table
        _listviewR = QListView()
        _listviewR.setModel(_lm)
        _vListLayoutR.addWidget(_listviewR)

        # Statusbar
        #self.statusBar().showMessage('Ready')


#################################################################### 
class MyListModel(QAbstractListModel): 
    def __init__(self, datain, parent=None, *args): 
        """ datain: a list where each item is a row
        """
        QAbstractListModel.__init__(self, parent, *args) 
        self.listdata = datain
 
    def rowCount(self, parent=QModelIndex()): 
        return len(self.listdata) 
 
    def data(self, index, role): 
        if index.isValid() and role == Qt.DisplayRole:
            return QVariant(self.listdata[index.row()])
        else: 
            return QVariant()

####################################################################
if __name__ == "__main__": 
    main()
