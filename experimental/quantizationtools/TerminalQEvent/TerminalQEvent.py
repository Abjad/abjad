from abjad.tools import durationtools
from experimental.quantizationtools.QEvent import QEvent


class TerminalQEvent(QEvent):

    ### CLASS ATTRIBUTES ###

    _fields = ('_offset',)

    ### INITIALIZER ###

    def __new__(cls, offset):
        offset = durationtools.Offset(offset)
        return tuple.__new__(cls, (offset,))
