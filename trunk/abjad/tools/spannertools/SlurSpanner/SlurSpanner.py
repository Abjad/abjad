from abjad.tools.spannertools.SlurSpanner._SlurSpannerFormatInterface import _SlurSpannerFormatInterface
from abjad.tools.spannertools._DirectedSpanner._DirectedSpanner import _DirectedSpanner


class SlurSpanner(_DirectedSpanner):
    r'''Abjad slur spanner::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        abjad> spannertools.SlurSpanner(staff[:])
        SlurSpanner(c'8, d'8, e'8, f'8)

    ::

        abjad> f(staff)
        \new Staff {
            c'8 (
            d'8
            e'8
            f'8 )
        }

    Return slur spanner.
    '''

    ### INITIALIZER ###

    def __init__(self, components = None, direction = None):
        _DirectedSpanner.__init__(self, components, direction)
        self._format = _SlurSpannerFormatInterface(self)

    ### PRIVATE METHODS ###

    def _right(self, leaf):
        '''Spanner format contribution right of leaf.'''
        result = []
        spanner = self.spanner
        if spanner._is_my_first_leaf(leaf):
            direction = spanner.direction
            if direction is not None:
                result.append('%s (' % direction)
            else:
                result.append('(')
        if spanner._is_my_last_leaf(leaf):
            result.append(')')
        return result
