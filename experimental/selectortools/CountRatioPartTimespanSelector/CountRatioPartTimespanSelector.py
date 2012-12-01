from abjad.tools import durationtools
from abjad.tools import sequencetools
from experimental.selectortools.RatioPartTimespanSelector import RatioPartTimespanSelector


class CountRatioPartTimespanSelector(RatioPartTimespanSelector):
    r'''.. versionadded:: 1.0
    
    Partition `selector` by `ratio` of counts. Then select exactly one part.

        >>> from experimental import *

    Select all background measures starting during segment ``'red'`` in ``'Voice 1'``.
    Then partition these measures ``1:1`` by their count.
    Then select part ``0`` of this partition::

        >>> segment_selector = selectortools.SingleSegmentTimespanSelector(identifier='red')
        >>> time_relation = timerelationtools.timespan_2_starts_during_timespan_1(timespan_1=segment_selector.timespan)
        >>> background_measure_selector = selectortools.BackgroundMeasureTimespanSelector(time_relation=time_relation)

    ::

        >>> count_ratio_part_selector = selectortools.CountRatioPartTimespanSelector(
        ... background_measure_selector, (1, 1), 0)

    ::

        >>> z(count_ratio_part_selector)
        selectortools.CountRatioPartTimespanSelector(
            selectortools.BackgroundMeasureTimespanSelector(
                time_relation=timerelationtools.TimespanTimespanTimeRelation(
                    'timespan_1.start <= timespan_2.start < timespan_1.stop',
                    timespan_1=symbolictimetools.SingleSourceSymbolicTimespan(
                        selector=selectortools.SingleSegmentTimespanSelector(
                            identifier='red'
                            )
                        )
                    )
                ),
            mathtools.Ratio(1, 1),
            0
            )

    All count ratio item selector properties are read-only.
    '''

    ### INITIALIZER ###

    def __init__(self, selector, ratio, part):
        from experimental import selectortools
        assert isinstance(selector, selectortools.SliceTimespanSelector)
        RatioPartTimespanSelector.__init__(self, selector, ratio, part)

    ### PUBLIC METHODS ###

    def get_offsets(self, score_specification, context_name):
        r'''Evaluate start and stop offsets of selector when applied
        to `context_name` in `score_specification`.

        Return offset.
        '''
        segment_specification = score_specification.get_start_segment_specification(self)
        segment_name = segment_specification.segment_name
        time_signatures = segment_specification.time_signatures[:]
        parts = sequencetools.partition_sequence_by_ratio_of_lengths(time_signatures, self.ratio)
        parts_before = parts[:self.part]
        durations_before = [
            sum([durationtools.Duration(x) for x in part_before]) for part_before in parts_before]
        duration_before = sum(durations_before)
        start_offset = durationtools.Offset(duration_before)
        start_offset = score_specification.segment_offset_to_score_offset(segment_name, start_offset)
        part = parts[self.part]
        durations = [durationtools.Duration(x) for x in part]
        duration = durationtools.Duration(sum(durations))
        stop_offset = duration_before + duration
        stop_offset = durationtools.Offset(stop_offset)
        stop_offset = score_specification.segment_offset_to_score_offset(segment_name, stop_offset)
        return start_offset, stop_offset
