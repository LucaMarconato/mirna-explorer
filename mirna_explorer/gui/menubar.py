import PySide2.QtWidgets as QtWidgets
import PySide2.QtGui as QtGui


class Menubar:

    def __init__(self, app):
        self._app = app
        self._menubar = app.menuBar()
        self.add_file_menu()

    def add_file_menu(self):
        action = self._create_action
        keys = QtGui.QKeySequence

        new_action = action('&New', self._new, keys.New)
        open_action = action('&Open...', self._open, keys.Open)
        save_action = action('&Save', self._save, keys.Save)
        save_as_action = action('Save As...', self._save_as, keys.SaveAs)
        import_action = action('Import...', self._import)
        export_action = action('Export...', self._export)
        exit_action = action('&Exit', self._app.close, keys.Quit)
        
        file_menu = self._menubar.addMenu('&File')
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(save_as_action)
        file_menu.addSeparator()
        file_menu.addAction(import_action)
        file_menu.addAction(export_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

    def add_edit_menu(self):
        pass

    def add_view_menu(self):
        pass

    def add_help_menu(self):
        pass

    def _new(self):
        print('new')

    def _open(self):
        print('open')

    def _save(self):
        print('save')

    def _save_as(self):
        print('save as')

    def _import(self):
        print('import')

    def _export(self):
        print('export')

    def _create_action(self, text, fnc, shortcut=None):
        action = QtWidgets.QAction(text, self._app)
        if shortcut is not None:
            action.setShortcut(shortcut)
        action.triggered.connect(lambda: fnc())
        return action
