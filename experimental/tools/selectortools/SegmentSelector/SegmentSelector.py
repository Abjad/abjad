from experimental.tools.selectortools.Selector import Selector


class SegmentSelector(Selector):
    r'''Segment selector.

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')
        >>> blue_segment = score_specification.append_segment(name='blue')
        >>> green_segment = score_specification.append_segment(name='green')

    Select voice ``1`` segments in score::

        >>> selector = score_specification.interface.select_segments('Voice 1')

    ::

        >>> z(selector)
        selectortools.SegmentSelector(
            voice_name='Voice 1'
            )

    Select the first two voice ``1`` segments in score::

        >>> selector = score_specification.interface.select_segments('Voice 1')[:2]

    ::

        >>> z(selector)
        selectortools.SegmentSelector(
            voice_name='Voice 1',
            callbacks=settingtools.CallbackInventory([
                'result = self.___getitem__(expression, slice(None, 2, None))'
                ])
            )

    Select voice ``1`` segments up to but not including ``'green'``::

        >>> selector = score_specification.interface.select_segments('Voice 1')[:'green']

    ::

        >>> z(selector)
        selectortools.SegmentSelector(
            voice_name='Voice 1',
            callbacks=settingtools.CallbackInventory([
                "result = self.___getitem__(expression, slice(None, 'green', None))"
                ])
            )

    Select voice ``1`` segments up to and including ``'green'``::

        >>> selector = score_specification.interface.select_segments('Voice 1')[:('green', 1)]

    ::

        >>> z(selector)
        selectortools.SegmentSelector(
            voice_name='Voice 1',
            callbacks=settingtools.CallbackInventory([
                "result = self.___getitem__(expression, slice(None, ('green', 1), None))"
                ])
            )

    Select voice ``1`` segment ``'red'``::

        >>> selector = score_specification.interface.select_segments('Voice 1')['red':('red', 1)]

    ::

        >>> z(selector)
        selectortools.SegmentSelector(
            voice_name='Voice 1',
            callbacks=settingtools.CallbackInventory([
                "result = self.___getitem__(expression, slice('red', ('red', 1), None))"
                ])
            )

    Segment selector properties are read only.
    '''

    ### PRIVATE METHODS ###

    def _evaluate(self, score_specification):
        from experimental.tools import settingtools
        start_segment_identifier = self.start_segment_identifier
        segment = score_specification[start_segment_identifier]
        start_offset = segment.start_offset
        result = settingtools.VoicedStartPositionedProduct(
            [segment], voice_name=self.voice_name, start_offset=start_offset)
        result = self._apply_callbacks(result)
        assert isinstance(result, settingtools.VoicedStartPositionedProduct), repr(result)
        return result

    def _make_identifier_expression(self, segment_name, addendum):
        assert isinstance(segment_name, str)
        assert isinstance(addendum, int)
        if 0 < addendum:
            return settingtools.SegmentIdentifierExpression('{!r} + {!r}'.format(segment_name, addendum))
        else:
            return settingtools.SegmentIdentifierExpression('{!r} - {!r}'.format(segment_name, addendum))
