from experimental import segmenttools
from experimental.selectortools.InequalitySelector import InequalitySelector
from experimental.selectortools.SliceSelector import SliceSelector


class SegmentSliceSelector(SliceSelector, InequalitySelector):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    Select all segments in score::

        >>> selectortools.SegmentSliceSelector()
        SegmentSliceSelector()

    Select segments from ``3`` forward::

        >>> selectortools.SegmentSliceSelector(start_identifier=3)
        SegmentSliceSelector(start_identifier=3)

    Select segments up to but not including ``6``::

        >>> selectortools.SegmentSliceSelector(stop_identifier=6)
        SegmentSliceSelector(stop_identifier=6)

    Select segments up to and including ``6``::

        >>> selectortools.SegmentSliceSelector(stop_identifier=6+1)
        SegmentSliceSelector(stop_identifier=7)

    Select segments from ``3`` up to but not including ``6``::

        >>> selectortools.SegmentSliceSelector(start_identifier=3, stop_identifier=6)
        SegmentSliceSelector(start_identifier=3, stop_identifier=6)

    Select segments from ``3`` up to and including ``6``::

        >>> selectortools.SegmentSliceSelector(start_identifier=3, stop_identifier=6+1)
        SegmentSliceSelector(start_identifier=3, stop_identifier=7)

    Select segments from ``'red'`` forward::

        >>> selectortools.SegmentSliceSelector(start_identifier='red')
        SegmentSliceSelector(start_identifier='red')

    Select segments up to but not including ``'blue'``::

        >>> selectortools.SegmentSliceSelector(stop_identifier='blue')
        SegmentSliceSelector(stop_identifier='blue')

    Select segments up to and including ``'blue'``::

        >>> selectortools.SegmentSliceSelector(stop_identifier=helpertools.SegmentIdentifierExpression("'blue' + 1"))
        SegmentSliceSelector(stop_identifier=SegmentIdentifierExpression("'blue' + 1"))

    Select segments from ``'red'`` up to but not including ``'blue'``::

        >>> selectortools.SegmentSliceSelector(start_identifier='red', stop_identifier='blue')
        SegmentSliceSelector(start_identifier='red', stop_identifier='blue')

    Select segments from ``'red'`` up to and including ``'blue'``::

        >>> selectortools.SegmentSliceSelector(start_identifier='red', stop_identifier=helpertools.SegmentIdentifierExpression("'blue' + 1"))
        SegmentSliceSelector(start_identifier='red', stop_identifier=SegmentIdentifierExpression("'blue' + 1"))

    Select three segments from ``'red'``::

        >>> selectortools.SegmentSliceSelector(start_identifier='red', stop_identifier=helpertools.SegmentIdentifierExpression("'red' + 3"))
        SegmentSliceSelector(start_identifier='red', stop_identifier=SegmentIdentifierExpression("'red' + 3"))

    Select all segments starting during the first third of the score:

        >>> timespan = timespantools.SingleSourceTimespan(multiplier=Fraction(1, 3))
        >>> inequality = timespantools.expr_starts_during_timespan(timespan=timespan)

    ::

        >>> selector = selectortools.SegmentSliceSelector(inequality=inequality)

    ::

        >>> z(selector)
        selectortools.SegmentSliceSelector(
            inequality=timespantools.TimespanInequality(
                timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                timespantools.SingleSourceTimespan(
                    multiplier=Fraction(1, 3)
                    )
                )
            )

    Select the last two segments starting during the first third of the score::

        >>> selector = selectortools.SegmentSliceSelector(inequality=inequality, start_identifier=-2)

    ::

        >>> z(selector)
        selectortools.SegmentSliceSelector(
            inequality=timespantools.TimespanInequality(
                timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                timespantools.SingleSourceTimespan(
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
