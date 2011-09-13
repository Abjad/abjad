from abjad.tools.spannertools.GlissandoSpanner._GlissandoSpannerFormatInterface import _GlissandoSpannerFormatInterface
from abjad.tools.spannertools.Spanner import Spanner


class GlissandoSpanner(Spanner):
    r'''Abjad glissando spanner::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        abjad> spannertools.GlissandoSpanner(staff[:])
        GlissandoSpanner(c'8, d'8, e'8, f'8)

    ::

        abjad> f(staff)
        \new Staff {
            c'8 \glissando
            d'8 \glissando
            e'8 \glissando
            f'8
        }

    Format nonlast leaves in spanner with LilyPond glissando command.

    Return glissando spanner.
    '''

    def __init__(self, components = None):
        Spanner.__init__(self, components)
        self._format = _GlissandoSpannerFormatInterface(self)
