from abjad.tools.abctools.AbjadObject import AbjadObject


class TimespanInequality(AbjadObject):
    r'''.. versionadded:: 1.0

    SingleSourceTimespan inequality.

    Test for all objects that start during segment ``'red'``::

        >>> from experimental import *

    ::

        >>> segment_selector = selectortools.SingleSegmentSelector(identifier='red')
        >>> timespan_inequality = timespantools.expr_starts_during_timespan(timespan=segment_selector.timespan)

    ::

        >>> z(timespan_inequality)
        timespantools.TimespanInequality(
            timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
            timespantools.SingleSourceTimespan(
                selector=selectortools.SingleSegmentSelector(
                    identifier='red'
                    )
                )
            )

    SingleSourceTimespan inequalities are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, timespan_inequality_template, timespan):
        from experimental import timespantools
        timespan = timespantools.expr_to_timespan(timespan)
        assert isinstance(timespan_inequality_template, timespantools.TimespanInequalityTemplate), repr(
            timespan_inequality_template)
        self._timespan = timespan
        self._timespan_inequality_template = timespan_inequality_template

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if isinstance(expr, type(self)):
            if self.timespan_inequality_template == expr.timespan_inequality_template:
                if self.timespan == expr.timespan:
                    return True
        return False

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def segment_identifier(self):
        '''Delegate to ``self.timespan.segment_identifier``.
        '''
        return self.timespan.segment_identifier

    @property
    def timespan(self):
        '''SingleSourceTimespan of inequality.

        Return timespan object.
        '''
        return self._timespan

    @property
    def timespan_inequality_template(self):
        '''Class of inequality.

        Return timespan inequality or timespan inequality template object.
        '''
        return self._timespan_inequality_template

    ### PUBLIC METHODS ###

    def get_duration(self, score_specification):
        '''Delegate to ``self.timespan.get_duration()``.
        '''
        return self.timespan.get_duration(score_specification)
