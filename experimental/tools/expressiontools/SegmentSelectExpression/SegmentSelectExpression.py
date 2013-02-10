from abjad.tools import durationtools
from experimental.tools.expressiontools.SelectExpression import SelectExpression


class SegmentSelectExpression(SelectExpression):
    r'''Segment select expression.

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecificationInterface(score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')
        >>> blue_segment = score_specification.append_segment(name='blue')
        >>> green_segment = score_specification.append_segment(name='green')

    Select voice ``1`` segments in score::

        >>> select_expression = score_specification.select_segments('Voice 1')

    ::

        >>> z(select_expression)
        expressiontools.SegmentSelectExpression(
            voice_name='Voice 1'
            )

    Select the first two voice ``1`` segments in score::

        >>> select_expression = score_specification.select_segments('Voice 1')[:2]

    ::

        >>> z(select_expression)
        expressiontools.SegmentSelectExpression(
            voice_name='Voice 1',
            callbacks=expressiontools.CallbackInventory([
                'result = self._getitem__(payload_expression, slice(None, 2, None))'
                ])
            )

    Select voice ``1`` segments up to but not including ``'green'``::

        >>> select_expression = score_specification.select_segments('Voice 1')[:'green']

    ::

        >>> z(select_expression)
        expressiontools.SegmentSelectExpression(
            voice_name='Voice 1',
            callbacks=expressiontools.CallbackInventory([
                "result = self._getitem__(payload_expression, slice(None, 'green', None))"
                ])
            )

    Select voice ``1`` segments up to and including ``'green'``::

        >>> select_expression = score_specification.select_segments('Voice 1')[:('green', 1)]

    ::

        >>> z(select_expression)
        expressiontools.SegmentSelectExpression(
            voice_name='Voice 1',
            callbacks=expressiontools.CallbackInventory([
                "result = self._getitem__(payload_expression, slice(None, ('green', 1), None))"
                ])
            )

    Select voice ``1`` segment ``'red'``::

        >>> select_expression = score_specification.select_segments('Voice 1')['red':('red', 1)]

    ::

        >>> z(select_expression)
        expressiontools.SegmentSelectExpression(
            voice_name='Voice 1',
            callbacks=expressiontools.CallbackInventory([
                "result = self._getitem__(payload_expression, slice('red', ('red', 1), None))"
                ])
            )

    Segment select expression properties are read only.
    '''

    ### PRIVATE METHODS ###

    def _make_identifier_expression(self, segment_name, addendum):
        assert isinstance(segment_name, str)
        assert isinstance(addendum, int)
        if 0 < addendum:
            return expressiontools.SegmentIdentifierExpression('{!r} + {!r}'.format(segment_name, addendum))
        else:
            return expressiontools.SegmentIdentifierExpression('{!r} - {!r}'.format(segment_name, addendum))
    
    ### PUBLIC METHODS ###

    def evaluate(self):
        '''Evaluate segment select expression.
        
        Return none when nonevaluable.

        Return start-positioned payload expression when evaluable.
        '''
        from experimental.tools import expressiontools
        segments = self.score_specification.segment_specifications[:]
        start_offset = durationtools.Offset(0)
        expression = expressiontools.StartPositionedPayloadExpression(segments, start_offset=start_offset)
        expression = self._apply_callbacks(expression)
        return expression
