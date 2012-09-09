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

        >>> timespan = timespantools.SingleSourceTimespan(multiplier=Fraction(1, 3))
        >>> inequality = timespaninequalitytools.timespan_2_starts_during_timespan_1(expr_1=timespan)

    ::

        >>> selector = selectortools.SegmentSelector(inequality=inequality)

    ::

        >>> z(selector)
        selectortools.SegmentSelector(
            inequality=timespaninequalitytools.TimespanInequality(
                'expr_1.start <= expr_2.start < expr_1.stop',
                expr_1=timespantools.SingleSourceTimespan(
                    multiplier=Fraction(1, 3)
                    )
                )
            )

    Select the last two segments starting during the first third of the score::

        >>> selector = selectortools.SegmentSelector(inequality=inequality, start_identifier=-2)

    ::

        >>> z(selector)
        selectortools.SegmentSelector(
            inequality=timespaninequalitytools.TimespanInequality(
                'expr_1.start <= expr_2.start < expr_1.stop',
                expr_1=timespantools.SingleSourceTimespan(
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
    def segment_identifier(self):
        '''Temporary hack. Generalize later.
        '''
        return self.start_identifier
