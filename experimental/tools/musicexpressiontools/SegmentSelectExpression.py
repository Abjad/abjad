# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from experimental.tools.musicexpressiontools.SelectExpression \
    import SelectExpression


class SegmentSelectExpression(SelectExpression):
    r'''Segment select expression.

    Preliminary definitions:

    ::

        >>> score_template = \
        ...     scoretemplatetools.GroupedRhythmicStavesScoreTemplate(
        ...     staff_count=4)
        >>> score_specification = \
        ...     musicexpressiontools.ScoreSpecificationInterface(
        ...     score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')
        >>> blue_segment = score_specification.append_segment(name='blue')
        >>> green_segment = score_specification.append_segment(name='green')

    Example 1. Select voice ``1`` segments in score:

    ::

        >>> select_expression = score_specification.select_segments('Voice 1')

    ::

        >>> print format(select_expression)
        musicexpressiontools.SegmentSelectExpression(
            voice_name='Voice 1',
            callbacks=musicexpressiontools.CallbackInventory([]),
            )

    Example 2. Select the first two voice ``1`` segments in score:

    ::

        >>> select_expression = \
        ...     score_specification.select_segments('Voice 1')[:2]

    ::

        >>> print format(select_expression)
        musicexpressiontools.SegmentSelectExpression(
            voice_name='Voice 1',
            callbacks=musicexpressiontools.CallbackInventory([
                'result = self._getitem__(payload_expression, slice(None, 2, None))',
                ]),
            )

    Example 3. Select voice ``1`` segments up to but not including ``'green'``:

    ::

        >>> select_expression = \
        ...     score_specification.select_segments('Voice 1')[:'green']

    ::

        >>> print format(select_expression)
        musicexpressiontools.SegmentSelectExpression(
            voice_name='Voice 1',
            callbacks=musicexpressiontools.CallbackInventory([
                "result = self._getitem__(payload_expression, slice(None, 'green', None))",
                ]),
            )

    Examle 4. Select voice ``1`` segments up to and including ``'green'``:

    ::

        >>> select_expression = \
        ...     score_specification.select_segments('Voice 1')[:('green', 1)]

    ::

        >>> print format(select_expression)
        musicexpressiontools.SegmentSelectExpression(
            voice_name='Voice 1',
            callbacks=musicexpressiontools.CallbackInventory([
                "result = self._getitem__(payload_expression, slice(None, ('green', 1), None))",
                ]),
            )

    Example 5. Select voice ``1`` segment ``'red'``:

    ::

        >>> select_expression = \
        ...     score_specification.select_segments(
        ...     'Voice 1')['red':('red', 1)]

    ::

        >>> print format(select_expression)
        musicexpressiontools.SegmentSelectExpression(
            voice_name='Voice 1',
            callbacks=musicexpressiontools.CallbackInventory([
                "result = self._getitem__(payload_expression, slice('red', ('red', 1), None))",
                ]),
            )

    Segment select expressions are immutable.
    '''

    ### PRIVATE METHODS ###

    def _make_identifier_expression(self, segment_name, addendum):
        assert isinstance(segment_name, str)
        assert isinstance(addendum, int)
        if 0 < addendum:
            return musicexpressiontools.SegmentIdentifierExpression(
                '{!r} + {!r}'.format(segment_name, addendum))
        else:
            return musicexpressiontools.SegmentIdentifierExpression(
                '{!r} - {!r}'.format(segment_name, addendum))

    ### PUBLIC METHODS ###

    def evaluate(self):
        r'''Evaluate segment select expression.

        Returns none when nonevaluable.

        Returns start-positioned payload expression when evaluable.
        '''
        from experimental.tools import musicexpressiontools
        segments = self.score_specification.segment_specifications[:]
        start_offset = durationtools.Offset(0)
        expression = musicexpressiontools.StartPositionedPayloadExpression(
            segments, start_offset=start_offset)
        expression = self._apply_callbacks(expression)
        return expression
