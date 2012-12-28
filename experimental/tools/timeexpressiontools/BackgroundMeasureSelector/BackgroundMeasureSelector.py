from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import measuretools
from abjad.tools import sequencetools
from experimental.tools.timeexpressiontools.Selector import Selector


class BackgroundMeasureSelector(Selector):
    r'''

    ::

        >>> from experimental.tools import *

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    Select voice ``1`` measures that start during score::

        >>> selector = score_specification.select_background_measures('Voice 1')

    ::

        >>> z(selector)
        timeexpressiontools.BackgroundMeasureSelector(
            voice_name='Voice 1'
            )

    Select voice ``1`` measures starting during segment ``'red'``::

        >>> selector = red_segment.select_background_measures('Voice 1')

    ::

        >>> z(selector)
        timeexpressiontools.BackgroundMeasureSelector(
            anchor='red',
            voice_name='Voice 1'
            )

    Select voice ``1`` measures that start during three contiguous segments::

        >>> segments = score_specification.select_segments('Voice 1')['red':('red', 3)]
        >>> selector = segments.select_background_measures('Voice 1')

    ::

        >>> z(selector)
        timeexpressiontools.BackgroundMeasureSelector(
            anchor=timeexpressiontools.SegmentSelector(
                voice_name='Voice 1',
                request_modifiers=settingtools.ModifierInventory([
                    "result = self.___getitem__(elements, start_offset, slice('red', ('red', 3), None))"
                    ])
                ),
            voice_name='Voice 1'
            )

    Background measure selectors are immutable.
    '''

    ### PRIVATE METHODS ###

    def _get_offsets(self, score_specification, context_name):
        r'''Evaluate start and stop offsets when selector is applied
        to `score_specification`.

        Ignore `context_name`. 

        Then apply any request_modifiers in selector request_modifiers stack.

        Return pair.
        '''
        segment_specification = score_specification.get_start_segment_specification(self.anchor)
        time_signatures = segment_specification.time_signatures[:]
        time_signatures = [mathtools.NonreducedFraction(x) for x in time_signatures]
        segment_name = segment_specification.segment_name
        start_offset = score_specification.segment_offset_to_score_offset(segment_name, 0)
        time_signatures, start_offset = self._apply_request_modifiers(time_signatures, start_offset)
        durations = [durationtools.Duration(x) for x in time_signatures]
        duration = sum(durations)
        stop_offset = start_offset + duration
        start_offset, stop_offset = self._apply_timespan_modifiers(start_offset, stop_offset)
        return start_offset, stop_offset
