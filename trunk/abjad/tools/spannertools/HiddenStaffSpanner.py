# -*- encoding: utf-8 -*-
from abjad.tools.spannertools.Spanner import Spanner


class HiddenStaffSpanner(Spanner):
    r'''A hidden staff spanner.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        >>> spannertools.HiddenStaffSpanner(staff[:2])
        HiddenStaffSpanner(c'8, d'8)

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \stopStaff
            c'8
            d'8
            \startStaff
            e'8
            f'8
        }

    ::

        >>> show(staff) # doctest: +SKIP

    Hide staff behind leaves in spanner.

    Returns hidden staff spanner.
    '''

    ### INITIALIZER ###

    def __init__(
        self, 
        components=None,
        overrides=None,
        ):
        Spanner.__init__(
            self, 
            components,
            overrides=overrides,
            )

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        pass

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
