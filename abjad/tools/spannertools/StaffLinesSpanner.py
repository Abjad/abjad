# -*- encoding: utf-8 -*-
from abjad.tools import schemetools
from abjad.tools.spannertools.Spanner import Spanner


class StaffLinesSpanner(Spanner):
    r'''A staff lines spanner.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> spanner = spannertools.StaffLinesSpanner(lines=1)
        >>> attach(spanner, staff[:2])
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print format(staff)
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
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_lines',
        )

    ### INITIALIZER ###

    def __init__(
        self, 
        lines=5,
        overrides=None,
        ):
        Spanner.__init__(
            self, 
            overrides=overrides,
            )
        if isinstance(lines, int) and 0 < lines:
            self._lines = lines
        elif isinstance(lines, (tuple, list)) \
            and all(isinstance(x, (int, float)) for x in lines):
            self._lines = tuple(lines)
        else:
            messsage = 'must be integer or a sequence of integers: {!r}.'
            message = message.format(lines)
            raise ValueError(message)
        self._lines = lines

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        new._lines = self.lines

    def _format_after_leaf(self, leaf):
        result = []
        if self._is_my_last_leaf(leaf):
            result.append(r'\stopStaff')
            if isinstance(self.lines, int):
                string = r"\revert Staff.StaffSymbol #'line-count"
                result.append(string)
            else:
                string = r"\revert Staff.StaffSymbol #'line-positions"
                result.append(string)
            result.append(r'\startStaff')
        return result

    def _format_before_leaf(self, leaf):
        result = []
        if self._is_my_first_leaf(leaf):
            result.append(r'\stopStaff')
            if isinstance(self.lines, int):
                string = r"\override Staff.StaffSymbol #'line-count = #{}"
                string = string.format(self.lines)
                result.append(string)
            else:
                string = r"\override Staff.StaffSymbol #'line-positions = {}"
                string = string.format(schemetools.SchemeVector(*self.lines))
                result.append(string)
            result.append(r'\startStaff')
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def lines(self):
        r'''Gets staff lines spanner line count.

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> spanner = spannertools.StaffLinesSpanner(lines=1)
            >>> attach(spanner, staff[:2])
            >>> show(staff) # doctest: +SKIP

        ::

            >>> spanner.lines
            1

        Returns nonnegative integer.
        '''
        return self._lines
