from experimental import helpertools
from experimental import segmenttools
from experimental.selectortools.InequalitySelector import InequalitySelector
from experimental.selectortools.SliceSelector import SliceSelector


class SegmentSelector(SliceSelector, InequalitySelector):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    Select all segments in score::

        >>> selectortools.SegmentSelector()
        SegmentSelector()

    Select segments from ``3`` forward::

        >>> selectortools.SegmentSelector(start_identifier=3)
        SegmentSelector(start_identifier=3)

    Select segments up to but not including ``6``::

        >>> selectortools.SegmentSelector(stop_identifier=6)
        SegmentSelector(stop_identifier=6)

    Select segments up to and including ``6``::

        >>> selectortools.SegmentSelector(stop_identifier=6+1)
        SegmentSelector(stop_identifier=7)

    Select segments from ``3`` up to but not including ``6``::

        >>> selectortools.SegmentSelector(start_identifier=3, stop_identifier=6)
        SegmentSelector(start_identifier=3, stop_identifier=6)

    Select segments from ``3`` up to and including ``6``::

        >>> selectortools.SegmentSelector(start_identifier=3, stop_identifier=6+1)
        SegmentSelector(start_identifier=3, stop_identifier=7)

    Select segments from ``'red'`` forward::

        >>> selectortools.SegmentSelector(start_identifier='red')
        SegmentSelector(start_identifier='red')

    Select segments up to but not including ``'blue'``::

        >>> selectortools.SegmentSelector(stop_identifier='blue')
        SegmentSelector(stop_identifier='blue')

    Select segments up to and including ``'blue'``::

        >>> selectortools.SegmentSelector(stop_identifier=helpertools.SegmentIdentifierExpression("'blue' + 1"))
        SegmentSelector(stop_identifier=SegmentIdentifierExpression("'blue' + 1"))

    Select segments from ``'red'`` up to but not including ``'blue'``::

        >>> selectortools.SegmentSelector(start_identifier='red', stop_identifier='blue')
        SegmentSelector(start_identifier='red', stop_identifier='blue')

    Select segments from ``'red'`` up to and including ``'blue'``::

        >>> selectortools.SegmentSelector(start_identifier='red', stop_identifier=helpertools.SegmentIdentifierExpression("'blue' + 1"))
        SegmentSelector(start_identifier='red', stop_identifier=SegmentIdentifierExpression("'blue' + 1"))

    Select three segments from ``'red'``::

        >>> selectortools.SegmentSelector(start_identifier='red', stop_identifier=helpertools.SegmentIdentifierExpression("'red' + 3"))
        SegmentSelector(start_identifier='red', stop_identifier=SegmentIdentifierExpression("'red' + 3"))

    Select all segments starting during the first third of the score:

        >>> timespan = timetools.SingleSourceSymbolicTimespan(multiplier=Fraction(1, 3))
        >>> inequality = timetools.timespan_2_starts_during_timespan_1(timespan_1=timespan)

    ::

        >>> selector = selectortools.SegmentSelector(inequality=inequality)

    ::

        >>> z(selector)
        selectortools.SegmentSelector(
            inequality=timetools.TimespanInequality(
                'timespan_1.start <= timespan_2.start < timespan_1.stop',
                timespan_1=timetools.SingleSourceSymbolicTimespan(
                    multiplier=Fraction(1, 3)
                    )
                )
            )

    Select the last two segments starting during the first third of the score::

        >>> selector = selectortools.SegmentSelector(inequality=inequality, start_identifier=-2)

    ::

        >>> z(selector)
        selectortools.SegmentSelector(
            inequality=timetools.TimespanInequality(
                'timespan_1.start <= timespan_2.start < timespan_1.stop',
                timespan_1=timetools.SingleSourceSymbolicTimespan(
                    multiplier=Fraction(1, 3)
                    )
                ),
            start_identifier=-2
            )

    All segment slice selector properties are read-only.
    '''

    ### INITIALIZER ###

    def __init__(self, inequality=None, start_identifier=None, stop_identifier=None):
        SliceSelector.__init__(self, start_identifier=start_identifier, stop_identifier=stop_identifier)
        InequalitySelector.__init__(self, inequality=inequality)
        self._klass = segmenttools.Segment

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def klass(self):
        return self._klass

    @property
    def start_segment_identifier(self):
        '''Temporary hack. Generalize later.
        '''
        return self.start_identifier

    @property
    def stop_segment_identifier(self):
        '''Temporary hack. Generalize later.

        Return string or none.
        '''
        return self.stop_identifier

    ### PUBLIC PROPERTIES ###

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
            self.stop_segment_identifier)
        return start_offset

    def get_segment_start_offset(self, score_specification, context_name):
        r'''Evaluate segment start offset of selector when applied
        to `score_specification`.

        Ignore `context_name`.

        .. note:: might be possible to remove altogether.

        Return offset.
        '''
        raise NotImplementedError

    def get_segment_stop_offset(self, score_specification, context_name):
        r'''Evaluate segment stop offset of selector when applied
        to `score_specification`.

        Ignore `context_name`.

        .. note:: might be possible to remove altogether.

        Return offset.
        '''
        raise NotImplementedError
