from abjad.tools.spannertools._DirectedSpanner._DirectedSpanner import _DirectedSpanner


class PhrasingSlurSpanner(_DirectedSpanner):
    r'''Abjad phrasing slur spanner::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        abjad> spannertools.PhrasingSlurSpanner(staff[:])
        PhrasingSlurSpanner(c'8, d'8, e'8, f'8)

    ::

        abjad> f(staff)
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
        _DirectedSpanner.__init__(self, components, direction)

    ### PRIVATE METHODS ###

    def _format_right_of_leaf(self, leaf):
        result = []
        if self._is_my_first_leaf(leaf):
            if self.direction is not None:
                result.append(r'%s \(' % self.direction)
            else:
                result.append(r'\(')
        if self._is_my_last_leaf(leaf):
            result.append(r'\)')
        return result
