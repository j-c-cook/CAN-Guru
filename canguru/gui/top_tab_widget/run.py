import can

import canguru.utils
from canguru.gui.top_tab_widget.interface import Interface
from canguru.gui.mdi_area.trace import Trace


class Run:
    def __init__(self, interface: Interface, trace_thread: Trace):
        self.interface = interface
        self.trace_thread = trace_thread

    def start(self):
        # TODO: Handle files from system

        if self.trace_thread.isRunning():
            return

        interface, channel = self.interface.get()

        if interface is None:
            return

        try:
            self.trace_thread.can_bus = can.Bus(
                interface=interface, channel=channel, bitrate=250000
            )
        except (can.exceptions.CanInterfaceNotImplementedError, OSError) as m:
            canguru.utils.generic_error(
                "Interface back-end is not supported or device is not mounted.", m.strerror
            )
            return

        self.trace_thread.start()

    def stop(self):
        self.trace_thread.should_run = False
