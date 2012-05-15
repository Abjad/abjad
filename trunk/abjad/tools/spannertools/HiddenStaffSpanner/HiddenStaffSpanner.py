from abjad.tools.spannertools.Spanner import Spanner


class HiddenStaffSpanner(Spanner):
    r'''Abjad hidden staff spanner::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        abjad> spannertools.HiddenStaffSpanner(staff[:2])
        HiddenStaffSpanner(c'8, d'8)

    ::

        abjad> f(staff)
        \new Staff {
            \stopStaff
            c'8
            d'8
            \startStaff
            e'8
            f'8
        }

    Hide staff behind leaves in spanner.

    Return hidden staff spanner.
    '''

    ### INITIALIZER ###

    def __init__(self, components=None):
        Spanner.__init__(self, components)

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
