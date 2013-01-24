from experimental.tools.settingtools.SelectExpression import SelectExpression


class SegmentSelectExpression(SelectExpression):
    r'''Segment select expression.

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')
        >>> blue_segment = score_specification.append_segment(name='blue')
        >>> green_segment = score_specification.append_segment(name='green')

    Select voice ``1`` segments in score::

        >>> select_expression = score_specification.interface.select_segments('Voice 1')

    ::

        >>> z(select_expression)
        settingtools.SegmentSelectExpression(
            voice_name='Voice 1'
            )

    Select the first two voice ``1`` segments in score::

        >>> select_expression = score_specification.interface.select_segments('Voice 1')[:2]

    ::

        >>> z(select_expression)
        settingtools.SegmentSelectExpression(
            voice_name='Voice 1',
            callbacks=settingtools.CallbackInventory([
                'result = self.___getitem__(payload_expression, slice(None, 2, None))'
                ])
            )

    Select voice ``1`` segments up to but not including ``'green'``::

        >>> select_expression = score_specification.interface.select_segments('Voice 1')[:'green']

    ::

        >>> z(select_expression)
        settingtools.SegmentSelectExpression(
            voice_name='Voice 1',
            callbacks=settingtools.CallbackInventory([
                "result = self.___getitem__(payload_expression, slice(None, 'green', None))"
                ])
            )

    Select voice ``1`` segments up to and including ``'green'``::

        >>> select_expression = score_specification.interface.select_segments('Voice 1')[:('green', 1)]

    ::

        >>> z(select_expression)
        settingtools.SegmentSelectExpression(
            voice_name='Voice 1',
            callbacks=settingtools.CallbackInventory([
                "result = self.___getitem__(payload_expression, slice(None, ('green', 1), None))"
                ])
            )

    Select voice ``1`` segment ``'red'``::

        >>> select_expression = score_specification.interface.select_segments('Voice 1')['red':('red', 1)]

    ::

        >>> z(select_expression)
        settingtools.SegmentSelectExpression(
            voice_name='Voice 1',
            callbacks=settingtools.CallbackInventory([
                "result = self.___getitem__(payload_expression, slice('red', ('red', 1), None))"
                ])
            )

    Segment select expression properties are read only.
    '''

    ### PRIVATE METHODS ###

    def _evaluate(self):
        from experimental.tools import settingtools
        start_segment_identifier = self.start_segment_identifier
        segment = self.score_specification[start_segment_identifier]
        start_offset = segment.start_offset
        expression = settingtools.StartPositionedPayloadExpression([segment], start_offset=start_offset)
        expression = self._apply_callbacks(expression)
        return expression

    def _make_identifier_expression(self, segment_name, addendum):
        assert isinstance(segment_name, str)
        assert isinstance(addendum, int)
        if 0 < addendum:
            return settingtools.SegmentIdentifierExpression('{!r} + {!r}'.format(segment_name, addendum))
        else:
            return settingtools.SegmentIdentifierExpression('{!r} - {!r}'.format(segment_name, addendum))
