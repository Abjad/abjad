from abjad.tools.abctools.AbjadObject import AbjadObject


class TimespanInequality(AbjadObject):
    r'''.. versionadded:: 1.0

    Timespan inequality.

    Test for all objects that start during segment ``'red'``::

        >>> from experimental import selectortools
        >>> from experimental import specificationtools
        >>> from experimental import timespantools

    ::

        >>> segment_selector = selectortools.SegmentSelector(index='red')
        >>> timespan_inequality = timespantools.expr_starts_during_timespan(timespan=segment_selector.timespan)

    ::

        >>> z(timespan_inequality)
        timespantools.TimespanInequality(
            timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
            timespantools.Timespan(
                selector=selectortools.SegmentSelector(
                    index='red'
                    )
                )
            )

    Timespan inequalities are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, timespan_inequality_template, timespan):
        from experimental import timespantools
        assert isinstance(timespan, timespantools.Timespan), repr(timespan)
        assert isinstance(timespan_inequality_template, timespantools.TimespanInequalityTemplate), repr(
            timespan_inequality_template)
        self._timespan = timespan
        self._timespan_inequality_template = timespan_inequality_template

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def timespan(self):
        '''Timespan of inequality.

        Return timespan object.
        '''
        return self._timespan

    @property
    def timespan_inequality_template(self):
        '''Class of inequality.

        Return timespan inequality or timespan inequality template object.
        '''
        return self._timespan_inequality_template
