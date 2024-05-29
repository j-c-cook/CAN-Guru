from typing import List

from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QDialog

from PyQt6 import QtOpenGLWidgets, QtOpenGL
from abc import ABC, abstractmethod


class BaseBox(ABC):
    def __init__(self, x, y, w, h, parent=None):
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._parent = parent

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def w(self):
        return self._w

    @property
    def h(self):
        return self._h

    @property
    def parent(self):
        return self._parent

    def center(self):
        return self.x + self.w // 2, self.y + self.h // 2

    def top_center(self):
        return self.x + self.w // 2, self.y

    def bottom_center(self):
        return self.x + self.w // 2, self.y + self.h

    def left_center(self):
        return self.x, self.y + self.h // 2

    def right_center(self):
        return self.x + self.w, self.y + self.h // 2

    @abstractmethod
    def paintEvent(self, event, painter):
        pass

    @abstractmethod
    def on_double_click(self):
        pass

    def mouseDoubleClickEvent(self, event):
        # If the mouse double click event occurs within the box, open a new window
        if (self.x < event.position().x() < self.x + self.w and
                self.y < event.position().y() < self.y + self.w):
            self.on_double_click()


class InterfaceBox(BaseBox):
    def __init__(self, parent=None):
        BaseBox.__init__(self, 80, 350, 100, 50, parent)

    def paintEvent(self, event, painter):
        # Draw a red rectangle (50x50 px) at position 10,10
        painter.setPen(QColor(255, 0, 0))  # Color set to red
        painter.drawRect(self.x, self.y, self.w, self.h)

        # Set the color of the text to be drawn
        painter.setPen(QColor(255, 255, 255))

        # Draw text in the middle of the rectangle
        center_x = self.x + self.w // 6
        center_y = self.y + self.h // 3
        painter.drawText(center_x, center_y, "CAN")
        painter.drawText(center_x, center_y + 20, "Interface")

    def on_double_click(self):
        # Create and show a new dialog window
        dialog = QDialog(self.parent)
        dialog.show()


class SelectFilesBox(BaseBox):
    def __init__(self, parent=None):
        BaseBox.__init__(self, 80, 200, 100, 50, parent)

    def paintEvent(self, event, painter):
        # Draw a red rectangle (50x50 px) at position 10,10
        painter.setPen(QColor(255, 0, 0))  # Color set to red
        painter.drawRect(self.x, self.y, self.w, self.h)

        # Set the color of the text to be drawn
        painter.setPen(QColor(255, 255, 255))

        # Draw text in the middle of the rectangle
        center_x = self.x + self.w // 6
        center_y = self.y + self.h // 3
        painter.drawText(center_x, center_y, "Select")
        painter.drawText(center_x, center_y + 20, "Files")

    def on_double_click(self):
        # Create and show a new dialog window
        dialog = QDialog(self.parent)
        dialog.show()


class SelectModeBox(BaseBox):
    def __init__(self, interface_box: InterfaceBox, select_files_box: SelectFilesBox, parent=None):
        BaseBox.__init__(self, 200, 275, 100, 50, parent)

        self.interface_box = interface_box
        self.select_files_box = select_files_box

        self.from_interface = True

    def paintEvent(self, event, painter):
        # Draw a red rectangle (50x50 px) at position 10,10
        painter.setPen(QColor(255, 0, 0))  # Color set to red
        painter.drawRect(self.x, self.y, self.w, self.h)

        # Draw text in the middle of the rectangle
        center_x = self.x + self.w // 7

        if self.from_interface:
            interface_text_color = (255, 255, 255)
            from_file_text_color = (128, 128, 128)
            interface_line_color = (255, 0, 0)  # Red
            from_file_line_color = (128, 128, 128)  # Gray
        else:
            interface_text_color = (128, 128, 128)
            from_file_text_color = (255, 255, 255)
            interface_line_color = (128, 128, 128)  # Gray
            from_file_line_color = (255, 0, 0)  # Red

        painter.setPen(QColor(*interface_text_color))
        painter.drawText(center_x, self.y + self.h - 5, "From Interface")
        painter.setPen(QColor(*from_file_text_color))
        painter.drawText(center_x, self.y + 15, "From Files")

        painter.setPen(QColor(*interface_line_color))
        painter.drawLine(
            QPoint(*self.interface_box.right_center()),
            QPoint(self.bottom_center()[0], self.interface_box.right_center()[1])
        )
        painter.drawLine(
            QPoint(self.bottom_center()[0], self.interface_box.right_center()[1]),
            QPoint(*self.bottom_center())
        )

        painter.setPen(QColor(*from_file_line_color))
        painter.drawLine(
            QPoint(*self.select_files_box.right_center()),
            QPoint(self.bottom_center()[0], self.select_files_box.right_center()[1])
        )
        painter.drawLine(
            QPoint(self.bottom_center()[0], self.select_files_box.right_center()[1]),
            QPoint(*self.top_center())
        )

    def on_double_click(self):
        self.from_interface = not self.from_interface
        self.parent.update()


class TraceBox(BaseBox):
    def __init__(self, center_output_x, center_output_y, parent=None):
        self.center_output_x = center_output_x
        self.center_output_y = center_output_y

        BaseBox.__init__(self, center_output_x + 100, center_output_y - 25, 100, 50, parent)

    def paintEvent(self, event, painter):
        # Draw a red rectangle (50x50 px) at position 10,10
        painter.setPen(QColor(255, 0, 0))  # Color set to red
        painter.drawRect(self.x, self.y, self.w, self.h)

        painter.setPen(QColor(255, 255, 255))
        painter.drawText(self.center()[0] - 15, self.top_center()[1] + 15, "Trace")

        painter.setPen(QColor(255, 0, 0))  # Color set to red

        painter.drawLine(
            QPoint(*self.left_center()),
            QPoint(self.center_output_x, self.center_output_y)
        )

    def on_double_click(self):
        dialog = QDialog(self.parent)
        dialog.show()


class CANOutputs(BaseBox):
    spacing = 75

    def __init__(self, select_mode_box: SelectModeBox, parent=None):
        self.select_mode_box = select_mode_box

        x = self.select_mode_box.right_center()[0] + self.spacing
        y = self.select_mode_box.right_center()[1] - 10

        BaseBox.__init__(self, x, y, 20, 20, parent)

        self.outputs: List[BaseBox] = []

        x, y = self.center()
        self.outputs.append(
            TraceBox(x, y, parent=parent)
        )

    def paintEvent(self, event, painter):
        # Draw a red rectangle (50x50 px) at position 10,10
        painter.setPen(QColor(255, 0, 0))  # Color set to red
        painter.drawRect(self.x, self.y, self.w, self.h)

        painter.drawLine(
            QPoint(*self.select_mode_box.right_center()),
            QPoint(*self.center())
        )

        for output in self.outputs:
            output.paintEvent(event, painter)

    def on_double_click(self):
        pass


class SetupOpenGLWidget(QtOpenGLWidgets.QOpenGLWidget):
    def __init__(self, parent=None):
        super(SetupOpenGLWidget, self).__init__(parent)
        self.setObjectName("openGLWidget_setup")

        self.interface_box = InterfaceBox(self)
        self.select_files_box = SelectFilesBox(self)
        self.select_mode_box = SelectModeBox(self.interface_box, self.select_files_box, parent=self)
        self.can_outputs = CANOutputs(self.select_mode_box, parent=self)

    def initializeGL(self):
        pass

    def paintGL(self):
        pass

    def resizeGL(self, w: int, h: int):
        pass

    def paintEvent(self, event):
        # QPainter object allows painting inside the widget
        painter = QPainter()
        painter.begin(self)

        self.interface_box.paintEvent(event, painter)
        self.select_files_box.paintEvent(event, painter)
        self.select_mode_box.paintEvent(event, painter)
        self.can_outputs.paintEvent(event, painter)

        painter.end()

    def mouseDoubleClickEvent(self, event):
        self.interface_box.mouseDoubleClickEvent(event)
        self.select_files_box.mouseDoubleClickEvent(event)
        self.select_mode_box.mouseDoubleClickEvent(event)
        self.can_outputs.mouseDoubleClickEvent(event)
        for output in self.can_outputs.outputs:
            output.mouseDoubleClickEvent(event)
