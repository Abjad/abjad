from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import measuretools
from abjad.tools import sequencetools
from abjad.tools import timespantools
from experimental.tools.selectortools.Selector import Selector


class MeasureSelector(Selector):
    r'''Measure selector.

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    Select voice ``1`` measures that start during score::

        >>> measures = score_specification.interface.select_measures('Voice 1')

    ::

        >>> z(measures)
        selectortools.MeasureSelector(
            voice_name='Voice 1'
            )

    Select voice ``1`` measures starting during segment ``'red'``::

        >>> measures = red_segment.select_measures('Voice 1')

    ::

        >>> z(measures)
        selectortools.MeasureSelector(
            anchor='red',
            voice_name='Voice 1'
            )

    Select voice ``1`` measures that start during three contiguous segments::

        >>> segments = score_specification.interface.select_segments('Voice 1')['red':('red', 3)]
        >>> measures = segments.timespan.select_measures('Voice 1')

    ::

        >>> z(measures)
        selectortools.MeasureSelector(
            anchor=settingtools.TimespanExpression(
                anchor=selectortools.SegmentSelector(
                    voice_name='Voice 1',
                    callbacks=settingtools.CallbackInventory([
                        "result = self.___getitem__(expression, slice('red', ('red', 3), None))"
                        ])
                    )
                ),
            voice_name='Voice 1'
            )

    Measure selectors are immutable.
    '''

    ### PRIVATE METHODS ###

    def _evaluate(self, score_specification):
        from experimental.tools import settingtools
        start_segment_specification = score_specification.get_start_segment_specification(self)
        time_signatures = start_segment_specification.time_signatures[:]
        time_signatures = [mathtools.NonreducedFraction(x) for x in time_signatures]
        start_offset = start_segment_specification.timespan.start_offset
        result = settingtools.VoicedStartPositionedDivisionProduct(
            time_signatures, voice_name=self.voice_name, start_offset=start_offset)
        result = self._apply_callbacks(result)
        assert isinstance(result, settingtools.VoicedStartPositionedDivisionProduct), repr(result)
        return result

    # special definition because time signatures can be evaluated without knowing the timespan they occupy
    def _evaluate_early(self, score_specification):
        from experimental.tools import settingtools
        start_segment_specification = score_specification.get_start_segment_specification(self)
        time_signatures = start_segment_specification.time_signatures[:]
        time_signatures = [mathtools.NonreducedFraction(x) for x in time_signatures]
        expression = settingtools.PayloadExpression(time_signatures)
        expression = self._apply_callbacks(expression)
        assert isinstance(expression, settingtools.PayloadExpression), repr(expression)
        return expression
