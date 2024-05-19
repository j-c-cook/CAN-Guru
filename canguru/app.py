import sys

from gui.guru import Ui_MainWindow
from canguru import interface

from PyQt6 import QtWidgets


class App(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        self.setupUi(self)
        self.add_sub_windows()

        self.interface = interface.Interface(self.pushButton_refreshInterfaces, self.comboBox)
        self.interface.interface_options.connect(self.interface.update_interface_options)

    def add_sub_windows(self):
        # pyuic6 *.ui -o *.py does not include this, possibly missing a setting
        self.mdiArea.addSubWindow(self.subwindow_trace)
        self.mdiArea.addSubWindow(self.subwindow_configuration)
        self.mdiArea.addSubWindow(self.subwindow_databases)
        self.mdiArea.addSubWindow(self.subwindow_filtering)


def main():
    # Start the application
    can_guru_app = QtWidgets.QApplication(sys.argv)
    # Load the form from the tri-calc app
    form = App()
    form.show()
    can_guru_app.exec()


if __name__ == '__main__':
    main()
