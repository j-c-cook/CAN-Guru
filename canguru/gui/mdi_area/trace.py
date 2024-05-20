import copy
from typing import List

from PyQt6.QtWidgets import QTreeWidgetItem

from canguru.message import Message as GuruMessage
from canguru import j1939

import can
import cantools
from PyQt6.QtCore import QThread, pyqtSignal


class Trace(QThread):

    message = pyqtSignal(GuruMessage)

    def __init__(self, treeWidget, dbs):
        super().__init__()
        self.can_bus: can.Bus = None

        self.treeWidget = treeWidget

        self.dbs: List[cantools.db.Database] = dbs

        self.start_time = None

        self.should_run = True

    def add_msg(self, msg: GuruMessage):
        if msg is None:
            return

        tree = self.treeWidget

        pdu = j1939.PDU(msg.arbitration_id)

        # Add root with child
        root = QTreeWidgetItem(tree)
        root.setText(0, "{:4f}".format(msg.timestamp - self.start_time))
        root.setText(1, msg.channel)
        root.setText(2, hex(pdu.pgn))
        if msg.decoded is not None:
            root.setText(3, msg.db.name)
        root.setText(4, hex(pdu.source_address))
        root.setText(5, hex(pdu.pdu_specific))
        root.setText(6, hex(msg.arbitration_id))
        root.setText(7, str(msg.dlc))

        # convert it to hex
        s = []
        for i in range(msg.dlc):
            hex_value = hex(msg.data[i])[2:].zfill(2)
            s.append(hex_value)
        s = ' '.join(s)
        root.setText(8, s)

        if msg.decoded is None:
            return

        for i, signal in enumerate(msg.decoded):
            child = QTreeWidgetItem(root)
            child.setText(0, f'{signal}')
            child.setText(1, f'{msg.decoded[signal]}')

    def run(self):
        self.start_time = None
        self.should_run = True

        if self.can_bus is None:
            return

        dbs = copy.deepcopy(self.dbs)

        try:
            while self.should_run:
                can_msg = self.can_bus.recv(1)
                if can_msg is None:
                    continue

                if self.start_time is None:
                    self.start_time = can_msg.timestamp

                guru_msg: GuruMessage = GuruMessage(can_msg)
                guru_msg.decode(dbs)

                self.message.emit(guru_msg)

        except KeyboardInterrupt:
            pass
        finally:
            self.can_bus.shutdown()
