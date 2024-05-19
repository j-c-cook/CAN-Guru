from PyQt6.QtWidgets import QMessageBox, QFileDialog


def generic_error(text, title):
    msg = QMessageBox()
    msg.setText(text)
    msg.setWindowTitle(title)
    retval = msg.exec()


def file_dialog(caption="", directory="", file_filter="All Files (*)"):
    file_name, _ = QFileDialog.getOpenFileName(
        None, caption=caption, directory=directory, filter=file_filter)
    if file_name:
        return file_name


def directory_dialog(caption="Select a Directory"):
    directory = QFileDialog.getExistingDirectory(None, "Select a Directory")
    if directory:
        return directory
