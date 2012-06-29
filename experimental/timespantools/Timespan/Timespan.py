from abjad.tools import componenttools
from abjad.tools import mathtools
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.specificationtools.Timepoint import Timepoint


class Timespan(AbjadObject):
    r'''.. versionadded 1.0

    Finite span of score time bounded by start and stop timepoints.

    (Object-oriented delayed evaluation.)

    Timespan objects have much in common with time interval objects.

    Timespan objects highlight a contiguous blocks of time
    somewhere and say "everything within my bounds is selected
    for some upcoming operation."

    Timespan objects make up the temporal part of a selection.
    (Context name lists make up the vertical part of a selection.)

    Timespan objects afford the selection of time relative to score
    objects that do not yet exist.

    Timespan objects resolve to a rational-valued duration.

    Initialize with optional `start` and `stop` timepoints.

    Select the timespan of the entire score::

        >>> from experimental import specificationtools

    ::

        >>> timespantools.Timespan()
        Timespan()

    Select the timespan of the first third of the score::

        >>> stop = specificationtools.Timepoint(multiplier=Fraction(1, 3), edge=Right)

    ::

        >>> timespantools.Timespan(stop=stop)
        Timespan(stop=Timepoint(edge=Right, multiplier=Fraction(1, 3)))

    Select the timespan of the last third of the score::

        >>> start = specificationtools.Timepoint(edge=Right, multiplier=Fraction(2, 3))

    ::

        >>> timespantools.Timespan(start=start)
        Timespan(start=Timepoint(edge=Right, multiplier=Fraction(2, 3)))

    Select the timespan of the middle third of the score::

        >>> start = specificationtools.Timepoint(edge=Right, multiplier=Fraction(1, 3))
        >>> stop = specificationtools.Timepoint(edge=Right, multiplier=Fraction(2, 3))

    ::

        >>> timespantools.Timespan(start=start, stop=stop)
        Timespan(start=Timepoint(edge=Right, multiplier=Fraction(1, 3)), stop=Timepoint(edge=Right, multiplier=Fraction(2, 3)))

    Select the timespan of the first ``1/8`` of a whole note in score::

        >>> stop = specificationtools.Timepoint(addendum=Fraction(1, 8))

    ::

        >>> timespantools.Timespan(stop=stop)
        Timespan(stop=Timepoint(addendum=Offset(1, 8)))

    Select the timespan of the last ``1/8`` of a whole note in score::

        >>> start = specificationtools.Timepoint(edge=Right, addendum=-Fraction(1, 8))

    ::

        >>> timespantools.Timespan(start=start)
        Timespan(start=Timepoint(edge=Right, addendum=Offset(-1, 8)))

    Select the timespan of the segment with name ``'red'``::

        >>> anchor = specificationtools.ScoreObjectSelector(segment='red')

    ::

        >>> start = specificationtools.Timepoint(anchor=anchor)
        >>> stop = specificationtools.Timepoint(anchor=anchor, edge=Right)

    ::

        >>> timespantools.Timespan(start=start, stop=stop)
        Timespan(ScoreObjectSelector(segment='red'))

    Select the timespan of the first measure in the segment with name ``'red'``::

        >>> anchor = specificationtools.ScoreObjectSelector(segment='red', klass=Measure)

    ::

        >>> start = specificationtools.Timepoint(anchor=anchor)
        >>> stop = specificationtools.Timepoint(anchor=anchor, edge=Right)

    ::

        >>> timespantools.Timespan(start=start, stop=stop)
        Timespan(ScoreObjectSelector(segment='red', klass=measuretools.Measure))

    Select the timespan of the first division in the segment with name ``'red'``::

        >>> anchor = specificationtools.ScoreObjectSelector(segment='red', klass=specificationtools.Division)

    ::

        >>> start = specificationtools.Timepoint(anchor=anchor)
        >>> stop = specificationtools.Timepoint(anchor=anchor, edge=Right)

    ::

        >>> timespantools.Timespan(start=start, stop=stop)
        Timespan(ScoreObjectSelector(segment='red', klass=specificationtools.Division))

    Select the timespan starting at the left edge of the segment with the name ``'red'``
    and stopping at the right edge of the segment with the name ``'blue'``::

        >>> anchor = specificationtools.ScoreObjectSelector(segment='red')
        >>> start = specificationtools.Timepoint(anchor=anchor)

    ::

        >>> anchor = specificationtools.ScoreObjectSelector(segment='blue')
        >>> stop = specificationtools.Timepoint(anchor=anchor, edge=Right)

    ::

        >>> timespantools.Timespan(start=start, stop=stop)
        Timespan(start=Timepoint(anchor=ScoreObjectSelector(segment='red')), stop=Timepoint(anchor=ScoreObjectSelector(segment='blue'), edge=Right))

    Select the timespan starting at the left edge of the last measure in the segment with name ``'red'``
    and stopping at the right edge of the first measure in the segment with name ``'blue'``::

        >>> anchor = specificationtools.ScoreObjectSelector(segment='red', klass=Measure, index=-1)
        >>> start = specificationtools.Timepoint(anchor=anchor)

    ::

        >>> anchor = specificationtools.ScoreObjectSelector(segment='blue', klass=Measure)
        >>> stop = specificationtools.Timepoint(anchor=anchor, edge=Right)

    ::

        >>> timespantools.Timespan(start=start, stop=stop)
        Timespan(start=Timepoint(anchor=ScoreObjectSelector(segment='red', klass=measuretools.Measure, index=-1)), stop=Timepoint(anchor=ScoreObjectSelector(segment='blue', klass=measuretools.Measure), edge=Right))

    Examples below reference the timespan defined immediately above::

        >>> timespan = _

    Timespans are immutable.

    Limitations of the design:

    Timespan objects do not afford the specification of timespans relative to each other.
    So it is not possible to pick out the first third of the timespan starting at the left edge 
    of the last measure in the segment with name ``'red'`` and stopping at the right edge of the
    first measure in the segment with name ``'blue'``.

    When or if we decide we want such functionality we can extend the grammar to allow timespan
    objects to anchor timepoint objects.
    '''

    ### INITIALIZER ###

    def __init__(self, start=None, stop=None):
        assert isinstance(start, (Timepoint, type(None))), repr(start)
        assert isinstance(stop, (Timepoint, type(None))), repr(stop)
        self._start = start
        self._stop = stop

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if isinstance(expr, type(self)):
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
        return '[{} {}]'.format(self.start._one_line_format, self.stop._one_line_format)

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
        if self.start.anchor == self.stop.anchor:
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
        if self.encompasses_one_object_exactly:
            if self.start.anchor.is_segment:
                return True
        return False

    @property
    def start(self):
        '''Timespan start specified by user.

            >>> timespan.start
            Timepoint(anchor=ScoreObjectSelector(segment='red', klass=measuretools.Measure, index=-1))

        Value of none is taken equal to the left edge of score.

        Return timepoint or none.
        '''
        return self._start

    @property
    def stop(self):
        '''Timespan stop specified by user.

            >>> timespan.stop
            Timepoint(anchor=ScoreObjectSelector(segment='blue', klass=measuretools.Measure), edge=Right)

        Value of none is taken equal to the right edge of score.  

        Return timepoint or none.
        '''
        return self._stop
