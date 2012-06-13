from abjad.tools import componenttools
from abjad.tools import mathtools
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.specificationtools.TemporalCursor import TemporalCursor


class TemporalScope(AbjadObject):
    r'''.. versionadded 1.0

    Finite interval of score time bounded by start and stop cursors.

    (Object-oriented delayed evaluation.)

    Temporal scope objects have much in common with time interval objects.

    The purpose of a temporal scope is to highlight a contiguous block of time
    somewhere and say "everything within my bounds is selected
    for some upcoming operation."

    Temporal scope objects make up the temporal part of a selection.
    (The thing that makes up the vertical part of a selection is a list of
    zero or more context names.)

    Temporal scope objects afford the selection of time relative to score
    objects that do not yet exist.

    Initialize with optional start and stop cursors.

    Import ``specificationtools``::

        >>> from experimental import specificationtools

    Select the duration entire score::

        >>> specificationtools.TemporalScope()
        TemporalScope()

    Select the first ``1/8`` of a whole note's duration in the score::

        >>> cursor = specificationtools.TemporalCursor(addendum=Fraction(1, 8))

    ::

        >>> specificationtools.TemporalScope(stop=cursor)
        TemporalScope(stop=TemporalCursor(addendum=Offset(1, 8)))

    Select the last ``1/8`` of a whole note's duration in the score::

        >>> cursor = specificationtools.TemporalCursor(edge=right, addendum=-Fraction(1, 8))

    ::

        >>> specificationtools.TemporalScope(start=cursor)
        TemporalScope(start=TemporalCursor(edge=right, addendum=Offset(-1, 8)))

    Select the first third of the score::

        >>> cursor = specificationtools.TemporalCursor(scalar=Fraction(1, 3), edge=right)

    ::

        >>> specificationtools.TemporalScope(stop=cursor)
        TemporalScope(stop=TemporalCursor(edge=right, scalar=Fraction(1, 3)))

    Select the last third of the score::

        >>> cursor = specificationtools.TemporalCursor(edge=right, scalar=Fraction(2, 3))

    ::

        >>> specificationtools.TemporalScope(start=cursor)
        TemporalScope(start=TemporalCursor(edge=right, scalar=Fraction(2, 3)))
    
    Examples below reference the temporal scope defined immediately above::

        >>> temporal_scope = _

    Temporal scopes are immutable.

    .. note:: many more examples coming soon.
    '''

    ### INITIALIZER ###

    def __init__(self, start=None, stop=None):
        assert isinstance(start, (TemporalCursor, type(None))), repr(start)
        assert isinstance(stop, (TemporalCursor, type(None))), repr(stop)
        self._start = start
        self._stop = stop

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def start(self):
        '''Temporal scope start cursor specified by user.
        '''
        return self._start

    @property
    def stop(self):
        '''Temporal scope stop cursor specified by user.
        '''
        return self._stop

    ### PUBLIC METHODS ###

#    def all_are_component_subclasses(self, expr):
#        r'''True when `expr` is an iterable and all elements in `expr`
#        are subclasses of the Abjad component class. False otherwise.
#    
#        Abjad components can be used to pick out the `start` and `stop`
#        values of a temporal scope.
#
#        Return boolean.
#        '''
#        try:
#            return all([issubclass(x, componenttools.Component) for x in expr])
#        except:
#            return False

#    def are_concordant_input_values(self, part, start, stop):
#        r'''Test to make sure that `part`, `start`, `stop` all make sense together.
#
#        True when `part` is none.
#        True when `part`, `start`, `stop` are all nonnone.
#        Otherwise false.
#
#        Explanation of this remains to be written.
#
#        Return boolean.
#        '''
#        if part is not None:
#            if start is not None or stop is not None:
#                return False
#        return True
        
#    def is_valid_criterion(self, expr):
#        r'''True when `expr` is either none, a component class, or one of the strings
#        ``'divisions'`` or ``'measures'``. False otherwise.
#
#        The method indicates those things from which horziontal scope
#        `start` and `stop` times can be taken.
#
#        Tthe `start` and `stop` times of a temporal scope can be taken
#        from anything in the score specification that is a measure, a division,
#        a tuplet, note, rest, chord or so on. The start and stop times of these
#        objects are precisely the things that can be used to draw the two
#        'cursors' that together comprise the temporal bounds of a temporal scope.
#        
#        Return boolean.
#        '''
#        if expr is None:
#            return True
#        elif self.all_are_component_subclasses(expr):
#            return True
#        elif expr in self.criteria_strings:
#            return True
#        else:
#            raise ValueError('invalid temporal scope criterion: {!r}'.format(expr))
