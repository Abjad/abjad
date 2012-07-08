from abjad.tools import componenttools
from abjad.tools import mathtools
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.selectortools.Selector import Selector
from experimental.timespantools.Timepoint import Timepoint


class Timespan(AbjadObject):
    r'''.. versionadded 1.0

    Finite timespan bounded by start and stop timepoints.

    Timespan objects highlight a contiguous blocks of time
    somewhere and say "everything within my bounds is selected
    for some upcoming operation."

    Timespan of the entire score::

        >>> from experimental import selectortools
        >>> from experimental import specificationtools
        >>> from experimental import timespantools

    ::

        >>> timespantools.Timespan()
        Timespan()

    Timespan of the first third of the score::

        >>> stop = timespantools.Timepoint(multiplier=Fraction(1, 3), edge=Right)

    ::

        >>> timespantools.Timespan(stop=stop)
        Timespan(stop=Timepoint(edge=Right, multiplier=Fraction(1, 3)))

    Timespan of the last third of the score::

        >>> start = timespantools.Timepoint(edge=Right, multiplier=Fraction(2, 3))

    ::

        >>> timespantools.Timespan(start=start)
        Timespan(start=Timepoint(edge=Right, multiplier=Fraction(2, 3)))

    Timespan of the middle third of the score::

        >>> start = timespantools.Timepoint(edge=Right, multiplier=Fraction(1, 3))
        >>> stop = timespantools.Timepoint(edge=Right, multiplier=Fraction(2, 3))

    ::

        >>> timespantools.Timespan(start=start, stop=stop)
        Timespan(start=Timepoint(edge=Right, multiplier=Fraction(1, 3)), stop=Timepoint(edge=Right, multiplier=Fraction(2, 3)))

    Timespan of the first ``1/8`` of a whole note in score::

        >>> stop = timespantools.Timepoint(addendum=Fraction(1, 8))

    ::

        >>> timespantools.Timespan(stop=stop)
        Timespan(stop=Timepoint(addendum=Offset(1, 8)))

    Timespan of the last ``1/8`` of a whole note in score::

        >>> start = timespantools.Timepoint(edge=Right, addendum=-Fraction(1, 8))

    ::

        >>> timespantools.Timespan(start=start)
        Timespan(start=Timepoint(edge=Right, addendum=Offset(-1, 8)))

    Timespan of the segment with name ``'red'``::

        >>> segment_selector = selectortools.SegmentSelector(index='red')

    ::

        >>> timespantools.Timespan(selector=segment_selector)
        Timespan(selector=SegmentSelector(index='red'))

    Timespan of the first measure that starts during segment ``'red'``::

        >>> inequality = timespantools.expr_starts_during_timespan(timespan=segment_selector.timespan)
        >>> measure_selector = selectortools.BackgroundBackgroundMeasureSelector(inequality=inequality)

    ::

        >>> timespan = timespantools.Timespan(selector=measure_selector)

    ::

        >>> z(timespan)
        timespantools.Timespan(
            selector=selectortools.BackgroundBackgroundMeasureSelector(
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
            )

    Timespan of ``'Voice 1'`` division ``0`` starting during segment ``'red'``::

        >>> division_selector = selectortools.DivisionSelector('Voice 1', inequality=inequality)

    ::

        >>> timespan = timespantools.Timespan(selector=division_selector)

    ::

       >>> z(timespan)
        timespantools.Timespan(
            selector=selectortools.DivisionSelector(
                'Voice 1',
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
            )

    Timespan starting at the left edge of the segment with the name ``'red'``
    and stopping at the right edge of the segment with the name ``'blue'``::

        >>> stop = specificationtools.Hold("'blue' + 1")
        >>> segment_slice_selector = selectortools.SegmentSliceSelector(start='red', stop=stop)

    ::

        >>> timespantools.Timespan(selector=segment_slice_selector)
        Timespan(selector=SegmentSliceSelector(start='red', stop=Hold("'blue' + 1")))

    Timespan starting at the left edge of the last measure in the segment with name ``'red'``
    and stopping at the right edge of the first measure in the segment with name ``'blue'``::

        >>> segment_selector = selectortools.SegmentSelector(index='red')
        >>> inequality = timespantools.expr_starts_during_timespan(timespan=segment_selector.timespan)
        >>> measure_selector = selectortools.BackgroundBackgroundMeasureSelector(inequality=inequality, index=-1)
        >>> start = timespantools.Timepoint(anchor=measure_selector)

    ::

        >>> segment_selector = selectortools.SegmentSelector(index='blue')
        >>> inequality = timespantools.expr_starts_during_timespan(timespan=segment_selector.timespan)
        >>> measure_selector = selectortools.BackgroundBackgroundMeasureSelector(inequality=inequality)
        >>> stop = timespantools.Timepoint(anchor=measure_selector, edge=Right)
        
    ::

        >>> timespan = timespantools.Timespan(start=start, stop=stop)

    ::

        >>> z(timespan)
        timespantools.Timespan(
            start=timespantools.Timepoint(
                anchor=selectortools.BackgroundBackgroundMeasureSelector(
                    inequality=timespantools.TimespanInequality(
                        timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                        timespantools.Timespan(
                            selector=selectortools.SegmentSelector(
                                index='red'
                                )
                            )
                        ),
                    index=-1
                    )
                ),
            stop=timespantools.Timepoint(
                anchor=selectortools.BackgroundBackgroundMeasureSelector(
                    inequality=timespantools.TimespanInequality(
                        timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                        timespantools.Timespan(
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

    Timespans are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, selector=None, start=None, stop=None):
        assert isinstance(selector, (Selector, type(None))), repr(selector)
        assert isinstance(start, (Timepoint, type(None))), repr(start)
        assert isinstance(stop, (Timepoint, type(None))), repr(stop)
        if selector is not None: assert start is None and stop is None
        self._selector = selector
        self._start = start
        self._stop = stop

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if isinstance(expr, type(self)):
            if self.selector == expr.selector:
                if self.start == expr.start:
                    if self.stop == expr.stop:
                        return True
        return False

    def __repr__(self):
        if self.start is not None and self.stop is not None:
            if self.start.anchor == self.stop.anchor:
                if self.start.edge in (Left, None):
                    if self.stop.edge == Right:
                        return '{}({!r})'.format(self._class_name, self.start.anchor)
        return AbjadObject.__repr__(self)

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _one_line_format(self):
        if self.selector is None:
            return '[{} {}]'.format(self.start._one_line_format, self.stop._one_line_format)
        else:
            # note that this is not yet implemented
            return '[{}]'.format(self.selector._one_line_format)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def duration(self):
        '''Rational-valued duration of timespan.
        
        Derived from input values.

        Return rational.
        
        .. note:: not yet implemented.
        '''
        raise NotImplementedError

    @property
    def exact_segment(self):
        '''Return segment name when timespan equals exactly one segment.

        Otherwise return none.
        '''
        pass

    @property
    def is_anchored_to_one_object(self):
        '''True when start anchor equals stop anchor. Otherwise false.

        Return boolean.
        '''
        return self.start.anchor == self.stop.anchor

    @property
    def encompasses_one_object_exactly(self):
        '''True when the following five conditions hold:

        1. start anchor equals stop anchor.

        2. start edge is left.

        3. stop edge is right.

        4. start and stop multipliers are both none.
    
        5. start and stop addenda are both none.

        Return boolean.
        '''
        if self.selector is not None:
            return True
        elif self.start.anchor == self.stop.anchor:
            if self.start.edge in (None, Left):
                if self.stop.edge == Right:
                    if self.start.multiplier is self.stop.multiplier is None:
                        if self.start.addendum is self.stop.addendum is None:
                            return True
        return False

    @property
    def encompasses_one_segment_exactly(self):
        '''True when timespan encompasses one object exactly and when that
        object is a segment. Otherwise false.

        Return boolean.
        '''
        from experimental import selectortools
        if self.encompasses_one_object_exactly:
            if isinstance(self.selector, selectortools.SegmentSelector):
                return True
            elif isinstance(self.start.anchor, selectortools.SegmentSelector):
                return True
        return False

    @property
    def selector(self):
        '''Timespan selector specified by user.

        .. note:: add example.

        Return selector or none.
        '''
        return self._selector

    @property
    def start(self):
        '''Timespan start specified by user.

            >>> z(timespan.start)
            timespantools.Timepoint(
                anchor=selectortools.BackgroundBackgroundMeasureSelector(
                    inequality=timespantools.TimespanInequality(
                        timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                        timespantools.Timespan(
                            selector=selectortools.SegmentSelector(
                                index='red'
                                )
                            )
                        ),
                    index=-1
                    )
                )

        Value of none is interpreted as the left edge of score.

        Return timepoint or none.
        '''
        return self._start

    @property
    def stop(self):
        '''Timespan stop specified by user.

            >>> z(timespan.stop)
            timespantools.Timepoint(
                anchor=selectortools.BackgroundBackgroundMeasureSelector(
                    inequality=timespantools.TimespanInequality(
                        timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                        timespantools.Timespan(
                            selector=selectortools.SegmentSelector(
                                index='blue'
                                )
                            )
                        ),
                    index=0
                    ),
                edge=Right
                )

        Value of none is interpreted as the right edge of score.  

        Return timepoint or none.
        '''
        return self._stop
