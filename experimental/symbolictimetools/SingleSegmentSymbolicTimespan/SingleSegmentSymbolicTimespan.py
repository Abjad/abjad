from abjad.tools import durationtools
from experimental import helpertools
from experimental import segmenttools
from experimental.symbolictimetools.SymbolicTimespan import SymbolicTimespan


class SingleSegmentSymbolicTimespan(SymbolicTimespan):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    Select segment ``3``::

        >>> symbolictimetools.SingleSegmentSymbolicTimespan(identifier=3)
        SingleSegmentSymbolicTimespan(identifier=3)

    Select segment ``'red'``::

        >>> symbolictimetools.SingleSegmentSymbolicTimespan(identifier='red')
        SingleSegmentSymbolicTimespan(identifier='red')

    Segment selectors are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, identifier=0):
        #Selector.__init__(self)
        SymbolicTimespan.__init__(self)
        self._identifier = identifier

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if isinstance(expr, type(self)):
            if self.identifier == expr.identifier:
                return True
        return False

    ### READ-ONLY PROPERTIES ###

    @property
    def identifier(self):
        return self._identifier

    @property
    def start_segment_identifier(self):
        return self._identifier

    ### PUBLIC METHODS ###

    def get_offsets(self, score_specification, context_name, start_segment_name=None):
        '''Evaluate start and stop offsets of selector when applied
        to `score_specification`.

        Ignore `context_name`.

        Return pair.
        '''
        return score_specification.segment_identifier_expression_to_offsets(self.start_segment_identifier)

    def get_selected_objects(self, score_specification, context_name):
        '''Get segments selected when selector is applied
        to `score_specification`.

        Ignore `context_name`.

        Return segment.
        '''
        raise NotImplementedError

    def set_segment_identifier(self, segment_identifier):
        assert isinstance(segment_identifier, (str, int))
        self._identifier = segment_identifier
