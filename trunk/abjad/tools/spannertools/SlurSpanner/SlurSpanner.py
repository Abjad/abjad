from abjad.tools import stringtools
from abjad.tools.spannertools.DirectedSpanner.DirectedSpanner import DirectedSpanner


class SlurSpanner(DirectedSpanner):
    r'''Abjad slur spanner:

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        >>> spannertools.SlurSpanner(staff[:])
        SlurSpanner(c'8, d'8, e'8, f'8)

    ::

        >>> f(staff)
        \new Staff {
            c'8 (
            d'8
            e'8
            f'8 )
        }

    ::

        >>> show(staff) # doctest: +SKIP

    Return slur spanner.
    '''

    ### INITIALIZER ###

    def __init__(self, components=None, direction=None):
        DirectedSpanner.__init__(self, components, direction)

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        DirectedSpanner._copy_keyword_args(self, new)

    def _deposit_format_contributions(self):
        first_leaf = self._get_my_first_leaf()
        if self.direction is not None:
            string = '{} ('.format(stringtools.arg_to_tridirectional_lilypond_symbol(self.direction))
        else:
            string = '('
        override_contributions = self.override._list_format_contributions('override', is_once=False)
        if override_contributions:
            print override_contributions
            first_leaf_opening = first_leaf._spanner_format_contributions.setdefault('opening', [])
            for override_contribution in override_contributions:
                first_leaf_opening.append((self, override_contribution, 'first leaf in spanner'))
        first_leaf_right = first_leaf._spanner_format_contributions.setdefault('right', [])
        first_leaf_right.append((self, string, 'first leaf in spanner'))
        last_leaf = self._get_my_last_leaf()
        last_leaf_right = last_leaf._spanner_format_contributions.setdefault('right', [])
        string = ')'
        last_leaf_right.append((self, string, 'last leaf in spanner'))
        revert_contributions = self.override._list_format_contributions('revert')
        if revert_contributions:
            last_leaf_closing = last_leaf._spanner_format_contributions.setdefault('closing', [])
            for revert_contribution in revert_contributions:
                last_leaf_closing.append((self, revert_contribution, 'last leaf in spanner'))

    def _format_right_of_leaf(self, leaf):
        result = []
        if self._is_my_first_leaf(leaf):
            direction = self.direction
            if direction is not None:
                result.append('{} ('.format(stringtools.arg_to_tridirectional_lilypond_symbol(direction)))
            else:
                result.append('(')
        if self._is_my_last_leaf(leaf):
            result.append(')')
        return result
