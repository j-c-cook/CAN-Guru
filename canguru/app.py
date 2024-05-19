import sys

from gui.guru import Ui_MainWindow
from gui.trace import Trace

from PyQt6 import QtWidgets


class App(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        self.setupUi(self)

        self.trace = Trace(self.subwindow_trace)

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
