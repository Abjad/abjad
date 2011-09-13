from _StaffLinesSpannerFormatInterface import _StaffLinesSpannerFormatInterface
from abjad.tools.spannertools.Spanner import Spanner


class StaffLinesSpanner(Spanner):
    r'''Abjad staff lines spanner::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        abjad> spannertools.StaffLinesSpanner(staff[:2], 1)
        StaffLinesSpanner(c'8, d'8)

    ::

        abjad> f(staff)
        \new Staff {
            \stopStaff
            \override Staff.StaffSymbol #'line-count = #1
            \startStaff
            c'8
            d'8
            \stopStaff
            \revert Staff.StaffSymbol #'line-count
            \startStaff
            e'8
            f'8
        }

    Staff lines spanner handles changing either the line-count
    or the line-positions property of the StaffSymbol grob,
    as well as automatically stopping and restarting the staff
    so that the change may take place.

    Return staff lines spanner.
    '''

    def __init__(self, components = None, arg = 5):
        Spanner.__init__(self, components)
        if isinstance(arg, int) and 0 < arg:
            self._lines = arg
        elif isinstance(arg, (tuple, list)) \
            and all([isinstance(x, (int, float)) for x in arg]):
            self._lines = arg
        else:
            raise ValueError('StaffLinesSpanner requires either an int, '
                'or a list/tuple of ints and/or floats.')
        self._format = _StaffLinesSpannerFormatInterface(self)

    @apply
    def lines():
        def fget(self):
            r'''Get staff lines spanner line count::

                abjad> staff = Staff("c'8 d'8 e'8 f'8")
                abjad> spanner = spannertools.StaffLinesSpanner(staff[:2], 1)
                abjad> spanner.lines
                1

            Set staff lines spanner line count::

                abjad> staff = Staff("c'8 d'8 e'8 f'8")
                abjad> spanner = spannertools.StaffLinesSpanner(staff[:2], 1)
                abjad> spanner.lines = 2
                abjad> spanner.lines
                2

            Set integer.
            '''
            return self._lines
        def fset(self, arg):
            if isinstance(arg, int) and 0 < arg:
                self._lines = arg
            elif isinstance(arg, (tuple, list)) \
                and all([isinstance(x, (int, float)) for x in arg]):
                self._lines = arg
            else:
                raise ValueError('StaffLinesSpanner requires either an int, '
                    'or a list/tuple of ints and/or floats.')
        return property(**locals())
