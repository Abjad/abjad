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
        >>> inequality = timetools.timespan_2_starts_during_timespan_1(timespan_1=timespan)

    ::

        >>> divisions = selectortools.DivisionSelector(inequality=inequality)

    ::

        >>> z(divisions)
        selectortools.DivisionSelector(
            inequality=timetools.TimespanInequality(
                'timespan_1.start <= timespan_2.start < timespan_1.stop',
                timespan_1=timetools.SingleSourceSymbolicTimespan(
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
            inequality=timetools.TimespanInequality(
                'timespan_1.start <= timespan_2.start < timespan_1.stop',
                timespan_1=timetools.SingleSourceSymbolicTimespan(
                    selector=selectortools.SingleSegmentSelector(
                        identifier='red'
                        )
                    )
                ),
            start_identifier=-2
            )

    Division selectors are immutable.
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

    ### PUBLIC METHODS ###

    def get_score_start_offset(self, score_specification, context_name):
        '''Evaluate score start offset of selector when applied
        to `context_name` in `score_specification`.

        Return offset.
        '''
        segment_specification = score_specification.get_start_segment_specification(self)
        segment_name = segment_specification.segment_name
        segment_index = score_specification.segment_name_to_segment_index(segment_name)
        start, stop = self.identifiers
        start = start or 0
        stop = stop or None

        # FIXME: hardcoded hack
        context_name = 'Voice 1'

        segment_division_lists = score_specification.contexts[context_name]['segment_division_lists']
        segment_division_list = segment_division_lists[segment_index]
        durations = [durationtools.Duration(x) for x in segment_division_list]
        durations_before = durations[:start]
        duration_before = sum(durations_before)
        start_offset = durationtools.Offset(duration_before)
        start_offset = score_specification.segment_offset_to_score_offset(segment_name, start_offset)
        return start_offset

    def get_score_stop_offset(self, score_specification, context_name):
        r'''Evaluate score stop of selector when applied
        to `context_name` in `score_specification`.

        Return offset.
        '''
        segment_specification = score_specification.get_start_segment_specification(self)
        segment_name = segment_specification.segment_name
        segment_index = score_specification.segment_name_to_segment_index(segment_name)
        start, stop = self.identifiers
        start = start or 0
        stop = stop or None
        # FIXME: hardcoded hack
        context_name = 'Voice 1'
        segment_division_lists = score_specification.contexts[context_name]['segment_division_lists']
        segment_division_list = segment_division_lists[segment_index]
        durations = [durationtools.Duration(x) for x in segment_division_list]
        durations_up_through = durations[:stop]
        duration_up_through = sum(durations_up_through)
        stop_offset = durationtools.Offset(duration_up_through)
        stop_offset = score_specification.segment_offset_to_score_offset(segment_name, stop_offset)
        return stop_offset
        
    def set_segment_identifier(self, segment_identifier):
        '''Delegate to ``self.inequality.set_segment_identifier()``.
        '''
        self.inequality.set_segment_identifier(segment_identifier)
