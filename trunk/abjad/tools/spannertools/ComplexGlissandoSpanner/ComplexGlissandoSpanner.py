from abjad.tools.spannertools.ComplexGlissandoSpanner._ComplexGlissandoSpannerFormatInterface \
    import _ComplexGlissandoSpannerFormatInterface
from abjad.tools.spannertools.Spanner import Spanner


class ComplexGlissandoSpanner(Spanner):
    r'''.. versionadded:: 2.29

    Abjad rest-skipping glissando spanner::

        abjad> staff = Staff("c'16 r r g' r8 c'8")

    ::

        abjad> spannertools.ComplexGlissandoSpanner(staff[:])
        ComplexGlissandoSpanner(c'16, r16, r16, g'16, r8, c'8)

    ::

        abjad> f(staff)
        \new Staff {
            c'16 \glissando
            \once \override NoteColumn #'glissando-skip = ##t
            \once \override Rest #'transparent = ##t
            r16
            \once \override NoteColumn #'glissando-skip = ##t
            \once \override Rest #'transparent = ##t
            r16
            g'16 \glissando
            \once \override NoteColumn #'glissando-skip = ##t
            \once \override Rest #'transparent = ##t
            r8
            c'8
        }

    Should be used with spannertools.BeamSpanner for best effect, along with
    an override of Stem #'stemlet-length, in order to generate stemlets over
    each invisible rest.

    Format nonlast leaves in spanner with LilyPond glissando command.

    Set all Rest instances to transparent.

    Set all NoteColumns filled with silences to be skipped by glissandi.

    Return `ComplexGlissandoSpanner` instance.
    '''

    def __init__(self, components = None):
        Spanner.__init__(self, components)
        self._format = _ComplexGlissandoSpannerFormatInterface(self)
