import PySide2.QtWidgets as QtWidgets
import PySide2.QtGui as QtGui

FNC = 'function'
KEY = 'shortcut'
SEP = 'separator'


class Menubar:

    def __init__(self, app):
        self._app = app
        self._menubar = app.menuBar()
        keys = QtGui.QKeySequence

        menu = {
            '&File': {
                '&New': {FNC: self._new, KEY: keys.New},
                '&Open': {FNC: self._open, KEY: keys.Open},
                '&Save': {FNC: self._save, KEY: keys.Save},
                'Save As...': {FNC: self._save_as, KEY: keys.SaveAs},
                f'{SEP}1': {},
                'Import...': {FNC: self._import},
                'Export...': {FNC: self._export},
                f'{SEP}2': {},
                '&Exit': {FNC: self._app.close, KEY: keys.Quit}
            },
            '&Edit': {
                'Undo': {FNC: self._undo, KEY: keys.Undo},
                'Redo': {FNC: self._redo, KEY: keys.Redo},
                'Undo History': {FNC: self._undo_history},
                f'{SEP}3': {},
                'Cut': {FNC: self._cut, KEY: keys.Cut},
                'Copy': {FNC: self._copy, KEY: keys.Copy},
                'Paste': {FNC: self._paste, KEY: keys.Paste},
                f'sep4': {},
                'Preferences': {FNC: self._preferences},
                'Keyboard Shortcuts': {FNC: self._kb_shortcuts}
            },
            '&View': {
                'Zoom': {FNC: self._zoom},
                f'{SEP}5': {},
                'Fullscreen': {FNC: self._fullscreen, KEY: keys.FullScreen},
                f'{SEP}6': {},
                'Show Grid': {FNC: self._show_grid},
                'Show Sample Points': {FNC: self._show_sample_pts},
                f'{SEP}7': {},
                'Show Menubar': {FNC: self._show_menubar},
                'Show Statusbar': {FNC: self._show_statusbar}
            },
            '&Help': {
                'Help': {FNC: self._help, KEY: keys.HelpContents},
                'Contact Help': {FNC: self._contact_help},
                'About Mirna Explorer': {FNC: self._about}
            }
        }

        self._create_menu(menu)

    def _create_menu(self, menu_layout):
        for header, entries in menu_layout.items():
            menu = self._menubar.addMenu(header)
            for submenu, opts in entries.items():
                if 'sep' in submenu:
                    menu.addSeparator()
                else:
                    menu.addAction(self._create_action(submenu, **opts))

    def _create_action(self, text, function, shortcut=None):
        action = QtWidgets.QAction(text, self._app)
        if shortcut is not None:
            action.setShortcut(shortcut)
        action.triggered.connect(lambda: function())
        return action

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

    def _undo(self):
        print('undo')

    def _redo(self):
        print('redo')

    def _undo_history(self):
        print('undo_history')

    def _cut(self):
        print('cut')

    def _copy(self):
        print('copy')

    def _paste(self):
        print('paste')

    def _preferences(self):
        print('preferences')

    def _kb_shortcuts(self):
        print('keyboard shortcuts')

    def _zoom(self):
        print('zoom')

    def _fullscreen(self):
        print('fullscreen')

    def _show_grid(self):
        print('show grid')

    def _show_sample_pts(self):
        print('show sample points')

    def _show_menubar(self):
        print('show menubar')

    def _show_statusbar(self):
        print('show statusbar')

    def _help(self):
        print('help')

    def _contact_help(self):
        print('contact help')

    def _about(self):
        print('about')
