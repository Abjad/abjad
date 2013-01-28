from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import measuretools
from abjad.tools import sequencetools
from abjad.tools import timespantools
from experimental.tools.expressiontools.SelectExpression import SelectExpression


class MeasureSelectExpression(SelectExpression):
    r'''Measure select expression.

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = expressiontools.ScoreSpecificationInterface(score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    Select voice ``1`` measures that start during score::

        >>> measures = score_specification.select_measures('Voice 1')

    ::

        >>> z(measures)
        expressiontools.MeasureSelectExpression(
            voice_name='Voice 1'
            )

    Select voice ``1`` measures starting during segment ``'red'``::

        >>> measures = red_segment.select_measures('Voice 1')

    ::

        >>> z(measures)
        expressiontools.MeasureSelectExpression(
            anchor='red',
            voice_name='Voice 1'
            )

    Select voice ``1`` measures that start during three contiguous segments::

        >>> segments = score_specification.select_segments('Voice 1')['red':('red', 3)]
        >>> measures = segments.timespan.select_measures('Voice 1')

    ::

        >>> z(measures)
        expressiontools.MeasureSelectExpression(
            anchor=expressiontools.TimespanExpression(
                anchor=expressiontools.SegmentSelectExpression(
                    voice_name='Voice 1',
                    callbacks=expressiontools.CallbackInventory([
                        "result = self.___getitem__(payload_expression, slice('red', ('red', 3), None))"
                        ])
                    )
                ),
            voice_name='Voice 1'
            )

    Measure select expressions are immutable.
    '''

    ### PRIVATE METHODS ###

    def evaluate(self):
        from experimental.tools import expressiontools
        start_segment_specification = self.score_specification.get_start_segment_specification(self)
        time_signatures = start_segment_specification.time_signatures[:]
        time_signatures = [mathtools.NonreducedFraction(x) for x in time_signatures]
        start_offset = start_segment_specification.timespan.start_offset
        expression = expressiontools.StartPositionedDivisionPayloadExpression(time_signatures, start_offset=start_offset)
        expression = self._apply_callbacks(expression)
        return expression

    # special definition because time signatures can be evaluated without knowing the timespan they occupy
    def evaluate_early(self):
        from experimental.tools import expressiontools
        start_segment_specification = self.score_specification.get_start_segment_specification(self)
        time_signatures = start_segment_specification.time_signatures[:]
        time_signatures = [mathtools.NonreducedFraction(x) for x in time_signatures]
        expression = expressiontools.PayloadExpression(time_signatures)
        expression = self._apply_callbacks(expression)
        assert isinstance(expression, expressiontools.PayloadExpression), repr(expression)
        return expression
