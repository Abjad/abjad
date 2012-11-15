from abjad.tools.quantizationtools.QEvent import QEvent


class TerminalQEvent(QEvent):
    '''The terminal event in a series of ``QEvents``:

        >>> q_event = quantizationtools.TerminalQEvent(1000)
        >>> q_event
        quantizationtools.TerminalQEvent(
            durationtools.Offset(1000, 1)
            )

    Carries no significance outside the context of a ``QEventSequence``.

    Return ``TerminalQEvent`` instance.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_offset',)

    ### INITIALIZER ###

    def __init__(self, offset):
        QEvent.__init__(self, offset)

    ### SPECIAL METHODS ###

    def __eq__(self, other):
        if type(self) == type(other) and \
            self.offset == other.offset:
            return True
        return False
