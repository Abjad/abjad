from abjad.tools.spannertools.SlurSpanner._SlurSpannerFormatInterface import _SlurSpannerFormatInterface
from abjad.tools.spannertools.Spanner import Spanner


class SlurSpanner(Spanner):
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

    def __init__(self, components = None):
        Spanner.__init__(self, components)
        self._format = _SlurSpannerFormatInterface(self)
