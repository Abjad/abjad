from abjad.tools.abctools.AbjadObject import AbjadObject


class TimespanInequality(AbjadObject):
    r'''.. versionadded:: 1.0

    Timespan inequality.

    ::

        >>> from experimental import *

    Test for all objects that start during segment ``'red'``::

        >>> selector = selectortools.SingleSegmentSelector(identifier='red')
        >>> timespan_inequality = timespantools.expr_starts_during_timespan(timespan=selector)

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

    Timespan inequalities are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, timespan_inequality_template, timespan, expr_2=None):
        from experimental import timespantools
        timespan = timespantools.expr_to_timespan(timespan)
        assert isinstance(timespan_inequality_template, timespantools.TimespanInequalityTemplate), repr(
            timespan_inequality_template)
        self._timespan_inequality_template = timespan_inequality_template
        self._timespan = timespan
        self._expr_2 = expr_2

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if isinstance(expr, type(self)):
            if self.timespan_inequality_template == expr.timespan_inequality_template:
                if self.timespan == expr.timespan:
                    if self.expr_2 == expr.expr_2:
                        return True
        return False

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def expr_2(self):
        '''Expression ``2`` of timespan inequality.

        Return arbitrary object.
        '''
        return self._expr_2
        
    @property
    def segment_identifier(self):
        '''Delegate to ``self.timespan.segment_identifier``.
        '''
        return self.timespan.segment_identifier

    @property
    def timespan(self):
        '''Timespan of timespan inequality.

        Return timespan object.
        '''
        return self._timespan

    @property
    def timespan_inequality_template(self):
        '''Class of timespan inequality.

        Return timespan inequality or timespan inequality template object.
        '''
        return self._timespan_inequality_template

    ### PUBLIC METHODS ###

    def get_duration(self, score_specification, context_name):
        '''Delegate to ``self.timespan.get_duration()``.
        '''
        return self.timespan.get_duration(score_specification, context_name)

    def set_segment_identifier(self, segment_identifier):
        '''Delegate to ``self.timespan.set_segment_identifier()``.
        '''
        self.timespan.set_segment_identifier(segment_identifier)
