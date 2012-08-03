from abjad.tools import durationtools
from experimental.selectortools.BackgroundElementSliceSelector import BackgroundElementSliceSelector


class BackgroundMeasureSliceSelector(BackgroundElementSliceSelector):
    r'''.. versionadded:: 1.0

    Select all measures in score::

        >>> from experimental import *

    ::

        >>> selectortools.BackgroundMeasureSliceSelector()
        BackgroundMeasureSliceSelector()

    Select measures from ``3`` forward::

        >>> selectortools.BackgroundMeasureSliceSelector(start_identifier=3)
        BackgroundMeasureSliceSelector(start_identifier=3)

    Select measures up to but not including ``6``::

        >>> selectortools.BackgroundMeasureSliceSelector(stop_identifier=6)
        BackgroundMeasureSliceSelector(stop_identifier=6)

    Select measures from ``3`` up to but not including ``6``::

        >>> selectortools.BackgroundMeasureSliceSelector(start_identifier=3, stop_identifier=6)
        BackgroundMeasureSliceSelector(start_identifier=3, stop_identifier=6)

    Select all measures starting during segment ``'red'``::

        >>> timespan = selectortools.SegmentItemSelector(identifier='red')
        >>> inequality = timespantools.expr_starts_during_timespan(timespan=timespan)

    ::

        >>> selector = selectortools.BackgroundMeasureSliceSelector(inequality=inequality)

    ::

        >>> z(selector)
        selectortools.BackgroundMeasureSliceSelector(
            inequality=timespantools.TimespanInequality(
                timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                timespantools.SingleSourceTimespan(
                    selector=selectortools.SegmentItemSelector(
                        identifier='red'
                        )
                    )
                )
            )

    Select the last two measures during segment ``'red'``::

        >>> selector = selectortools.BackgroundMeasureSliceSelector(inequality=inequality, start_identifier=-2)

    ::
    
        >>> z(selector)
        selectortools.BackgroundMeasureSliceSelector(
            inequality=timespantools.TimespanInequality(
                timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                timespantools.SingleSourceTimespan(
                    selector=selectortools.SegmentItemSelector(
                        identifier='red'
                        )
                    )
                ),
            start_identifier=-2
            )

    Select all the measures that start during the three contiguous segments starting with ``'red'``::

        >>> expr = helpertools.SegmentIdentifierExpression("'red' + 3")
        >>> selector = selectortools.SegmentSliceSelector(start_identifier='red', stop_identifier=expr)
        >>> inequality = timespantools.expr_starts_during_timespan(timespan=selector)

    ::
    
        >>> selector = selectortools.BackgroundMeasureSliceSelector(inequality=inequality)

    ::

        >>> z(selector)
        selectortools.BackgroundMeasureSliceSelector(
            inequality=timespantools.TimespanInequality(
                timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                timespantools.SingleSourceTimespan(
                    selector=selectortools.SegmentSliceSelector(
                        start_identifier='red',
                        stop_identifier=helpertools.SegmentIdentifierExpression("'red' + 3")
                        )
                    )
                )
            )

    Select the last two measures that start during the three contiguous segments starting with ``'red'``::

        >>> selector = selectortools.BackgroundMeasureSliceSelector(inequality=inequality, start_identifier=-2)

    ::

        >>> z(selector)
        selectortools.BackgroundMeasureSliceSelector(
            inequality=timespantools.TimespanInequality(
                timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                timespantools.SingleSourceTimespan(
                    selector=selectortools.SegmentSliceSelector(
                        start_identifier='red',
                        stop_identifier=helpertools.SegmentIdentifierExpression("'red' + 3")
                        )
                    )
                ),
            start_identifier=-2
            )

    Measure slice selectors are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, inequality=None, start_identifier=None, stop_identifier=None):
        from abjad.tools import measuretools
        BackgroundElementSliceSelector.__init__(self, measuretools.Measure,
            inequality=inequality, start_identifier=start_identifier, stop_identifier=stop_identifier)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def context_name(self):
        '''Return none.
        '''
        return

    @property
    def context_names(self):
        '''Return empty list.
        '''
        return []

    @property
    def segment_identifier(self):
        '''Return ``self.inequality.segment_identifier``.
        '''
        return self.inequality.segment_identifier

    ### PUBLIC METHODS ###

    def get_duration(self, score_specification):
        '''Calculcate making assumptions about segment to which selector refers.
        '''
        segment_specification = score_specification.get_segment_specification(self)
        start, stop = self.identifiers
        time_signatures = segment_specification.time_signatures[start:stop]
        durations = [durationtools.Duration(x) for x in time_signatures]
        duration = durationtools.Duration(sum(durations))
        return duration

    def get_segment_start_offset(self, score_specification):
        segment_specification = score_specification.get_segment_specification(self)
        start, stop = self.identifiers
        start = start or 0
        durations = [durationtools.Duration(x) for x in segment_specification.time_signatures]     
        durations_before = durations[:start]
        duration_before = sum(durations_before)
        start_offset = durationtools.Offset(duration_before)
        return start_offset

    def get_segment_stop_offset(self, score_specification):
        segment_specification = score_specification.get_segment_specification(self)
        start, stop = self.identifiers
        durations = [durationtools.Duration(x) for x in segment_specification.time_signatures]     
        durations_up_through = durations[:stop]
        duration_up_through = sum(durations_up_through)
        stop_offset = durationtools.Offset(duration_up_through)
        return stop_offset
