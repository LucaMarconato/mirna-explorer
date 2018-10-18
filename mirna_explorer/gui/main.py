import sys
from PySide2.QtWidgets import (QLabel, QWidget, QMainWindow, QApplication, QAction, 
                               QFileDialog, QGridLayout, QVBoxLayout, QPushButton)
from graph import Graph


class MirnaExplorer(QMainWindow):
    
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle(self.tr('Mirna Explorer'))
        
        self.test_widget = Graph(self)
        self.setCentralWidget(self.test_widget)
        
        self.createMenus()       
        
    def createMenus(self):
        fileMenu = self.menuBar().addMenu("&File")
        toolMenu = self.menuBar().addMenu("&Tools")

        openAction = self.createAction("&Open...", fileMenu, self.openFile)
        saveAction = self.createAction("&Save As...", fileMenu, self.saveFile)
        fileMenu.addSeparator()
        exitAction = self.createAction("E&xit", fileMenu, self.close)

        addAction = self.createAction("&Add Entry...", toolMenu, self.hello)
        self.editAction = self.createAction("&Edit Entry...", toolMenu, self.hello)
        toolMenu.addSeparator()
        self.removeAction = self.createAction("&Remove Entry", toolMenu, self.hello)
        
        self.editAction.setEnabled(False)
        self.removeAction.setEnabled(False)
        
    def createAction(self, text, menu, slot):
        action = QAction(text, self)
        menu.addAction(action)
        action.triggered.connect(slot)
        return action
        
    def openFile(self):
        filename, _ = QFileDialog.getOpenFileName(self)

    def saveFile(self):
        filename, _ = QFileDialog.getSaveFileName(self)

    def updateActions(self, selection):
        indexes = selection.indexes()

        if len(indexes) > 0:
            self.removeAction.setEnabled(True)
            self.editAction.setEnabled(True)
        else:
            self.removeAction.setEnabled(False)
            self.editAction.setEnabled(False)
            
    def hello(self):
        print('hello')


def run_app():
    app = QApplication(sys.argv)
    
    window = MirnaExplorer()
    window.show()
    
    sys.exit(app.exec_())
