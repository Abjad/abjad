from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools import timespantools
from experimental.tools.selectortools.Selector import Selector


class BeatSelector(Selector):
    '''

    Beat selector.

    ::

        >>> from experimental.tools import *

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')
    
    Select voice ``1`` beats that start during score::

        >>> selector = score_specification.interface.select_beats('Voice 1')

    ::

        >>> z(selector)
        selectortools.BeatSelector(
            voice_name='Voice 1'
            )

    Select voice ``1`` beats that start during segment ``'red'``::

        >>> selector = red_segment.select_beats('Voice 1')

    ::

        >>> z(selector)
        selectortools.BeatSelector(
            anchor='red',
            voice_name='Voice 1'
            )

    Beat selectors are to be treated as immutable.
    '''

    ### PRIVATE METHODS ###

    # TODO: remove timespan=None keyword and effect with payload callback instead.
    def _get_timespan_and_payload(self, score_specification, voice_name, timespan=None):
        time_signatures = score_specification.time_signatures
        assert time_signatures
        timespan = timespan or score_specification.timespan
        naive_beats = []
        for time_signature in time_signatures:
            numerator, denominator = time_signature.pair
            naive_beats.extend(numerator * [mathtools.NonreducedFraction(1, denominator)])
        weights = [timespan.start_offset, timespan.duration]
        shards = sequencetools.split_sequence_by_weights(
            naive_beats, weights, cyclic=False, overhang=False)
        result = shards[1]
        start_offset = durationtools.Offset(sum(shards[0]))
        result, start_offset = self._apply_payload_callbacks(result, start_offset)
        result_duration = durationtools.Duration(sum(result))
        stop_offset = start_offset + result_duration
        result_timespan = timespantools.Timespan(start_offset, stop_offset)
        result = [x.pair for x in result]
        return result_timespan, result
