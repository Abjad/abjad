from abjad.tools import timespantools
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
            payload_callbacks=settingtools.CallbackInventory([
                'result = self.___getitem__(elements, start_offset, slice(None, 2, None))'
                ])
            )

    Select voice ``1`` segments up to but not including ``'green'``::

        >>> selector = score_specification.interface.select_segments('Voice 1')[:'green']

    ::

        >>> z(selector)
        selectortools.SegmentSelector(
            voice_name='Voice 1',
            payload_callbacks=settingtools.CallbackInventory([
                "result = self.___getitem__(elements, start_offset, slice(None, 'green', None))"
                ])
            )

    Select voice ``1`` segments up to and including ``'green'``::

        >>> selector = score_specification.interface.select_segments('Voice 1')[:('green', 1)]

    ::

        >>> z(selector)
        selectortools.SegmentSelector(
            voice_name='Voice 1',
            payload_callbacks=settingtools.CallbackInventory([
                "result = self.___getitem__(elements, start_offset, slice(None, ('green', 1), None))"
                ])
            )

    Select voice ``1`` segment ``'red'``::

        >>> selector = score_specification.interface.select_segments('Voice 1')['red':('red', 1)]

    ::

        >>> z(selector)
        selectortools.SegmentSelector(
            voice_name='Voice 1',
            payload_callbacks=settingtools.CallbackInventory([
                "result = self.___getitem__(elements, start_offset, slice('red', ('red', 1), None))"
                ])
            )

    Segment selector properties are read only.
    '''

    ### PRIVATE METHODS ###

    def _get_payload_and_timespan(self, score_specification, voice_name=None):
        # ignore voice_name input parameter
        voice_name = None
        start_segment_identifier = self.start_segment_identifier
        segment = score_specification[start_segment_identifier]
        segment = self._apply_payload_callbacks(segment)
        return segment, segment.timespan

    def _make_identifier_expression(self, segment_name, addendum):
        assert isinstance(segment_name, str)
        assert isinstance(addendum, int)
        if 0 < addendum:
            return settingtools.SegmentIdentifierExpression('{!r} + {!r}'.format(segment_name, addendum))
        else:
            return settingtools.SegmentIdentifierExpression('{!r} - {!r}'.format(segment_name, addendum))

    ### READ-ONLY PUBLIC PROPERTIES ###

    # TODO: Eventually extend to work without anchor being defined.
    #       Evaluate request payload_callbacks instead.
    @property
    def start_segment_identifier(self):
        '''Temporary hack. Generalize later.
        '''
        assert isinstance(self.anchor, str)
        return self.anchor
