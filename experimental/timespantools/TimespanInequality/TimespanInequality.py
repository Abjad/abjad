from abjad.tools.abctools.AbjadObject import AbjadObject


class TimespanInequality(AbjadObject):
    r'''.. versionadded:: 1.0

    Timespan inequality.

    Test for all objects that start during segment ``'red'``::

        >>> from experimental import specificationtools
        >>> from experimental import timespantools

    ::

        >>> reference = specificationtools.BackgroundElementSelector(specificationtools.Segment, 'red')
        >>> inequality = timespantools.expr_starts_during_timespan()

    ::

        >>> timespan_inequality = timespantools.TimespanInequality(reference.timespan, inequality)

    ::

        >>> z(timespan_inequality)
        timespantools.TimespanInequality(
            timespantools.Timespan(
                selector=specificationtools.BackgroundElementSelector(
                    specificationtools.Segment,
                    'red'
                    )
                ),
            timespantools.TimespanInequalityClass(
                't.start <= expr.start < t.stop'
                )
            )

    Timespan inequalities are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, timespan, timespan_inequality_class):
        from experimental import timespantools
        assert isinstance(timespan, timespantools.Timespan), repr(timespan)
        assert isinstance(timespan_inequality_class, timespantools.TimespanInequalityClass), repr(
            timespan_inequality_class)
        self._timespan = timespan
        self._timespan_inequality_class = timespan_inequality_class

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def timespan(self):
        '''Timespan of inequality.

        Return timespan object.
        '''
        return self._timespan

    @property
    def timespan_inequality_class(self):
        '''Class of inequality.

        Return timespan inequality object.
        '''
        return self._timespan_inequality_class
