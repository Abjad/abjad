from abjad.tools import chordtools
from abjad.tools import notetools
from abjad.tools.spannertools.Spanner import Spanner


class ComplexGlissandoSpanner(Spanner):
    r'''.. versionadded:: 2.9

    Abjad rest-skipping glissando spanner::

        >>> staff = Staff("c'16 r r g' r8 c'8")

    ::

        >>> spannertools.ComplexGlissandoSpanner(staff[:])
        ComplexGlissandoSpanner(c'16, r16, r16, g'16, r8, c'8)

    ::

        >>> f(staff)
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

    Should be used with beamtools.BeamSpanner for best effect, along with
    an override of Stem #'stemlet-length, in order to generate stemlets over
    each invisible rest.

    Format nonlast leaves in spanner with LilyPond glissando command.

    Set all Rest instances to transparent.

    Set all NoteColumns filled with silences to be skipped by glissandi.

    Return `ComplexGlissandoSpanner` instance.
    '''

    ### INITIALIZER ###

    def __init__(self, components=None):
        Spanner.__init__(self, components)

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        pass

    def _format_before_leaf(self, leaf):
        result = []
        if not isinstance(leaf, (chordtools.Chord, notetools.Note)):
            result.append(r"\once \override NoteColumn #'glissando-skip = ##t")
            result.append(r"\once \override Rest #'transparent = ##t")
        return result

    def _format_right_of_leaf(self, leaf):
        '''Spanner contribution to right of leaf.'''
        result = []
        if not self._is_my_last_leaf(leaf) and isinstance(leaf, (chordtools.Chord, notetools.Note)):
            result.append(r'\glissando')
        return result
