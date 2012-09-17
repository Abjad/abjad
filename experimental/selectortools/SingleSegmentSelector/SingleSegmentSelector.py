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

    def get_duration(self, score_specification, context_name):
        r'''Evaluate duration of selector when applied
        to `context_name` in `score_specification`.

        Return duration.
        '''
        segment_specification = score_specification.get_start_segment_specification(self)
        return segment_specification.duration

    def get_segment_start_offset(self, score_specification, context_name):
        r'''Evaluate segment start offset of selector when applied
        to `context_name` in `score_specification`.

        Return offset ``0``.
        '''
        return durationtools.Offset(0)

    def get_segment_stop_offset(self, score_specification, context_name):
        r'''Evaluate segment stop offset of selector when applied
        to `context_name` in `score_specification`.

        Return offset.
        '''
        segment_specification = score_specification.get_start_segment_specification(self)
        return durationtools.Offset(segment_specification.duration)

    def set_segment_identifier(self, segment_identifier):
        assert isinstance(segment_identifier, (str, int))
        self._identifier = segment_identifier
