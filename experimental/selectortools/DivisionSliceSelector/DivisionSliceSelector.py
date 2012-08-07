from experimental.selectortools.InequalitySelector import InequalitySelector
from experimental.selectortools.SliceSelector import SliceSelector


class DivisionSliceSelector(SliceSelector, InequalitySelector):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    Select all divisions::

        >>> selectortools.DivisionSliceSelector()
        DivisionSliceSelector()

    Select all divisions starting during segment ``'red'``::

        >>> segment = selectortools.SegmentItemSelector(identifier='red')
        >>> timespan = segment.timespan
        >>> inequality = timespantools.expr_starts_during_timespan(timespan=timespan)

    ::

        >>> divisions = selectortools.DivisionSliceSelector(inequality=inequality)

    ::

        >>> z(divisions)
        selectortools.DivisionSliceSelector(
            inequality=timespantools.TimespanInequality(
                timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                timespantools.SingleSourceTimespan(
                    selector=selectortools.SegmentItemSelector(
                        identifier='red'
                        )
                    )
                )
            )

    Select the last two divisions starting during segment ``'red'``::

        >>> divisions = selectortools.DivisionSliceSelector(inequality=inequality, start_identifier=-2)

    ::

        >>> z(divisions)
        selectortools.DivisionSliceSelector(
            inequality=timespantools.TimespanInequality(
                timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                timespantools.SingleSourceTimespan(
                    selector=selectortools.SegmentItemSelector(
                        identifier='red'
                        )
                    )
                ),
            start_identifier=-2
            )

    Division slice selectors are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, inequality=None, start_identifier=None, stop_identifier=None):
        from experimental import divisiontools
        SliceSelector.__init__(self, start_identifier=start_identifier, stop_identifier=stop_identifier)
        InequalitySelector.__init__(self, inequality=inequality)
        self._klass = divisiontools.Division

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def klass(self):
        return self._klass

    @property
    def segment_identifier(self):
        '''Return ``self.inequality.segment_identifier``.
        '''
        return self.inequality.segment_identifier
