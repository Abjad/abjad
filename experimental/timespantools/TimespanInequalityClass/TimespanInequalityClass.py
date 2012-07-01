from abjad.tools.abctools.AbjadObject import AbjadObject


class TimespanInequalityClass(AbjadObject):
    r'''.. versionadded:: 1.0

    Relate expression ``expr`` to timespan ``t``.

    Expresion starts during timespan::

        >>> from experimental import timespantools

    ::

        >>> timespantools.TimespanInequalityClass('t.start <= expr.start < t.stop')
        TimespanInequalityClass('t.start <= expr.start < t.stop')

    Expression stops during timespan::

        >>> timespantools.TimespanInequalityClass('t.start < expr.stop <= t.stop')
        TimespanInequalityClass('t.start < expr.stop <= t.stop')

    Expression both starts and stops during timespan::

        >>> timespantools.TimespanInequalityClass('t.start <= expr.start < expr.stop <= t.stop')
        TimespanInequalityClass('t.start <= expr.start < expr.stop <= t.stop')
        
    Timepsan objects perform no input checking.

    Timespan objects share qualities with lamba expressions.
    '''

    ### INITIALIZER ###

    def __init__(self, string):
        assert isinstance(string, str), repr(string)
        self._string = string

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def string(self):
        '''Inequality string assigned by user.
        '''
        return self._string
