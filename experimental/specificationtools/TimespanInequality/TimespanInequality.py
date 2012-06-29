from abjad.tools.abctools.AbjadObject import AbjadObject


class TimespanInequality(AbjadObject):
    r'''.. versionadded:: 1.0

    Inequality that relates durated score object ``x``
    to reference timespan ``t``.

    Score object starts during timespan::

        >>> from experimental import specificationtools

    ::

        >>> timespantools.TimespanInequality('t.start <= x.start < t.stop')
        TimespanInequality('t.start <= x.start < t.stop')

    Score object stops during timespan::

        >>> timespantools.TimespanInequality('t.start < x.stop <= t.stop')
        TimespanInequality('t.start < x.stop <= t.stop')

    Score object both starts and stops during timespan::

        >>> timespantools.TimespanInequality('t.start <= x.start < x.stop <= t.stop')
        TimespanInequality('t.start <= x.start < x.stop <= t.stop')
        
    Timepsan objects perform no input checking.

    Timespan objects share many qualities with lamba expressions.
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
