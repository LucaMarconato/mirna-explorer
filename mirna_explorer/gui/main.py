import PySide2.QtWidgets as QtWidgets
import PySide2.QtGui as QtGui
from gui.graph import Graph


class MirnaExplorer(QtWidgets.QMainWindow):
    
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setWindowTitle(self.tr('Mirna Explorer'))
        self.resize(1024, 768)
        
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
        action = QtWidgets.QAction(text, self)
        menu.addAction(action)
        action.triggered.connect(slot)
        return action
        
    def openFile(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self)
        
    def saveFile(self):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self)

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
