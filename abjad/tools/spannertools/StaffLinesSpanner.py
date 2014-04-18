# -*- encoding: utf-8 -*-
from abjad.tools import schemetools
from abjad.tools.spannertools.Spanner import Spanner


class StaffLinesSpanner(Spanner):
    r'''A staff lines spanner.

    ..  container:: example

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> spanner = spannertools.StaffLinesSpanner(lines=1)
            >>> attach(spanner, staff[1:3])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new Staff {
                c'8
                \stopStaff
                \once \override Staff.StaffSymbol.line-count = 1
                \startStaff
                d'8
                e'8
                \stopStaff
                \startStaff
                f'8
            }

    Stops and restarts staff on first leaf in spanner.

    Overrides ``line-count`` attribute of LilyPond ``Staff.StaffSymbol`` grob
    on first leaf in spanner.

    Stops and restarts staff on last leaf in spanner.

    Reverts ``line-count`` attribute of LilyPond ``Staff.StaffSymbol`` grob on
    last leaf in spanner.
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
            message = 'must be integer or a sequence of integers: {!r}.'
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
            result.append(r'\startStaff')
        return result

    def _format_before_leaf(self, leaf):
        from abjad.tools import lilypondnametools
        result = []
        if self._is_my_first_leaf(leaf):
            result.append(r'\stopStaff')
            if isinstance(self.lines, int):
                override = lilypondnametools.LilyPondGrobOverride(
                    context_name='Staff',
                    grob_name='StaffSymbol',
                    is_once=True,
                    property_path='line-count',
                    value=self.lines,
                    )
                string = '\n'.join(override.override_format_pieces)
                result.append(string)
            else:
                override = lilypondnametools.LilyPondGrobOverride(
                    context_name='Staff',
                    grob_name='StaffSymbol',
                    is_once=True,
                    property_path='line-positions',
                    value=schemetools.SchemeVector(*self.lines),
                    )
                string = '\n'.join(override.override_format_pieces)
                result.append(string)
            result.append(r'\startStaff')
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def lines(self):
        r'''Gets line of staff lines spanner.

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> spanner = spannertools.StaffLinesSpanner(lines=1)
            >>> attach(spanner, staff[1:3])
            >>> show(staff) # doctest: +SKIP

        ::

            >>> spanner.lines
            1

        Returns nonnegative integer.
        '''
        return self._lines
