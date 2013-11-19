# -*- encoding: utf-8 -*-
from abjad.tools.quantizationtools.QEvent import QEvent


class TerminalQEvent(QEvent):
    r'''The terminal event in a series of ``QEvents``:

        >>> q_event = quantizationtools.TerminalQEvent(1000)
        >>> print format(q_event)
        quantizationtools.TerminalQEvent(
            durationtools.Offset(1000, 1)
            )

    Carries no significance outside the context of a ``QEventSequence``.

    Return ``TerminalQEvent`` instance.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_offset',
        )

    ### INITIALIZER ###

    def __init__(self, offset):
        QEvent.__init__(self, offset)

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if type(self) == type(expr) and \
            self.offset == expr.offset:
            return True
        return False
