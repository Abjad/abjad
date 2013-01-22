from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools import timespantools
from experimental.tools.selectortools.Selector import Selector


class BeatSelector(Selector):
    '''Beat selector:

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

    def _evaluate(self, score_specification):
        from experimental.tools import settingtools
        time_signatures = score_specification.time_signatures
        assert time_signatures
        timespan = score_specification.timespan
        naive_beats = []
        for time_signature in time_signatures:
            numerator, denominator = time_signature.pair
            naive_beats.extend(numerator * [mathtools.NonreducedFraction(1, denominator)])
        weights = [timespan.start_offset, timespan.duration]
        shards = sequencetools.split_sequence_by_weights(
            naive_beats, weights, cyclic=False, overhang=False)
        result = shards[1]
        start_offset = durationtools.Offset(sum(shards[0]))
        result = settingtools.StartPositionedBeatProduct(
            result, voice_name=self.voice_name, start_offset=start_offset)
        result = self._apply_callbacks(result)
        assert isinstance(result, settingtools.StartPositionedBeatProduct), repr(result)
        return result
