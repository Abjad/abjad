from experimental.selectortools.BackgroundElementSelector import BackgroundElementSelector


class MeasureSelector(BackgroundElementSelector):
    r'''.. versionadded:: 1.0

    Select measure ``3``::

        >>> from experimental import selectortools

    ::

        >>> selectortools.MeasureSelector(3)
        MeasureSelector(3)

    Select the last measure to start in the first third of the score::

        >>> from experimental import timespantools

    ::

        >>> timepoint = timespantools.Timepoint(multiplier=Fraction(1, 3), edge=Right)
        >>> timespan = timespantools.Timespan(stop=timepoint)
        >>> taxon = timespantools.expr_starts_during_timespan()
        >>> inequality = timespantools.TimespanInequality(taxon, timespan)

    ::

        >>> selector = selectortools.MeasureSelector(-1, inequality=inequality)

    ::
    
        >>> z(selector)
        selectortools.MeasureSelector(
            -1,
            inequality=timespantools.TimespanInequality(
                timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                timespantools.Timespan(
                    stop=timespantools.Timepoint(
                        edge=Right,
                        multiplier=Fraction(1, 3)
                        )
                    )
                )
            )

    Select the first measure starting during segment ``'red'``::

        >>> segment = selectortools.SegmentSelector('red')
        >>> taxon = timespantools.expr_starts_during_timespan()
        >>> inequality = timespantools.TimespanInequality(taxon, segment.timespan)

    ::

        >>> selector = selectortools.MeasureSelector(0, inequality=inequality)

    ::

        >>> z(selector)
        selectortools.MeasureSelector(
            0,
            inequality=timespantools.TimespanInequality(
                timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                timespantools.Timespan(
                    selector=selectortools.SegmentSelector(
                        'red'
                        )
                    )
                )
            )

    Measure selectors are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, index, inequality=None):
        from abjad.tools import measuretools
        BackgroundElementSelector.__init__(self, measuretools.Measure, index, inequality=inequality)

    ### SPECIAL METHODS ###

    def __repr__(self):
        if self.inequality is not None:
            return '{}({!r}, inequality={!r})'.format(self._class_name, self.index, self.inequality)
        else:
            return '{}({!r})'.format(self._class_name, self.index)
