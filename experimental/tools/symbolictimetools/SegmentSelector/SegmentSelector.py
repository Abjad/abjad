from experimental.tools import helpertools
from experimental.tools import segmenttools
from experimental.tools.symbolictimetools.Selector import Selector


class SegmentSelector(Selector):
    r'''

    ::

        >>> from experimental.tools import *

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')
        >>> blue_segment = score_specification.append_segment(name='blue')
        >>> green_segment = score_specification.append_segment(name='green')

    Select voice ``1`` segments in score::

        >>> selector = score_specification.select_segments('Voice 1')

    ::

        >>> z(selector)
        symbolictimetools.SegmentSelector(
            voice_name='Voice 1'
            )

    Select the first two voice ``1`` segments in score::

        >>> selector = score_specification.select_segments('Voice 1')[:2]

    ::

        >>> z(selector)
        symbolictimetools.SegmentSelector(
            voice_name='Voice 1',
            request_modifiers=settingtools.ModifierInventory([
                'result = self.___getitem__(elements, start_offset, slice(None, 2, None))'
                ])
            )

    Select voice ``1`` segments up to but not including ``'green'``::

        >>> selector = score_specification.select_segments('Voice 1')[:'green']

    ::

        >>> z(selector)
        symbolictimetools.SegmentSelector(
            voice_name='Voice 1',
            request_modifiers=settingtools.ModifierInventory([
                "result = self.___getitem__(elements, start_offset, slice(None, 'green', None))"
                ])
            )

    Select voice ``1`` segments up to and including ``'green'``::

        >>> selector = score_specification.select_segments('Voice 1')[:('green', 1)]

    ::

        >>> z(selector)
        symbolictimetools.SegmentSelector(
            voice_name='Voice 1',
            request_modifiers=settingtools.ModifierInventory([
                "result = self.___getitem__(elements, start_offset, slice(None, ('green', 1), None))"
                ])
            )

    Select voice ``1`` segment ``'red'``::

        >>> selector = score_specification.select_segments('Voice 1')['red':('red', 1)]

    ::

        >>> z(selector)
        symbolictimetools.SegmentSelector(
            voice_name='Voice 1',
            request_modifiers=settingtools.ModifierInventory([
                "result = self.___getitem__(elements, start_offset, slice('red', ('red', 1), None))"
                ])
            )

    Segment selector properties are read only.
    '''

    ### PRIVATE METHODS ###

    def _get_offsets(self, score_specification, context_name):
        '''Evaluate start and stop offsets of selector when applied
        to `score_specification`.

        Ignore `context_name`.

        Return offset.
        '''
        offsets = score_specification.segment_identifier_expression_to_offsets(self.start_segment_identifier)
        start_offset, stop_offset = offsets
        offsets = self._apply_timespan_modifiers(start_offset, stop_offset)
        return offsets

    def _make_identifier_expression(self, segment_name, addendum):
        assert isinstance(segment_name, str)
        assert isinstance(addendum, int)
        if 0 < addendum:
            return helpertools.SegmentIdentifierExpression('{!r} + {!r}'.format(segment_name, addendum))
        else:
            return helpertools.SegmentIdentifierExpression('{!r} - {!r}'.format(segment_name, addendum))

    # TODO: eventually extend method to work with segment selectors that select more than one segment
    def _set_start_segment_identifier(self, segment_identifier):
        assert isinstance(segment_identifier, str)
        self._anchor = segment_identifier

    ### READ-ONLY PUBLIC PROPERTIES ###

    # TODO: Eventually extend to work without anchor being defined.
    #       Evaluate request request_modifiers instead.
    @property
    def start_segment_identifier(self):
        '''Temporary hack. Generalize later.
        '''
        assert isinstance(self.anchor, str)
        return self.anchor
