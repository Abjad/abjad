# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import scoretools
from abjad.tools import sequencetools
from abjad.tools import timespantools
from experimental.tools.musicexpressiontools.SelectExpression \
    import SelectExpression


class MeasureSelectExpression(SelectExpression):
    r'''Measure select expression.

    Definitions:

    ::

        >>> score_template = \
        ...     templatetools.GroupedRhythmicStavesScoreTemplate(
        ...     staff_count=4)
        >>> score_specification = \
        ...     musicexpressiontools.ScoreSpecificationInterface(
        ...     score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    Example 1. Select voice ``1`` measures that start during score:

    ::

        >>> measures = score_specification.select_measures('Voice 1')

    ::

        >>> print(format(measures))
        musicexpressiontools.MeasureSelectExpression(
            voice_name='Voice 1',
            callbacks=musicexpressiontools.CallbackInventory(
                []
                ),
            )

    Example 2. Select voice ``1`` measures starting during segment ``'red'``:

    ::

        >>> measures = red_segment.select_measures('Voice 1')

    ::

        >>> print(format(measures))
        musicexpressiontools.MeasureSelectExpression(
            anchor='red',
            voice_name='Voice 1',
            callbacks=musicexpressiontools.CallbackInventory(
                []
                ),
            )

    Example 3. Select voice ``1`` measures that start during three contiguous
    segments:

    ::

        >>> segments = score_specification.select_segments('Voice 1')['red':('red', 3)]
        >>> measures = segments.timespan.select_measures('Voice 1')

    ::

        >>> print(format(measures))
        musicexpressiontools.MeasureSelectExpression(
            anchor=musicexpressiontools.TimespanExpression(
                anchor=musicexpressiontools.SegmentSelectExpression(
                    voice_name='Voice 1',
                    callbacks=musicexpressiontools.CallbackInventory(
                        [
                            "result = self._getitem__(payload_expression, slice('red', ('red', 3), None))",
                            ]
                        ),
                    ),
                callbacks=musicexpressiontools.CallbackInventory(
                    []
                    ),
                ),
            voice_name='Voice 1',
            callbacks=musicexpressiontools.CallbackInventory(
                []
                ),
            )

    Measure select expressions are immutable.
    '''

    ### PRIVATE METHODS ###

    def evaluate(self):
        r'''Evaluate measure select expression.

        Returns none when nonevaluable.

        Returns start-positioned division payload expression when evaluable.
        '''
        from experimental.tools import musicexpressiontools
        anchor_timespan = self._evaluate_anchor_timespan()
        time_relation = self._get_time_relation(anchor_timespan)
        time_signatures = self.root_specification.time_signatures[:]
        time_signatures = \
            [mathtools.NonreducedFraction(x) for x in time_signatures]
        start_offset = self.root_specification.timespan.start_offset
        expression = \
            musicexpressiontools.StartPositionedDivisionPayloadExpression(
            payload=time_signatures,
            start_offset=start_offset,
            )
        callback_cache = self.score_specification.interpreter.callback_cache
        expression = expression.get_elements_that_satisfy_time_relation(
            time_relation, callback_cache)
        expression = self._apply_callbacks(expression)
        #expression._voice_name = self.voice_name
        return expression

    def evaluate_early(self):
        r'''Evaluate measure select expression early.

        Special definition because time signatures can be evaluated
        without knowing the timespan they occupy.

        Returns start-positioned division payload expression.
        '''
        from experimental.tools import musicexpressiontools
        time_signatures = self.root_specification.time_signatures[:]
        time_signatures = \
            [mathtools.NonreducedFraction(x) for x in time_signatures]
        expression = \
            musicexpressiontools.IterablePayloadExpression(time_signatures)
        expression = self._apply_callbacks(expression)
        assert isinstance(
            expression,
            musicexpressiontools.IterablePayloadExpression)
        return expression
