from abjad.tools import durationtools
from abjad.tools import mathtools
from experimental.symbolictimetools.RatioOperator import RatioOperator


class TimeRatioOperator(RatioOperator):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    Select all background measures starting during segment ``'red'`` in ``'Voice 1'``.
    Then partition these measures ``1:1`` by their duration.
    Then select part ``0`` of this partition::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    ::

        >>> measures = red_segment.select_background_measures('Voice 1', )

    ::

        >>> timespan = symbolictimetools.TimeRatioOperator(measures, (1, 1), 0)

    ::

        >>> z(timespan)
        symbolictimetools.TimeRatioOperator(
            symbolictimetools.BackgroundMeasureSelector(
                anchor='red',
                voice_name='Voice 1'
                ),
            mathtools.Ratio(1, 1),
            0
            )

    All time ratio part symbolic timespan properties are read-only.
    '''

    ### INITIALIZER ###

    def __init__(self, anchor, ratio, part):
        RatioOperator.__init__(self, anchor, ratio, part)

    ### PUBLIC METHODS ###

    def get_offsets(self, score_specification, context_name, start_segment_name=None):
        r'''Evaluate start and stop offsets of symbolic timespan when applied
        to `context_name` in `score_specification`.

        Return offset.
        '''
        if isinstance(self.anchor, str):
            start_offset, stop_offset = score_specification.segment_identifier_expression_to_offsets(
                self.anchor)
            anchor_duration = stop_offset - start_offset
        else:
            anchor_duration = self.anchor.get_duration(score_specification, context_name)
        parts = mathtools.divide_number_by_ratio(anchor_duration, self.ratio)
        parts_before = parts[:self.part]
        duration_before = sum(parts_before)
        start_offset = durationtools.Offset(duration_before) 
        segment_specification = score_specification.get_start_segment_specification(self)
        segment_name = segment_specification.segment_name
        start_offset = score_specification.segment_offset_to_score_offset(segment_name, start_offset)
        part = parts[self.part]
        duration = part
        stop_offset = duration_before + duration
        stop_offset = durationtools.Offset(stop_offset)
        stop_offset = score_specification.segment_offset_to_score_offset(segment_name, stop_offset)
        return start_offset, stop_offset
