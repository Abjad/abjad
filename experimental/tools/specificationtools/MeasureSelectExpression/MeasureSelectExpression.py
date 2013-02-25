from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import measuretools
from abjad.tools import sequencetools
from abjad.tools import timespantools
from experimental.tools.specificationtools.SelectExpression import SelectExpression


class MeasureSelectExpression(SelectExpression):
    r'''Measure select expression.

    Definitions:

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecificationInterface(score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    Example 1. Select voice ``1`` measures that start during score:

    ::

        >>> measures = score_specification.select_measures('Voice 1')

    ::

        >>> z(measures)
        specificationtools.MeasureSelectExpression(
            voice_name='Voice 1'
            )

    Example 2. Select voice ``1`` measures starting during segment ``'red'``:

    ::

        >>> measures = red_segment.select_measures('Voice 1')

    ::

        >>> z(measures)
        specificationtools.MeasureSelectExpression(
            anchor='red',
            voice_name='Voice 1'
            )

    Example 3. Select voice ``1`` measures that start during three contiguous segments:

    ::

        >>> segments = score_specification.select_segments('Voice 1')['red':('red', 3)]
        >>> measures = segments.timespan.select_measures('Voice 1')

    ::

        >>> z(measures)
        specificationtools.MeasureSelectExpression(
            anchor=specificationtools.TimespanExpression(
                anchor=specificationtools.SegmentSelectExpression(
                    voice_name='Voice 1',
                    callbacks=specificationtools.CallbackInventory([
                        "result = self._getitem__(payload_expression, slice('red', ('red', 3), None))"
                        ])
                    )
                ),
            voice_name='Voice 1'
            )

    Measure select expressions are immutable.
    '''

    ### PRIVATE METHODS ###

    def evaluate(self):
        '''Evaluate measure select expression.

        Return none when nonevaluable.

        Return start-positioned division payload expression when evaluable.
        '''
        from experimental.tools import specificationtools
        time_signatures = self.root_specification.time_signatures[:]
        time_signatures = [mathtools.NonreducedFraction(x) for x in time_signatures]
        start_offset = self.root_specification.timespan.start_offset
        expression = specificationtools.StartPositionedDivisionPayloadExpression(
            time_signatures, start_offset=start_offset)
        anchor_timespan = self._evaluate_anchor_timespan()
        time_relation = self._get_time_relation(anchor_timespan)
        expression = expression.get_elements_that_satisfy_time_relation(time_relation)
        expression = self._apply_callbacks(expression)
        return expression

    def evaluate_early(self):
        '''Evaluate measure select expression early.

        Special definition because time signatures can be evaluated
        without knowing the timespan they occupy.

        Return start-positioned division payload expression.
        '''
        from experimental.tools import specificationtools
        time_signatures = self.root_specification.time_signatures[:]
        time_signatures = [mathtools.NonreducedFraction(x) for x in time_signatures]
        expression = specificationtools.IterablePayloadExpression(time_signatures)
        expression = self._apply_callbacks(expression)
        assert isinstance(expression, specificationtools.IterablePayloadExpression), repr(expression)
        return expression
