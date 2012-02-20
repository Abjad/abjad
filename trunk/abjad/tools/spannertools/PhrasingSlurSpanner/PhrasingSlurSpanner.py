from abjad.tools.spannertools.PhrasingSlurSpanner._PhrasingSlurSpannerFormatInterface import _PhrasingSlurSpannerFormatInterface
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

    def __init__(self, components = None, direction = None):
        _DirectedSpanner.__init__(self, components, direction)
        self._format = _PhrasingSlurSpannerFormatInterface(self)
