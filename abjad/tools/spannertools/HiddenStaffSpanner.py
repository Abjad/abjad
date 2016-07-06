# -*- coding: utf-8 -*-
from abjad.tools.spannertools.Spanner import Spanner


class HiddenStaffSpanner(Spanner):
    r'''Hidden staff spanner.

    ..  container:: example

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> spanner = spannertools.HiddenStaffSpanner()
            >>> attach(spanner, staff[1:3])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new Staff {
                c'8
                \stopStaff
                d'8
                e'8
                \startStaff
                f'8
            }

    Formats LilyPond ``\stopStaff`` before first leaf in spanner.

    Formats LilyPond ``\startStaff`` command after last leaf in spanner.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(
        self,
        overrides=None,
        ):
        Spanner.__init__(
            self,
            overrides=overrides,
            )

    ### PRIVATE METHODS ###

    def _format_after_leaf(self, leaf):
        result = []
        if self._is_my_last_leaf(leaf):
            result.append(r'\startStaff')
        return result

    def _format_before_leaf(self, leaf):
        result = []
        if self._is_my_first_leaf(leaf):
            result.append(r'\stopStaff')
        return result