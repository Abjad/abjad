from abjad.tools import componenttools
from abjad.tools import mathtools
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.specificationtools.PartIndicator import PartIndicator


class HorizontalScope(AbjadObject):
    r'''.. versionadded 1.0

    Horizontal scope objects share much in common with time interval objects.

    Horizontal scope is essentially a fancy pair.

    Horizontal scope comprises a start time and a stop time.

    The purpose of a horizontal scope is to highlight a contiguous block of time
    somewhere in some segment and say "everything within my bounds if selected
    for some upcoming operation."

    That is, horizontal scopes make up the horizontal part of a selection.
    The thing that makes up the vertical part of a selection is a list of
    zero or more context names. 

    So a horizontal scope is an important part of a selection.

    Future design consideration: horizontal scope currently admits on a single criterion.
    This means that we can currently only say things like "start at the start time
    of measure ``0`` in the selection and stop at the stop time of measure ``6``
    in the selection."
    Probably both a `start_criterion` and a `stop_criterion` will be needed to
    generalize correctly. This will allow us to say things like "start at the start time of
    measure ``0`` in the selection and stop at the stop time of note ``20`` in the selection."
    '''

    ### CLASS ATTRIBUTES ###

    criteria_strings = ('divisions', 'measures',)

    ### INITIALIZER ###

    def __init__(self, criterion, part=None, start=None, stop=None):
        assert self.is_valid_criterion(criterion), repr(criterion)
        assert isinstance(part, (PartIndicator, type(None))), repr(part)
        assert isinstance(start, (int, type(None))), repr(start)
        assert isinstance(stop, (int, type(None))), repr(stop)
        assert self.are_concordant_input_values(part, start, stop), repr((start, stop))
        self.criterion = criterion
        self.part = part
        self.start = start
        self.stop = stop

    ### PUBLIC METHODS ###

    def all_are_component_subclasses(self, expr):
        r'''True when `expr` is an iterable and all elements in `expr`
        are subclasses of the Abjad component class. False otherwise.
    
        Abjad components can be used to pick out the `start` and `stop`
        values of a horizontal scope.

        Return boolean.
        '''
        try:
            return all([issubclass(x, componenttools.Component) for x in expr])
        except:
            return False

    def are_concordant_input_values(self, part, start, stop):
        r'''Test to make sure that `part`, `start`, `stop` all make sense together.

        True when `part` is none.
        True when `part`, `start`, `stop` are all nonnone.
        Otherwise false.

        Explanation of this remains to be written.

        Return boolean.
        '''
        if part is not None:
            if start is not None or stop is not None:
                return False
        return True
        
    def is_valid_criterion(self, expr):
        r'''True when `expr` is either none, a component class, or one of the strings
        ``'divisions'`` or ``'measures'``. False otherwise.

        The method indicates those things from which horziontal scope
        `start` and `stop` times can be taken.

        Tthe `start` and `stop` times of a horizontal scope can be taken
        from anything in the score specification that is a measure, a division,
        a tuplet, note, rest, chord or so on. The start and stop times of these
        objects are precisely the things that can be used to draw the two
        'cursors' that together comprise the temporal bounds of a horizontal scope.
        
        Return boolean.
        '''
        if expr is None:
            return True
        elif self.all_are_component_subclasses(expr):
            return True
        elif expr in self.criteria_strings:
            return True
        else:
            raise ValueError('invalid temporal scope criterion: {!r}'.format(expr))
