from typing import Union

import can
import cantools
from cantools.typechecking import DecodeResultType


class Message(can.Message):
    def __init__(self, can_msg: can.Message):
        attr_dict = {k: getattr(can_msg, k) for k in can_msg.__slots__ if k != '__weakref__'}
        super(Message, self).__init__(**attr_dict)
        self.db: Union[cantools.db.Message, None] = None
        self.decoded: Union[DecodeResultType, None] = None

    def decode(self, dbs, allow_truncated=True):
        for _, db in enumerate(dbs):
            try:
                self.db = db.get_message_by_frame_id(self.arbitration_id)
            except KeyError:
                continue
            try:
                self.decoded: DecodeResultType = self.db.decode(
                    self.data, allow_truncated=allow_truncated)
            except cantools.db.errors.DecodeError:
                continue
