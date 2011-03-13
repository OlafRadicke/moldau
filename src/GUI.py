#!/usr/bin/python

# Sempel Source: http://www.saltycrane.com/blog/2008/01/pyqt-43-simple-qabstractlistmodel/
# http://zetcode.com/tutorials/pyqt4/german/menusandtoolbars/
# http://stackoverflow.com/questions/1100775/create-pyqt-menu-from-a-list-of-strings

import sys
#from PyQt4.QtCore import * 
#from PyQt4.QtGui import * 
#from PyQt4 import QtGui
from PyQt4 import QtGui, QtCore


#################################################################### 
def main(): 
    app = QtGui.QApplication(sys.argv)
    w = MainWindow()
    w.show() 
    sys.exit(app.exec_())

##################################################################
class MainWindow(QtGui.QMainWindow):

    ## pseudo data
    list_data  = [1,2,3,4]

    ## Constructor
    def __init__(self, *args): 
        QtGui.QWidget.__init__(self, *args) 

        # pseudo data
        lm = MyListModel(self.list_data, self)

        ## menubar
        exit = QtGui.QAction(QtGui.QIcon('icons/exit.png'), 'Exit', self)
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip('Exit application')
        self.connect(exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))



        
        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        file.addAction(exit)



        # Main Widget
        centralWidget = QtGui.QWidget()
        self.setCentralWidget(centralWidget)

        # Main layout
        hMainLayout = QtGui.QHBoxLayout()
        centralWidget.setLayout(hMainLayout)

	# VBox left
        vListLayoutL = QtGui.QVBoxLayout()
        hMainLayout.addLayout(vListLayoutL)

        # create table
        listview = QtGui.QListView()
        listview.setModel(lm)
        vListLayoutL.addWidget(listview)


	# VBox Right
        vListLayoutR = QtGui.QVBoxLayout()
        hMainLayout.addLayout(vListLayoutR)

        # create Rigth table
        listviewR = QtGui.QListView()
        listviewR.setModel(lm)
        vListLayoutR.addWidget(listviewR)

        # Statusbar
        self.statusBar().showMessage('Ready')


#################################################################### 
class MyListModel(QtCore.QAbstractListModel):
    def __init__(self, datain, parent=None, *args): 
        """ datain: a list where each item is a row
        """
        QtCore.QAbstractListModel.__init__(self, parent, *args)
        self.listdata = datain
 
    def rowCount(self, parent=QtCore.QModelIndex()): 
        return len(self.listdata) 
 
    def data(self, index, role): 
        if index.isValid() and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self.listdata[index.row()])
        else: 
            return QtCore.QVariant()

####################################################################


main()
