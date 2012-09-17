from abjad.tools import stringtools
from abjad.tools.spannertools.DirectedSpanner.DirectedSpanner import DirectedSpanner


class PhrasingSlurSpanner(DirectedSpanner):
    r'''Abjad phrasing slur spanner::

        >>> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        >>> spannertools.PhrasingSlurSpanner(staff[:])
        PhrasingSlurSpanner(c'8, d'8, e'8, f'8)

    ::

        >>> f(staff)
        \new Staff {
            c'8 \(
            d'8
            e'8
            f'8 \)
        }

    Return phrasing slur spanner.
    '''

    ### INITIALIZER ###

    def __init__(self, components=None, direction=None):
        DirectedSpanner.__init__(self, components, direction)

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        DirectedSpanner._copy_keyword_args(self, new)

    def _format_right_of_leaf(self, leaf):
        result = []
        if self._is_my_first_leaf(leaf):
            if self.direction is not None:
                result.append(r'{} \('.format(stringtools.arg_to_tridirectional_lilypond_symbol(self.direction)))
            else:
                result.append(r'\(')
        if self._is_my_last_leaf(leaf):
            result.append(r'\)')
        return result
