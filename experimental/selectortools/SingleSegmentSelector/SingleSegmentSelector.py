from abjad.tools import durationtools
from experimental import helpertools
from experimental import segmenttools
from experimental.selectortools.InequalitySelector import InequalitySelector


class SingleSegmentSelector(InequalitySelector):
    r'''.. versionadded:: 1.0

    Select segment ``3``::

        >>> from experimental import *

    ::

        >>> selectortools.SingleSegmentSelector(identifier=3)
        SingleSegmentSelector(identifier=3)

    Select segment ``'red'``::

        >>> selectortools.SingleSegmentSelector(identifier='red')
        SingleSegmentSelector(identifier='red')

    Segment selectors are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, inequality=None, identifier=0):
        InequalitySelector.__init__(self, inequality=inequality)
        self._identifier = identifier
        self._klass = segmenttools.Segment

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if isinstance(expr, type(self)):
            if self.klass == expr.klass:
                if self.identifier == expr.identifier:
                    return True
        return False

    ### READ-ONLY PROPERTIES ###

    @property
    def identifier(self):
        return self._identifier

    @property
    def klass(self):
        return self._klass

    @property
    def start_segment_identifier(self):
        return self._identifier

    @property
    def stop_segment_identifier(self):
        return helpertools.SegmentIdentifierExpression('{!r} + 1'.format(self.start_segment_identifier))

    ### PUBLIC METHODS ###

    def get_score_start_offset(self, score_specification, context_name):
        '''Evaluate score start offset of selector when applied
        to `score_specification`.

        Ignore `context_name`.

        Return offset.
        '''
        start_offset, stop_offset = score_specification.segment_identifier_expression_to_offsets(
            self.start_segment_identifier)
        return start_offset

    def get_score_stop_offset(self, score_specification, context_name):
        '''Evaluate score stop offset of selector when applied
        to `score_specification`.

        Ignore `context_name`.

        Return offset.
        '''
        start_offset, stop_offset = score_specification.segment_identifier_expression_to_offsets(
            self.start_segment_identifier)
        return stop_offset

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
