from abjad.tools import schemetools
from abjad.tools.spannertools.Spanner import Spanner


class StaffLinesSpanner(Spanner):
    r'''Abjad staff lines spanner::

        >>> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        >>> spannertools.StaffLinesSpanner(staff[:2], 1)
        StaffLinesSpanner(c'8, d'8)

    ::

        >>> f(staff)
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

    ### INITIALIZER ###

    def __init__(self, components=None, lines=5):
        Spanner.__init__(self, components)
        self.lines = lines

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        new.lines = self.lines

    def _format_after_leaf(self, leaf):
        result = []
        if self._is_my_last_leaf(leaf):
            result.append(r'\stopStaff')
            if isinstance(self.lines, int):
                result.append(r"\revert Staff.StaffSymbol #'line-count")
            else:
                result.append(r"\revert Staff.StaffSymbol #'line-positions")
            result.append(r'\startStaff')
        return result

    def _format_before_leaf(self, leaf):
        result = []
        if self._is_my_first_leaf(leaf):
            result.append(r'\stopStaff')
            if isinstance(self.lines, int):
                result.append(r"\override Staff.StaffSymbol #'line-count = #%s" % \
                    self.lines)
            else:
                result.append(r"\override Staff.StaffSymbol #'line-positions = %s" % \
                    schemetools.SchemeVector(*self.lines).lilypond_format)
            result.append(r'\startStaff')
        return result

    ### READ / WRITE PUBLIC PROPERTIES ###

    @apply
    def lines():
        def fget(self):
            r'''Get staff lines spanner line count::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> spanner = spannertools.StaffLinesSpanner(staff[:2], 1)
                >>> spanner.lines
                1

            Set staff lines spanner line count::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> spanner = spannertools.StaffLinesSpanner(staff[:2], 1)
                >>> spanner.lines = 2
                >>> spanner.lines
                2

            Set integer.
            '''
            return self._lines
        def fset(self, arg):
            if isinstance(arg, int) and 0 < arg:
                self._lines = arg
            elif isinstance(arg, (tuple, list)) \
                and all([isinstance(x, (int, float)) for x in arg]):
                self._lines = tuple(arg)
            else:
                raise ValueError('StaffLinesSpanner requires either an int, '
                    'or a list/tuple of ints and/or floats.')
        return property(**locals())
