from experimental import helpertools
from experimental import segmenttools
from experimental.symbolictimetools.Selector import Selector


class SegmentSelector(Selector):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    Select all segments in score::

        >>> symbolictimetools.SegmentSelector()
        SegmentSelector()

    Select segments from ``3`` forward::

        >>> symbolictimetools.SegmentSelector(start_identifier=3)
        SegmentSelector(start_identifier=3)

    Select segments up to but not including ``6``::

        >>> symbolictimetools.SegmentSelector(stop_identifier=6)
        SegmentSelector(stop_identifier=6)

    Select segments up to and including ``6``::

        >>> symbolictimetools.SegmentSelector(stop_identifier=6+1)
        SegmentSelector(stop_identifier=7)

    Select segments from ``3`` up to but not including ``6``::

        >>> symbolictimetools.SegmentSelector(start_identifier=3, stop_identifier=6)
        SegmentSelector(start_identifier=3, stop_identifier=6)

    Select segments from ``3`` up to and including ``6``::

        >>> symbolictimetools.SegmentSelector(start_identifier=3, stop_identifier=6+1)
        SegmentSelector(start_identifier=3, stop_identifier=7)

    Select segments from ``'red'`` forward::

        >>> symbolictimetools.SegmentSelector(start_identifier='red')
        SegmentSelector(start_identifier='red')

    Select segments up to but not including ``'blue'``::

        >>> symbolictimetools.SegmentSelector(stop_identifier='blue')
        SegmentSelector(stop_identifier='blue')

    Select segments up to and including ``'blue'``::

        >>> symbolictimetools.SegmentSelector(stop_identifier=('blue', 1))
        SegmentSelector(stop_identifier=SegmentIdentifierExpression("'blue' + 1"))

    Select segments from ``'red'`` up to but not including ``'blue'``::

        >>> symbolictimetools.SegmentSelector(start_identifier='red', stop_identifier='blue')
        SegmentSelector(start_identifier='red', stop_identifier='blue')

    Select segments from ``'red'`` up to and including ``'blue'``::

        >>> symbolictimetools.SegmentSelector(start_identifier='red', stop_identifier=('blue', 1))
        SegmentSelector(start_identifier='red', stop_identifier=SegmentIdentifierExpression("'blue' + 1"))

    Select three segments from ``'red'``::

        >>> symbolictimetools.SegmentSelector(start_identifier='red', stop_identifier=('red', 3))
        SegmentSelector(start_identifier='red', stop_identifier=SegmentIdentifierExpression("'red' + 3"))

    All segment selector properties are read-only.
    '''

    ### INITIALIZER ###

    def __init__(self, anchor=None, 
        start_identifier=None, stop_identifier=None, time_relation=None, 
        timespan_modifications=None, selector_modifications=None):
        if isinstance(stop_identifier, tuple):
            assert len(stop_identifier) == 2
            stop_identifier = self._make_identifier_expression(*stop_identifier)
        Selector.__init__(self, 
            anchor=anchor,
            start_identifier=start_identifier,
            stop_identifier=stop_identifier,
            voice_name=None,
            time_relation=time_relation,
            timespan_modifications=timespan_modifications,
            selector_modifications=selector_modifications)

    ### PRIVATE METHODS ###

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

    ### PUBLIC METHODS ###

    def get_offsets(self, score_specification, context_name):
        '''Evaluate start and stop offsets of selector when applied
        to `score_specification`.

        Ignore `context_name`.

        Return offset.
        '''
        offsets = score_specification.segment_identifier_expression_to_offsets(self.start_segment_identifier)
        start_offset, stop_offset = offsets
        offsets = self._apply_timespan_modifications(start_offset, stop_offset)
        return offsets
