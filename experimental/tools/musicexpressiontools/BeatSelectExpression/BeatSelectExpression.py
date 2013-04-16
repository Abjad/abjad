from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools import timerelationtools
from abjad.tools import timespantools
from experimental.tools.musicexpressiontools.SelectExpression import SelectExpression


class BeatSelectExpression(SelectExpression):
    '''Beat select expression.

    Preparatory definitions:

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    Example 1. Select voice ``1`` beats that start during score:

    ::

        >>> select_expression = score_specification.select_beats('Voice 1')

    ::

        >>> z(select_expression)
        musicexpressiontools.BeatSelectExpression(
            voice_name='Voice 1'
            )

    Example 2. Select voice ``1`` beats that start during segment ``'red'``:

    ::

        >>> select_expression = red_segment.select_beats('Voice 1')

    ::

        >>> z(select_expression)
        musicexpressiontools.BeatSelectExpression(
            anchor='red',
            voice_name='Voice 1'
            )

    Beat select expressions are immutable.
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
        '''Evaluate beat select expression.

        Return none when nonevaluable.

        Return start-positioned division payload expression when evaluable.
        '''
        from experimental.tools import musicexpressiontools
        anchor_timespan = self._evaluate_anchor_timespan()
        time_relation = self._get_time_relation(anchor_timespan) 
        time_signatures = self.root_specification.time_signatures[:]
        beats = self._time_signatures_to_naive_beats(time_signatures)
        start_offset = self.root_specification.timespan.start_offset
        expression = musicexpressiontools.StartPositionedDivisionPayloadExpression(
            payload=beats, start_offset=start_offset)
        callback_cache = self.score_specification.interpreter.callback_cache
        expression = expression.get_elements_that_satisfy_time_relation(time_relation, callback_cache)
        expression = self._apply_callbacks(expression)
        expression._voice_name = self.voice_name
        return expression
