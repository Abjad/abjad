from abjad.tools import durationtools
from experimental import divisiontools
from experimental.selectortools.InequalitySelector import InequalitySelector
from experimental.selectortools.SliceSelector import SliceSelector


class DivisionSelector(SliceSelector, InequalitySelector):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    Select all divisions::

        >>> selectortools.DivisionSelector()
        DivisionSelector()

    Select all divisions starting during segment ``'red'``::

        >>> segment = selectortools.SingleSegmentSelector(identifier='red')
        >>> timespan = segment.timespan
        >>> inequality = timespantools.expr_2_starts_during_expr_1(expr_1=timespan)

    ::

        >>> divisions = selectortools.DivisionSelector(inequality=inequality)

    ::

        >>> z(divisions)
        selectortools.DivisionSelector(
            inequality=timespantools.TimespanInequality(
                'expr_1.start <= expr_2.start < expr_1.stop',
                expr_1=timespantools.SingleSourceTimespan(
                    selector=selectortools.SingleSegmentSelector(
                        identifier='red'
                        )
                    )
                )
            )

    Select the last two divisions starting during segment ``'red'``::

        >>> divisions = selectortools.DivisionSelector(inequality=inequality, start_identifier=-2)

    ::

        >>> z(divisions)
        selectortools.DivisionSelector(
            inequality=timespantools.TimespanInequality(
                'expr_1.start <= expr_2.start < expr_1.stop',
                expr_1=timespantools.SingleSourceTimespan(
                    selector=selectortools.SingleSegmentSelector(
                        identifier='red'
                        )
                    )
                ),
            start_identifier=-2
            )

    Division slice selectors are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, inequality=None, start_identifier=None, stop_identifier=None):
        SliceSelector.__init__(self, start_identifier=start_identifier, stop_identifier=stop_identifier)
        InequalitySelector.__init__(self, inequality=inequality)
        self._klass = divisiontools.Division

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def klass(self):
        return self._klass

    @property
    def segment_identifier(self):
        '''Return ``self.inequality.segment_identifier``.
        '''
        return self.inequality.segment_identifier

    ### PUBLIC METHODS ###

    def get_duration(self, score_specification, context_name):
        segment_specification = score_specification.get_segment_specification(self)
        segment_name = segment_specification.segment_name
        segment_index = score_specification.segment_name_to_segment_index(segment_name)
        start, stop = self.identifiers
        start = start or 0
        stop = stop or None
        # FIXME: HARDCODED HACK
        context_name = 'Voice 1'
        segment_division_lists = score_specification.contexts[context_name]['segment_division_lists'] 
        segment_division_list = segment_division_lists[segment_index]
        divisions = segment_division_list[start:stop]
        durations = [durationtools.Duration(division) for division in divisions]
        duration = durationtools.Duration(sum(durations))
        return duration

    # TODO: change name to self.get_start_offset_in_segment
    def get_segment_start_offset(self, score_specification, context_name):
        segment_specification = score_specification.get_segment_specification(self)
        segment_name = segment_specification.segment_name
        segment_index = score_specification.segment_name_to_segment_index(segment_name)
        start, stop = self.identifiers
        start = start or 0
        stop = stop or None
        # FIXME: HARDCODED HACK
        context_name = 'Voice 1'
        segment_division_lists = score_specification.contexts[context_name]['segment_division_lists']
        segment_division_list = segment_division_lists[segment_index]
        durations = [durationtools.Duration(x) for x in segment_division_list]
        durations_before = durations[:start]
        duration_before = sum(durations_before)
        start_offset = durationtools.Offset(duration_before)
        return start_offset

    # TODO: change name to self.get_stop_offset_in_segment
    def get_segment_stop_offset(self, score_specification, context_name):
        segment_specification = score_specification.get_segment_specification(self)
        segment_name = segment_specification.segment_name
        segment_index = score_specification.segment_name_to_segment_index(segment_name)
        start, stop = self.identifiers
        start = start or 0
        stop = stop or None
        # FIXME: HARDCODED HACK
        context_name = 'Voice 1'
        segment_division_lists = score_specification.contexts[context_name]['segment_division_lists']
        segment_division_list = segment_division_lists[segment_index]
        durations = [durationtools.Duration(x) for x in segment_division_list]
        durations_up_through = durations[:stop]
        duration_up_through = sum(durations_up_through)
        stop_offset = durationtools.Offset(duration_up_through)
        return stop_offset

    def set_segment_identifier(self, segment_identifier):
        '''Delegate to ``self.inequality.set_segment_identifier()``.
        '''
        self.inequality.set_segment_identifier(segment_identifier)
