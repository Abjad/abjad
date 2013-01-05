import numbers
from abjad.tools import durationtools
from abjad.tools.abctools import AbjadObject


class BreakPoint(AbjadObject):
    '''An x/y breakpoint:

    ::

        >>> from experimental.tools import breakpointtools

    ::

        >>> breakpointtools.BreakPoint(0.2, 0.5)
        BreakPoint(0.2, 0.5)

    Return `BreakPoint` instance.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_x', '_y')

    ### INITIALIZER ###

    def __init__(self, *args):
        if len(args) == 1:
            if isinstance(args[0], type(self)):
                x, y = args[0].x, args[0].y
            elif isinstance(args[0], (list, tuple)):
                x, y = args
            assert isinstance(x, numbers.Real)
            assert isinstance(y, numbers.Real)
        elif len(args) == 2:
            if isinstance(args[0], numbers.Real):
                x = args[0]
            else:
                x = durationtools.Offset(args[0])
            if isinstance(args[1], numbers.Real):
                y = args[1]
            else:
                y = durationtools.Offset(args[1])
        else:
            raise ValueError
        self._x = x
        self._y = y

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _positional_argument_names(self):
        return ('x', 'y')

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

