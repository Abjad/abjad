from experimental import helpertools
from experimental.selectortools.BackgroundElementSliceSelector import BackgroundElementSliceSelector


class SegmentSliceSelector(BackgroundElementSliceSelector):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    Select all segments in score::

        >>> selectortools.SegmentSliceSelector()
        SegmentSliceSelector()

    Select segments from ``3`` forward::

        >>> selectortools.SegmentSliceSelector(start=3)
        SegmentSliceSelector(start=3)

    Select segments up to but not including ``6``::

        >>> selectortools.SegmentSliceSelector(stop=6)
        SegmentSliceSelector(stop=6)

    Select segments up to and including ``6``::

        >>> selectortools.SegmentSliceSelector(stop=6+1)
        SegmentSliceSelector(stop=7)

    Select segments from ``3`` up to but not including ``6``::

        >>> selectortools.SegmentSliceSelector(start=3, stop=6)
        SegmentSliceSelector(start=3, stop=6)

    Select segments from ``3`` up to and including ``6``::

        >>> selectortools.SegmentSliceSelector(start=3, stop=6+1)
        SegmentSliceSelector(start=3, stop=7)

    Select segments from ``'red'`` forward::

        >>> selectortools.SegmentSliceSelector(start='red')
        SegmentSliceSelector(start='red')

    Select segments up to but not including ``'blue'``::

        >>> selectortools.SegmentSliceSelector(stop='blue')
        SegmentSliceSelector(stop='blue')

    Select segments up to and including ``'blue'``::

        >>> selectortools.SegmentSliceSelector(stop=helpertools.SegmentIndexExpression("'blue' + 1"))
        SegmentSliceSelector(stop=SegmentIndexExpression("'blue' + 1"))

    Select segments from ``'red'`` up to but not including ``'blue'``::

        >>> selectortools.SegmentSliceSelector(start='red', stop='blue')
        SegmentSliceSelector(start='red', stop='blue')

    Select segments from ``'red'`` up to and including ``'blue'``::

        >>> selectortools.SegmentSliceSelector(start='red', stop=helpertools.SegmentIndexExpression("'blue' + 1"))
        SegmentSliceSelector(start='red', stop=SegmentIndexExpression("'blue' + 1"))

    Select three segments from ``'red'``::

        >>> selectortools.SegmentSliceSelector(start='red', stop=helpertools.SegmentIndexExpression("'red' + 3"))
        SegmentSliceSelector(start='red', stop=SegmentIndexExpression("'red' + 3"))

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

        >>> selector = selectortools.SegmentSliceSelector(inequality=inequality, start=-2)

    ::

        >>> z(selector)
        selectortools.SegmentSliceSelector(
            inequality=timespantools.TimespanInequality(
                timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                timespantools.SingleSourceTimespan(
                    multiplier=Fraction(1, 3)
                    )
                ),
            start=-2
            )

    All segment slice selector properties are read-only.
    '''

    ### INITIALIZER ###

    def __init__(self, inequality=None, start=None, stop=None):
        from experimental import specificationtools
        BackgroundElementSliceSelector.__init__(self, specificationtools.Segment,
            inequality=inequality, start=start, stop=stop)
