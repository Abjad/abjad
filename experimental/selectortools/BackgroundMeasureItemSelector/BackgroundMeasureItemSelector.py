from experimental.selectortools.BackgroundElementItemSelector import BackgroundElementItemSelector


class BackgroundMeasureItemSelector(BackgroundElementItemSelector):
    r'''.. versionadded:: 1.0


    ::

        >>> from experimental import *

    Select measure ``3`` in score::

        >>> selectortools.BackgroundMeasureItemSelector(identifier=3)
        BackgroundMeasureItemSelector(identifier=3)

    Select the last measure to start in the first third of the score::


        >>> timespan = timespantools.SingleSourceTimespan(multiplier=Fraction(1, 3))
        >>> inequality = timespantools.expr_starts_during_timespan(timespan=timespan)

    ::

        >>> selector = selectortools.BackgroundMeasureItemSelector(inequality=inequality, identifier=-1)

    ::
    
        >>> z(selector)
        selectortools.BackgroundMeasureItemSelector(
            inequality=timespantools.TimespanInequality(
                timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                timespantools.SingleSourceTimespan(
                    multiplier=Fraction(1, 3)
                    )
                ),
            identifier=-1
            )

    Select the first measure starting during segment ``'red'``::

        >>> segment_selector = selectortools.SegmentItemSelector(identifier='red')
        >>> inequality = timespantools.expr_starts_during_timespan(timespan=segment_selector.timespan)

    ::

        >>> selector = selectortools.BackgroundMeasureItemSelector(inequality=inequality)

    ::

        >>> z(selector)
        selectortools.BackgroundMeasureItemSelector(
            inequality=timespantools.TimespanInequality(
                timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                timespantools.SingleSourceTimespan(
                    selector=selectortools.SegmentItemSelector(
                        identifier='red'
                        )
                    )
                ),
            identifier=0
            )

    Measure selector properties are read-only.
    '''

    ### INITIALIZER ###

    def __init__(self, inequality=None, identifier=0):
        from abjad.tools import measuretools
        BackgroundElementItemSelector.__init__(
            self, klass=measuretools.Measure, identifier=identifier, inequality=inequality)

    ### PUBLIC METHODS ###

    def context_name(self):
        '''Return none.
        '''
        return

    def context_names(self):
        '''Return empty list.
        '''
        return []
