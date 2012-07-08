from experimental.selectortools.BackgroundElementSliceSelector import BackgroundElementSliceSelector


class BackgroundMeasureSliceSelector(BackgroundElementSliceSelector):
    r'''.. versionadded:: 1.0

    Select all measures in score::

        >>> from experimental import selectortools
        >>> from experimental import specificationtools

    ::

        >>> selectortools.BackgroundBackgroundMeasureSliceSelector()
        BackgroundMeasureSliceSelector()

    Select measures from ``3`` forward::

        >>> selectortools.BackgroundBackgroundMeasureSliceSelector(start=3)
        BackgroundMeasureSliceSelector(start=3)

    Select measures up to but not including ``6``::

        >>> selectortools.BackgroundBackgroundMeasureSliceSelector(stop=6)
        BackgroundMeasureSliceSelector(stop=6)

    Select measures from ``3`` up to but not including ``6``::

        >>> selectortools.BackgroundBackgroundMeasureSliceSelector(start=3, stop=6)
        BackgroundMeasureSliceSelector(start=3, stop=6)

    Select all measures starting during segment ``'red'``::

        >>> from experimental import timespantools

    ::

        >>> timespan = selectortools.SegmentSelector(index='red').timespan
        >>> inequality = timespantools.expr_starts_during_timespan(timespan=timespan)

    ::

        >>> selector = selectortools.BackgroundBackgroundMeasureSliceSelector(inequality=inequality)

    ::

        >>> z(selector)
        selectortools.BackgroundBackgroundMeasureSliceSelector(
            inequality=timespantools.TimespanInequality(
                timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                timespantools.Timespan(
                    selector=selectortools.SegmentSelector(
                        index='red'
                        )
                    )
                )
            )

    Select the last two measures during segment ``'red'``::

        >>> selector = selectortools.BackgroundBackgroundMeasureSliceSelector(inequality=inequality, start=-2)

    ::
    
        >>> z(selector)
        selectortools.BackgroundBackgroundMeasureSliceSelector(
            inequality=timespantools.TimespanInequality(
                timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                timespantools.Timespan(
                    selector=selectortools.SegmentSelector(
                        index='red'
                        )
                    )
                ),
            start=-2
            )

    Select all the measures that start during the three contiguous segments starting with ``'red'``::

        >>> expr = specificationtools.Hold("'red' + 3")
        >>> timespan = selectortools.SegmentSliceSelector(start='red', stop=expr).timespan
        >>> inequality = timespantools.expr_starts_during_timespan(timespan)

    ::
    
        >>> selector = selectortools.BackgroundBackgroundMeasureSliceSelector(inequality=inequality)

    ::

        >>> z(selector)
        selectortools.BackgroundBackgroundMeasureSliceSelector(
            inequality=timespantools.TimespanInequality(
                timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                timespantools.Timespan(
                    selector=selectortools.SegmentSliceSelector(
                        start='red',
                        stop=specificationtools.Hold("'red' + 3")
                        )
                    )
                )
            )

    Select the last two measures that start during the three contiguous segments starting with ``'red'``::

        >>> selector = selectortools.BackgroundBackgroundMeasureSliceSelector(inequality=inequality, start=-2)

    ::

        >>> z(selector)
        selectortools.BackgroundBackgroundMeasureSliceSelector(
            inequality=timespantools.TimespanInequality(
                timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                timespantools.Timespan(
                    selector=selectortools.SegmentSliceSelector(
                        start='red',
                        stop=specificationtools.Hold("'red' + 3")
                        )
                    )
                ),
            start=-2
            )

    Measure slice selectors are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, inequality=None, start=None, stop=None):
        from abjad.tools import measuretools
        BackgroundElementSliceSelector.__init__(self, measuretools.Measure,
            inequality=inequality, start=start, stop=stop)
