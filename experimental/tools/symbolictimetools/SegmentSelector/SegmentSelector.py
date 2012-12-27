from experimental.tools import helpertools
from experimental.tools import segmenttools
from experimental.tools.symbolictimetools.Selector import Selector


class SegmentSelector(Selector):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental.tools import *

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')
        >>> blue_segment = score_specification.append_segment(name='blue')
        >>> green_segment = score_specification.append_segment(name='green')

    Select all segments in score::

        >>> score_specification.select_segments()
        SegmentSelector()

    Select the first two segments in score::

        >>> segments = score_specification.select_segments()[:2]

    ::

        >>> z(segments)
        symbolictimetools.SegmentSelector(
            modifications=datastructuretools.ObjectInventory([
                'result = self._slice_selected_objects(elements, start_offset, slice(None, 2, None))'
                ])
            )

    Select segments up to but not including ``'green'``::

        >>> segments = score_specification.select_segments()[:'green']

    ::

        >>> z(segments)
        symbolictimetools.SegmentSelector(
            modifications=datastructuretools.ObjectInventory([
                "result = self._slice_selected_objects(elements, start_offset, slice(None, 'green', None))"
                ])
            )

    Select segments up to and including ``'green'``::

        >>> segments = score_specification.select_segments()[:('green', 1)]

    ::

        >>> z(segments)
        symbolictimetools.SegmentSelector(
            modifications=datastructuretools.ObjectInventory([
                "result = self._slice_selected_objects(elements, start_offset, slice(None, ('green', 1), None))"
                ])
            )

    Select segment ``'red'``::

        >>> segments = score_specification.select_segments()['red':('red', 1)]

    ::

        >>> z(segments)
        symbolictimetools.SegmentSelector(
            modifications=datastructuretools.ObjectInventory([
                "result = self._slice_selected_objects(elements, start_offset, slice('red', ('red', 1), None))"
                ])
            )

    Segment selector properties are read only.
    '''

    ### INITIALIZER ###

    def __init__(self, anchor=None, 
        start_identifier=None, stop_identifier=None, time_relation=None, 
        timespan_modifications=None, modifications=None):
        if isinstance(stop_identifier, tuple):
            assert len(stop_identifier) == 2
            stop_identifier = self._make_identifier_expression(*stop_identifier)
        #if start_identifier is not None:
        #    raise Exception(start_identifier)
        #if stop_identifier is not None:
        #    raise Exception(stop_identifier)
        Selector.__init__(self, 
            anchor=anchor,
            start_identifier=start_identifier,
            stop_identifier=stop_identifier,
            time_relation=time_relation,
            timespan_modifications=timespan_modifications,
            modifications=modifications)

    ### PRIVATE METHODS ###

    def _get_offsets(self, score_specification, context_name):
        '''Evaluate start and stop offsets of selector when applied
        to `score_specification`.

        Ignore `context_name`.

        Return offset.
        '''
        offsets = score_specification.segment_identifier_expression_to_offsets(self.start_segment_identifier)
        start_offset, stop_offset = offsets
        offsets = self._apply_timespan_modifications(start_offset, stop_offset)
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
        self._start_identifier = segment_identifier
        self._stop_identifier = self._make_identifier_expression(segment_identifier, 1)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def start_segment_identifier(self):
        '''Temporary hack. Generalize later.
        '''
        return self.start_identifier
