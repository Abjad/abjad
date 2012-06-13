from abjad.tools import componenttools
from abjad.tools import mathtools
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.specificationtools.TemporalCursor import TemporalCursor


class TemporalScope(AbjadObject):
    r'''.. versionadded 1.0

    Finite span of score time bounded by start and stop cursors.

    (Object-oriented delayed evaluation.)

    Temporal scope objects have much in common with time interval objects.

    Temporal scope objects highlight a contiguous blocks of time
    somewhere and say "everything within my bounds is selected
    for some upcoming operation."

    Temporal scope objects make up the temporal part of a selection.
    (Context name lists make up the vertical part of a selection.)

    Temporal scope objects afford the selection of time relative to score
    objects that do not yet exist.

    Temporal scope objects resolve to a rational-valued duration.

    Initialize with optional `start` and `stop` cursors.

    Select the timespan of the entire score::

        >>> from experimental import specificationtools

    ::

        >>> specificationtools.TemporalScope()
        TemporalScope()

    Select the timespan of the first third of the score::

        >>> stop = specificationtools.TemporalCursor(scalar=Fraction(1, 3), edge=right)

    ::

        >>> specificationtools.TemporalScope(stop=stop)
        TemporalScope(stop=TemporalCursor(edge=right, scalar=Fraction(1, 3)))

    Select the timespan of the last third of the score::

        >>> start = specificationtools.TemporalCursor(edge=right, scalar=Fraction(2, 3))

    ::

        >>> specificationtools.TemporalScope(start=start)
        TemporalScope(start=TemporalCursor(edge=right, scalar=Fraction(2, 3)))

    Select the timespan of the middle third of the score::

        >>> start = specificationtools.TemporalCursor(edge=right, scalar=Fraction(1, 3))
        >>> stop = specificationtools.TemporalCursor(edge=right, scalar=Fraction(2, 3))

    ::

        >>> specificationtools.TemporalScope(start=start, stop=stop)
        TemporalScope(start=TemporalCursor(edge=right, scalar=Fraction(1, 3)), stop=TemporalCursor(edge=right, scalar=Fraction(2, 3)))

    Select the timespan of the first ``1/8`` of a whole note in score::

        >>> stop = specificationtools.TemporalCursor(addendum=Fraction(1, 8))

    ::

        >>> specificationtools.TemporalScope(stop=stop)
        TemporalScope(stop=TemporalCursor(addendum=Offset(1, 8)))

    Select the timespan of the last ``1/8`` of a whole note in score::

        >>> start = specificationtools.TemporalCursor(edge=right, addendum=-Fraction(1, 8))

    ::

        >>> specificationtools.TemporalScope(start=start)
        TemporalScope(start=TemporalCursor(edge=right, addendum=Offset(-1, 8)))

    Select the timespan of the segment with name ``'red'``::

        >>> anchor = specificationtools.ScoreObjectIndicator(segment='red')

    ::

        >>> start = specificationtools.TemporalCursor(anchor=anchor)
        >>> stop = specificationtools.TemporalCursor(anchor=anchor, edge=right)

    ::

        >>> specificationtools.TemporalScope(start=start, stop=stop)
        TemporalScope(start=TemporalCursor(anchor=ScoreObjectIndicator(segment='red')), stop=TemporalCursor(anchor=ScoreObjectIndicator(segment='red'), edge=right))

    Select the timespan of the first measure in the segment with name ``'red'``::

        >>> anchor = specificationtools.ScoreObjectIndicator(segment='red', klass=Measure)

    ::

        >>> start = specificationtools.TemporalCursor(anchor=anchor)
        >>> stop = specificationtools.TemporalCursor(anchor=anchor, edge=right)

    ::

        >>> specificationtools.TemporalScope(start=start, stop=stop)
        TemporalScope(start=TemporalCursor(anchor=ScoreObjectIndicator(segment='red', klass=measuretools.Measure)), stop=TemporalCursor(anchor=ScoreObjectIndicator(segment='red', klass=measuretools.Measure), edge=right))

    Select the timespan of the first division in the segment with name ``'red'``::

        >>> anchor = specificationtools.ScoreObjectIndicator(segment='red', klass=specificationtools.Division)

    ::

        >>> start = specificationtools.TemporalCursor(anchor=anchor)
        >>> stop = specificationtools.TemporalCursor(anchor=anchor, edge=right)

    ::

        >>> specificationtools.TemporalScope(start=start, stop=stop)
        TemporalScope(start=TemporalCursor(anchor=ScoreObjectIndicator(segment='red', klass=specificationtools.Division)), stop=TemporalCursor(anchor=ScoreObjectIndicator(segment='red', klass=specificationtools.Division), edge=right))

    Select the timespan starting at the left edge of the segment with the name ``'red'``
    and stopping at the right edge of the segment with the name ``'blue'``::

        >>> anchor = specificationtools.ScoreObjectIndicator(segment='red')
        >>> start = specificationtools.TemporalCursor(anchor=anchor)

    ::

        >>> anchor = specificationtools.ScoreObjectIndicator(segment='blue')
        >>> stop = specificationtools.TemporalCursor(anchor=anchor, edge=right)

    ::

        >>> specificationtools.TemporalScope(start=start, stop=stop)
        TemporalScope(start=TemporalCursor(anchor=ScoreObjectIndicator(segment='red')), stop=TemporalCursor(anchor=ScoreObjectIndicator(segment='blue'), edge=right))

    Select the timespan starting at the left edge of the last measure in the segment with name ``'red'``
    and stopping at the right edge of the first measure in the segment with name ``'blue'``::

        >>> anchor = specificationtools.ScoreObjectIndicator(segment='red', klass=Measure, index=-1)
        >>> start = specificationtools.TemporalCursor(anchor=anchor)

    ::

        >>> anchor = specificationtools.ScoreObjectIndicator(segment='blue', klass=Measure)
        >>> stop = specificationtools.TemporalCursor(anchor=anchor, edge=right)

    ::

        >>> specificationtools.TemporalScope(start=start, stop=stop)
        TemporalScope(start=TemporalCursor(anchor=ScoreObjectIndicator(segment='red', klass=measuretools.Measure, index=-1)), stop=TemporalCursor(anchor=ScoreObjectIndicator(segment='blue', klass=measuretools.Measure), edge=right))

    Examples below reference the temporal scope defined immediately above::

        >>> temporal_scope = _

    Temporal scopes are immutable.

    Limitations of the design:

    Temporal scope objects do not afford the specification of timespans relative to each other.
    So it is not possible to pick out the first third of the timespan starting at the left edge 
    of the last measure in the segment with name ``'red'`` and stopping at the right edge of the
    first measure in the segment with name ``'blue'``.

    When or if we decide we want such functionality we can extend the grammar to allow temporal
    scope objects to anchor temporal cursor objects.
    '''

    ### INITIALIZER ###

    def __init__(self, start=None, stop=None):
        assert isinstance(start, (TemporalCursor, type(None))), repr(start)
        assert isinstance(stop, (TemporalCursor, type(None))), repr(stop)
        self._start = start
        self._stop = stop

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def duration(self):
        '''Rational-valued duration of temporal scope.
        
        Derived from input values.

        Return rational.
        
        .. note:: not yet implemented.
        '''
        raise NotImplementedError

    @property
    def start(self):
        '''Temporal scope start cursor specified by user.

            >>> temporal_scope.start
            TemporalCursor(anchor=ScoreObjectIndicator(segment='red', klass=measuretools.Measure, index=-1))

        Value of none is taken equal to the left edge of score.

        Return temporal cursor or none.
        '''
        return self._start

    @property
    def stop(self):
        '''Temporal scope stop cursor specified by user.

            >>> temporal_scope.stop
            TemporalCursor(anchor=ScoreObjectIndicator(segment='blue', klass=measuretools.Measure), edge=right)

        Value of none is taken equal to the right edge of score.  

        Return temporal cursor or none.
        '''
        return self._stop
