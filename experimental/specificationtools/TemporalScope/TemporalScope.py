from abjad.tools import componenttools
from abjad.tools import mathtools
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.specificationtools.TemporalCursor import TemporalCursor


class TemporalScope(AbjadObject):
    r'''.. versionadded 1.0

    Finite amount of score time bounded by start and stop temporal cursors.

    (Object-oriented delayed evaluation.)

    Temporal scope objects are essentially fancy pairs.

    Temporal scope objects are designed to share much with time interval objects.

    The purpose of a temporal scope is to highlight a contiguous block of time
    somewhere in some segment and say "everything within my bounds is selected
    for some upcoming operation."

    That is, temporal scopes make up the temporal part of a selection.
    The thing that makes up the vertical part of a selection is a list of
    zero or more context names. 

    So a temporal scope is an important part of a selection.

    Temporal scope objects afford the selection of time relative to score
    objects that do not yet exist.

    Initialize with option start and stop cursors.

    Import ``specificationtools``::

        >>> from experimental import specificationtools

    Select the duration entire score::

        >>> specificationtools.TemporalScope()
        TemporalScope()

    Select the first ``1/8`` of a whole note of time in the score::

        >>> cursor = specificationtools.TemporalCursor(addendum=Fraction(1, 8))

    ::
        >>> specificationtools.TemporalScope(stop=cursor)

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
