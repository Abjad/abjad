from experimental.quantizationtools.QEvent import QEvent


class TerminalQEvent(QEvent):

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_offset')

    ### INITIALIZER ###

    def __init__(self, offset):
        QEvent.__init__(self, offset)

    ### SPECIAL METHODS ###

    def __eq__(self, other):
        if type(self) == type(other) and \
            self.offset == other.offset:
            return True
        return False
