from experimental.selectortools.BackgroundElementSelector import BackgroundElementSelector


class MeasureSelector(BackgroundElementSelector):
    r'''.. versionadded:: 1.0

    Select measure ``3``::

        >>> from experimental import selectortools

    ::

        >>> selectortools.MeasureSelector(index=3)
        MeasureSelector(index=3)

    Select the last measure to start in the first third of the score::

        >>> from experimental import timespantools

    ::

        >>> timepoint = timespantools.Timepoint(multiplier=Fraction(1, 3), edge=Right)
        >>> timespan = timespantools.Timespan(stop=timepoint)
        >>> template = timespantools.expr_starts_during_timespan()
        >>> inequality = timespantools.TimespanInequality(template, timespan)

    ::

        >>> selector = selectortools.MeasureSelector(inequality=inequality, index=-1)

    ::
    
        >>> z(selector)
        selectortools.MeasureSelector(
            inequality=timespantools.TimespanInequality(
                timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                timespantools.Timespan(
                    stop=timespantools.Timepoint(
                        edge=Right,
                        multiplier=Fraction(1, 3)
                        )
                    )
                ),
            index=-1
            )

    Select the first measure starting during segment ``'red'``::

        >>> timespan = selectortools.SegmentSelector(index='red').timespan
        >>> template = timespantools.expr_starts_during_timespan()
        >>> inequality = timespantools.TimespanInequality(template, timespan)

    ::

        >>> selector = selectortools.MeasureSelector(inequality=inequality)

    ::

        >>> z(selector)
        selectortools.MeasureSelector(
            inequality=timespantools.TimespanInequality(
                timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                timespantools.Timespan(
                    selector=selectortools.SegmentSelector(
                        index='red'
                        )
                    )
                ),
            index=0
            )

    Measure selectors are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, inequality=None, index=0):
        from abjad.tools import measuretools
        BackgroundElementSelector.__init__(self, klass=measuretools.Measure, index=index, inequality=inequality)
