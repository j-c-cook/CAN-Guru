import os.path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QListWidgetItem, QCheckBox, QWidget, QHBoxLayout, QLabel

from canguru import utils

import cantools


class CustomQWidget(QWidget):
    def __init__(self, text):
        super().__init__()

        self.layout = QHBoxLayout(self)

        self.displayName = QLabel(text)
        self.layout.addWidget(self.displayName)

        self.checkbox = QCheckBox()
        self.layout.addWidget(self.checkbox)


class Databases:
    def __init__(self, pushButton, listWidget):
        self.pushButton = pushButton
        self.listWidget = listWidget

        self.pushButton.clicked.connect(self.call_open_databases)

        self.databases = []

    def call_open_databases(self):
        file_path = utils.file_dialog(
            caption="Open DBC file", file_filter="DBC Files (*.dbc);;All Files (*)")
        if file_path is None:
            return

        item = QListWidgetItem(self.listWidget)
        self.listWidget.addItem(item)

        checkbox = QCheckBox(file_path)
        checkbox.setChecked(True)
        self.listWidget.setItemWidget(item, checkbox)

        self.reload_databases()

    def reload_databases(self):
        self.databases = []
        for index in range(self.listWidget.count()):
            item = self.listWidget.item(index)

            checkbox = self.listWidget.itemWidget(item)
            path_to_database = checkbox.text()

            if not os.path.isfile(path_to_database):
                checkbox.setStyleSheet("color: red")
                checkbox.setChecked(False)
                continue

            if not checkbox.isChecked():
                checkbox.setStyleSheet("color: gray")
                continue

            try:
                db = cantools.db.load_file(path_to_database)
                checkbox.setStyleSheet("color: red")
            except cantools.db.UnsupportedDatabaseFormatError:
                continue

            checkbox.setStyleSheet("color: green")
            self.databases.append(db)
