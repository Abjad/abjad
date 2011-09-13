from abjad.tools.spannertools.BeamSpanner._BeamSpannerFormatInterface import _BeamSpannerFormatInterface
from abjad.tools.spannertools.Spanner import Spanner


class BeamSpanner(Spanner):
    r'''Abjad beam spanner::

        abjad> staff = Staff("c'8 d'8 e'8 f'8 g'2")

    ::

        abjad> f(staff)
        \new Staff {
            c'8
            d'8
            e'8
            f'8
            g'2
        }

    ::

        abjad> spannertools.BeamSpanner(staff[:4])
        BeamSpanner(c'8, d'8, e'8, f'8)

    ::

        abjad> f(staff)
        \new Staff {
            c'8 [
            d'8
            e'8
            f'8 ]
            g'2
        }

    Return beam spanner.
    '''

    def __init__(self, components = None):
        Spanner.__init__(self, components)
        self._format = _BeamSpannerFormatInterface(self)
