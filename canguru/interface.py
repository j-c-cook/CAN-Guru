from PyQt6.QtCore import QThread, pyqtSignal
import platform
import can

from canguru import utils


class Interface(QThread):

    interface_options = pyqtSignal(str)

    def __init__(self, pushButton, comboBox):
        QThread.__init__(self)

        self.pushButton = pushButton
        self.comboBox = comboBox

        self.pushButton.clicked.connect(self.refresh_interfaces)

    def call_refresh_interfaces(self):
        if self.isRunning():
            return
        self.comboBox.clear()
        self.run()

    def update_interface_options(self, available_interface):
        if 'Error' in available_interface:
            err_msg = available_interface.split(':')
            return utils.generic_error(err_msg[1], err_msg[0])
        self.comboBox.addItem(available_interface)

    def refresh_interfaces(self):
        system = platform.system()
        if system == 'Linux':
            interfaces = ['socketcan']
        elif system == 'Windows':
            interfaces = ['vector', 'pcan']
        else:
            return 'OS Error: System is not supported.'

        available_interfaces = can.detect_available_configs(
            interfaces=interfaces
        )

        for interface in available_interfaces:
            self.interface_options.emit(f'{interface["interface"]}: {interface["channel"]}')
