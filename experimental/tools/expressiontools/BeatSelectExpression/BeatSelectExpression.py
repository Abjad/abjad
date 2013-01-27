from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools import timespantools
from experimental.tools.expressiontools.SelectExpression import SelectExpression


class BeatSelectExpression(SelectExpression):
    '''Beat select expression:

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')
    
    Select voice ``1`` beats that start during score::

        >>> select_expression = score_specification.interface.select_beats('Voice 1')

    ::

        >>> z(select_expression)
        expressiontools.BeatSelectExpression(
            voice_name='Voice 1'
            )

    Select voice ``1`` beats that start during segment ``'red'``::

        >>> select_expression = red_segment.select_beats('Voice 1')

    ::

        >>> z(select_expression)
        expressiontools.BeatSelectExpression(
            anchor='red',
            voice_name='Voice 1'
            )

    Beat select expressions are to be treated as immutable.
    '''

    ### PRIVATE METHODS ###

    def _time_signatures_to_naive_beats(self, time_signatures):
        naive_beats = []
        for time_signature in time_signatures:
            numerator, denominator = time_signature.pair
            naive_beats.extend(numerator * [mathtools.NonreducedFraction(1, denominator)])
        return naive_beats
    
    ### PUBLIC METHODS ###

    def evaluate(self):
        from experimental.tools import expressiontools
        time_signatures = self.score_specification.time_signatures
        timespan = self.score_specification.timespan
        beats = self._time_signatures_to_naive_beats(time_signatures)
        weights = [timespan.start_offset, timespan.duration]
        shards = sequencetools.split_sequence_by_weights(beats, weights, cyclic=False, overhang=False)
        beats = shards[1]
        start_offset = durationtools.Offset(sum(shards[0]))
        expression = expressiontools.StartPositionedDivisionPayloadExpression(payload=beats, start_offset=start_offset)
        expression = self._apply_callbacks(expression)
        expression._voice_name = self.voice_name
        return expression
