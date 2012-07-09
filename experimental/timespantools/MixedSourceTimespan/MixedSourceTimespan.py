from abjad.tools import abctools
from experimental.timespantools.Timepoint import Timepoint
from experimental.timespantools.SingleSourceTimespan import SingleSourceTimespan


class MixedSourceTimespan(SingleSourceTimespan):
    r'''.. versionadded:: 1.0

    Mixed-source timespan.

        >>> from experimental import selectortools
        >>> from experimental import specificationtools
        >>> from experimental import timespantools

    SingleSourceTimespan starting at the left edge of the last measure in the segment with name ``'red'``
    and stopping at the right edge of the first measure in the segment with name ``'blue'``::

        >>> segment_selector = selectortools.SegmentSelector(index='red')
        >>> inequality = timespantools.expr_starts_during_timespan(timespan=segment_selector.timespan)
        >>> measure_selector = selectortools.BackgroundMeasureSelector(inequality=inequality, index=-1)
        >>> start = timespantools.Timepoint(anchor=measure_selector)

    ::

        >>> segment_selector = selectortools.SegmentSelector(index='blue')
        >>> inequality = timespantools.expr_starts_during_timespan(timespan=segment_selector.timespan)
        >>> measure_selector = selectortools.BackgroundMeasureSelector(inequality=inequality)
        >>> stop = timespantools.Timepoint(anchor=measure_selector, edge=Right)
        
    ::

        >>> timespan = timespantools.MixedSourceTimespan(start=start, stop=stop)

    ::

        >>> z(timespan)
        timespantools.MixedSourceTimespan(
            start=timespantools.Timepoint(
                anchor=selectortools.BackgroundMeasureSelector(
                    inequality=timespantools.TimespanInequality(
                        timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                        timespantools.SingleSourceTimespan(
                            selector=selectortools.SegmentSelector(
                                index='red'
                                )
                            )
                        ),
                    index=-1
                    )
                ),
            stop=timespantools.Timepoint(
                anchor=selectortools.BackgroundMeasureSelector(
                    inequality=timespantools.TimespanInequality(
                        timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                        timespantools.SingleSourceTimespan(
                            selector=selectortools.SegmentSelector(
                                index='blue'
                                )
                            )
                        ),
                    index=0
                    ),
                edge=Right
                )
            )

    Mixed-source timespan properties are read-only.
    '''

    ### INITIALIZER ###

    def __init__(self, start=None, stop=None):
        assert isinstance(start, (Timepoint, type(None))), repr(start)
        assert isinstance(stop, (Timepoint, type(None))), repr(stop)
        self._start = start
        self._stop = stop

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def start(self):
        '''SingleSourceTimespan start specified by user.

        Return timepoint or none.
        '''
        return self._start

    @property
    def stop(self):
        '''SingleSourceTimespan stop specified by user.

        Return timepoint or none.
        '''
        return self._stop
