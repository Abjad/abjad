from abjad.tools import abctools
from experimental.timespantools.Timepoint import Timepoint
from experimental.timespantools.Timespan import Timespan


class MixedSourceTimespan(Timespan):
    r'''.. versionadded:: 1.0

    Mixed-source timespan.

        >>> from experimental import *

    SingleSourceTimespan starting at the left edge of the last measure in the segment with name ``'red'``
    and stopping at the right edge of the first measure in the segment with name ``'blue'``::

        >>> segment_selector = selectortools.SegmentItemSelector(index='red')
        >>> inequality = timespantools.expr_starts_during_timespan(timespan=segment_selector.timespan)
        >>> measure_selector = selectortools.BackgroundMeasureItemSelector(inequality=inequality, index=-1)
        >>> start = timespantools.Timepoint(anchor=measure_selector)

    ::

        >>> segment_selector = selectortools.SegmentItemSelector(index='blue')
        >>> inequality = timespantools.expr_starts_during_timespan(timespan=segment_selector.timespan)
        >>> measure_selector = selectortools.BackgroundMeasureItemSelector(inequality=inequality)
        >>> stop = timespantools.Timepoint(anchor=measure_selector, edge=Right)
        
    ::

        >>> timespan = timespantools.MixedSourceTimespan(start=start, stop=stop)

    ::

        >>> z(timespan)
        timespantools.MixedSourceTimespan(
            start=timespantools.Timepoint(
                anchor=selectortools.BackgroundMeasureItemSelector(
                    inequality=timespantools.TimespanInequality(
                        timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                        timespantools.SingleSourceTimespan(
                            selector=selectortools.SegmentItemSelector(
                                index='red'
                                )
                            )
                        ),
                    index=-1
                    )
                ),
            stop=timespantools.Timepoint(
                anchor=selectortools.BackgroundMeasureItemSelector(
                    inequality=timespantools.TimespanInequality(
                        timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                        timespantools.SingleSourceTimespan(
                            selector=selectortools.SegmentItemSelector(
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
        Timespan.__init__(self)
        self._start = start
        self._stop = stop

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if isintance(expr, type(self)):
            if self.start == expr.start:
                if self.stop == expr.stop:
                    return True
        return False

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def is_anchored_to_one_object(self):
        '''True when start anchor equals stop anchor. Otherwise false.

        Return boolean.
        '''
        return self.start.anchor == self.stop.anchor


    def encompasses_one_object_exactly(self):
        '''True when the following five conditions hold:

        1. start anchor equals stop anchor.

        2. start edge is left.

        3. stop edge is right.

        4. start and stop multipliers are both none.
    
        5. start and stop addenda are both none.

        Return boolean.
        '''
        if self.start.anchor == self.stop.anchor:
            if self.start.edge in (None, Left):
                if self.stop.edge == Right:
                    if self.start.multiplier is self.stop.multiplier is None:
                        if self.start.addendum is self.stop.addendum is None:
                            return True
        return False

    @property
    def encompasses_one_segment_exactly(self):
        '''False.
        '''
        return False


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
