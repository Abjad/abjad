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

        >>> symbolictimetools.SegmentSelector(stop_identifier=helpertools.SegmentIdentifierExpression("'blue' + 1"))
        SegmentSelector(stop_identifier=SegmentIdentifierExpression("'blue' + 1"))

    Select segments from ``'red'`` up to but not including ``'blue'``::

        >>> symbolictimetools.SegmentSelector(start_identifier='red', stop_identifier='blue')
        SegmentSelector(start_identifier='red', stop_identifier='blue')

    Select segments from ``'red'`` up to and including ``'blue'``::

        >>> symbolictimetools.SegmentSelector(start_identifier='red', stop_identifier=helpertools.SegmentIdentifierExpression("'blue' + 1"))
        SegmentSelector(start_identifier='red', stop_identifier=SegmentIdentifierExpression("'blue' + 1"))

    Select three segments from ``'red'``::

        >>> symbolictimetools.SegmentSelector(start_identifier='red', stop_identifier=helpertools.SegmentIdentifierExpression("'red' + 3"))
        SegmentSelector(start_identifier='red', stop_identifier=SegmentIdentifierExpression("'red' + 3"))

    All segment selector properties are read-only.
    '''

    @property
    def start_segment_identifier(self):
        '''Temporary hack. Generalize later.
        '''
        return self.start_identifier

    ### PUBLIC PROPERTIES ###

    def get_offsets(self, score_specification, context_name, start_segment_name=None):
        '''Evaluate start and stop offsets of selector when applied
        to `score_specification`.

        Ignore `context_name`.

        Return offset.
        '''
        return score_specification.segment_identifier_expression_to_offsets(self.start_segment_identifier)

    def get_selected_objects(self, score_specification, context_name):
        '''Get segments selected when selector is applied
        to `score_specification`.

        Ignore `context_name`.

        Return list of segments.
        '''
        raise NotImplementedError

    def set_segment_identifier(self, segment_identifier):
        # assume selector selects only one segment
        self._start_identifier = segment_identifier
        self._stop_idenetifier = helpertools.SegmentIdentifierExpression('{!r} + 1'.format(segment_identifier))
