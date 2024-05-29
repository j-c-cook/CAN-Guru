import sys

import canguru.gui.top_tab_widget.run
from gui.guru import Ui_MainWindow
from canguru.gui import mdi_area, top_tab_widget

from PyQt6 import QtWidgets


class App(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        self.setupUi(self)

        # Manually create the Setup sub window to enable the creation of a custom GLWidget
        self.subwindow_setup = QtWidgets.QWidget()
        self.subwindow_setup.setObjectName("subwindow_setup")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.subwindow_setup)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.openGLWidget_setup = mdi_area.setup.SetupOpenGLWidget(parent=self.subwindow_setup)
        self.openGLWidget_setup.setObjectName("openGLWidget_setup")
        self.gridLayout_3.addWidget(self.openGLWidget_setup, 0, 0, 1, 1)
        self.subwindow_setup.setWindowTitle("Setup")
        self.subwindow_setup.setGeometry(0, 0, 400, 300)

        self.add_sub_windows()

        # Top Tab Widgets
        self.interface = top_tab_widget.interface.Interface(
            self.pushButton_refreshInterfaces, self.comboBox)
        self.interface.interface_options.connect(self.interface.update_interface_options)

        # MDI Widgets
        self.databases = mdi_area.databases.Databases(
            self.pushButton_openDBC, self.listWidget_databases)
        self.trace_thread = mdi_area.trace.Trace(
            self.treeWidget_trace, self.databases.dbs
        )
        self.trace_thread.message.connect(self.trace_thread.add_msg)

        # Top Tab Widgets continued
        self.run = canguru.gui.top_tab_widget.run.Run(
            self.interface, self.trace_thread
        )
        self.pushButton_start.clicked.connect(self.run.start)
        self.pushButton_stop.clicked.connect(self.run.stop)

    def add_sub_windows(self):
        # pyuic6 *.ui -o *.py does not include this, possibly missing a setting
        self.mdiArea.addSubWindow(self.subwindow_trace)
        self.mdiArea.addSubWindow(self.subwindow_configuration)
        self.mdiArea.addSubWindow(self.subwindow_databases)
        self.mdiArea.addSubWindow(self.subwindow_setup)


def main():
    # Start the application
    can_guru_app = QtWidgets.QApplication(sys.argv)
    # Load the form from the tri-calc app
    form = App()
    form.show()
    can_guru_app.exec()


if __name__ == '__main__':
    main()
