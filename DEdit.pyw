import sys
import os

from PyQt5.QtWidgets import QTextEdit, QToolBar, QTabWidget, QMainWindow,\
    QApplication, QFileDialog, QMessageBox
import qdarkstyle

import syntax
import UI
import Helpers
import FileHelper


class Editer(QMainWindow, QTextEdit):
    def __init__(self, parent=None):
        myclass = Editer
        super(myclass, self).__init__(parent)
        # Created all Tables
        self.all_buttons = []
        self.fullname = []

        # All Class Definitions
        self.tabWidget = QTabWidget(self)
        self.toolbar = QToolBar()

        # Call my UI
        UI.ui_look(self)

    def create_tab(self, content="", filename="New"):
        result = Helpers.check_exist_filename(self, filename)
        if result is True:
            if filename is "New":
                self.create_tab(content="", filename="New " + str(len(self.fullname) - 1))
            else:
                self.create_msg("Exist", "You have open this file on tab ")
        elif result is False:
            # Add Tab
            tab = QTextEdit()
            self.tabWidget.addTab(tab, filename)
            tab.setStyleSheet("color: rgb(255,255,255);"
                              "background-color: rgb(50,65,74);"
                              "font-size: 18px;"
                              "font-family: Courier;")
            try:
                tab.setText(content)
            except TypeError:
                pass
            self.highlight = syntax.Highlighter(tab.document())
            self.fullname.append(filename)
            print(filename)
            self.tabWidget.setCurrentWidget(tab)
            self.tabWidget.setTabIcon(Helpers.get_tab_index(self.tabWidget), FileHelper.get_image('file.png'))
            self.tabWidget.setTabsClosable(True)

    def create_msg(self, title, text):
        msg = QMessageBox
        msg.information(self, title, text, msg.Yes)

    def load_file(self):
        try:
            type_to_load = "Daedalus (*.d) ;; ModelScript (*.mds);; Source Scripts(*src)"
            name, _ = QFileDialog.getOpenFileName(self, 'Open File', '\\*.d', type_to_load)
            file = open(name, 'r')
            temp = os.path.splitext(name)[0]

            with file:
                text = file.read()
                self.create_tab(text, os.path.basename(temp))

        except FileNotFoundError:
            pass
        except TypeError:
            pass

    def file_save(self):
        try:
            type_to_save = "Daedalus (*.d) ;; ModelScript (*.mds);; Source Scripts(*src)"
            name, _ = QFileDialog.getSaveFileName(self, 'Save File', '', type_to_save)
            file = open(name, "w")
            tab = Helpers.get_tab_object(self.tabWidget)
            text = tab.toPlainText()
            file.write(text)
            file.close()
        except FileNotFoundError:
            pass
        except PermissionError:
            pass

    def closeEvent(self, event):
        event.ignore()
        self.close_application()

    def close_application(self):
        msg = QMessageBox
        choice = msg.question(self, "Close", "Really you want close?", msg.Yes | msg.No)
        if choice == msg.Yes:
            sys.exit()
        else:
            pass

    def remove_tab(self, index):
        try:
            self.fullname.remove(self.tabWidget.tabText(index))
            self.tabWidget.removeTab(index)
        except ValueError:
            pass


if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setStyle("fusion")
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    myclass = Editer()
    sys.exit(app.exec_())
