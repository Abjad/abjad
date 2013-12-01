# -*- encoding: utf-8 -*-
from abjad.tools.quantizationtools.QEvent import QEvent


class TerminalQEvent(QEvent):
    r'''The terminal event in a series of ``QEvents``:

        >>> q_event = quantizationtools.TerminalQEvent(1000)
        >>> print format(q_event)
        quantizationtools.TerminalQEvent(
            offset=durationtools.Offset(1000, 1),
            )

    Carries no significance outside the context of a ``QEventSequence``.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_offset',
        )

    ### INITIALIZER ###

    def __init__(self, offset=0):
        QEvent.__init__(self, offset=offset)

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''True when `expr` is a terminal q-event with offset equal to that of
        this terminal q-event. Otherwise false.

        Returns boolean.
        '''
        if type(self) == type(expr) and \
            self.offset == expr.offset:
            return True
        return False
