from PyQt6.QtWidgets import QMessageBox


def generic_error(text, title):
    msg = QMessageBox()
    msg.setText(text)
    msg.setWindowTitle(title)
    retval = msg.exec()
