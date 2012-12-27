from abjad.tools import durationtools
from abjad.tools import measuretools
from abjad.tools import sequencetools
from experimental.tools.symbolictimetools.VoiceSelector import VoiceSelector


class BackgroundMeasureSelector(VoiceSelector):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental.tools import *

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    Select voice ``1`` measures that start during score::

        >>> score_specification.select_background_measures('Voice 1')
        BackgroundMeasureSelector(voice_name='Voice 1')

    Select voice ``1`` measures starting during segment ``'red'``::

        >>> red_segment.select_background_measures('Voice 1')
        BackgroundMeasureSelector(anchor='red', voice_name='Voice 1')

    Select all the measures that start during the three contiguous segments 
    starting with ``'red'``::

        >>> segments = score_specification.select_segments()['red':('red', 3)]
        >>> measures = segments.select_background_measures('Voice 1')

    ::

        >>> z(measures)
        symbolictimetools.BackgroundMeasureSelector(
            anchor=symbolictimetools.SegmentSelector(
                request_modifications=datastructuretools.ObjectInventory([
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

        Then apply any request_modifications in selector request_modifications stack.

        Return pair.
        '''
        segment_specification = score_specification.get_start_segment_specification(self.anchor)
        time_signatures = segment_specification.time_signatures[:]
        segment_name = segment_specification.segment_name
        start_offset = score_specification.segment_offset_to_score_offset(segment_name, 0)
        time_signatures, start_offset = self._apply_request_modifications(time_signatures, start_offset)
        durations = [durationtools.Duration(x) for x in time_signatures]
        duration = sum(durations)
        stop_offset = start_offset + duration
        start_offset, stop_offset = self._apply_timespan_modifications(start_offset, stop_offset)
        return start_offset, stop_offset
