from abjad.tools import durationtools
from abjad.tools import sequencetools
from experimental.symbolictimetools.RatioOperator import RatioOperator


class CountRatioOperator(RatioOperator):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *
    
    Select all background measures starting during segment ``'red'`` in ``'Voice 1'``.
    Then partition these measures ``1:1`` by their count.
    Then select part ``0`` of this partition::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    ::

        >>> measures = red_segment.select_background_measures()

    ::

        >>> timespan = symbolictimetools.CountRatioOperator(measures, (1, 1), 0)

    ::

        >>> z(timespan)
        symbolictimetools.CountRatioOperator(
            symbolictimetools.BackgroundMeasureSelector(
                anchor='red'
                ),
            mathtools.Ratio(1, 1),
            0
            )

    All count ratio part symbolic timespan properties are read-only.
    '''

    ### INITIALIZER ###

    def __init__(self, anchor, ratio, part):
        from experimental import symbolictimetools
        assert isinstance(anchor, (symbolictimetools.Selector, str))
        RatioOperator.__init__(self, anchor, ratio, part)

    ### PUBLIC METHODS ###

    def get_offsets(self, score_specification, context_name, start_segment_name=None):
        r'''Evaluate start and stop offsets of symbolic timespan when applied
        to `context_name` in `score_specification`.

        Return offset pair.
        '''
        if start_segment_name is None:
            segment_specification = score_specification.get_start_segment_specification(self)
        else:
            segment_specification = score_specification.get_start_segment_specification(start_segment_name)
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
