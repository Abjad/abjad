from abjad.tools import chordtools
from abjad.tools import notetools
from abjad.tools.spannertools.Spanner import Spanner


class GlissandoSpanner(Spanner):
    r'''Abjad glissando spanner::

        >>> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        >>> spannertools.GlissandoSpanner(staff[:])
        GlissandoSpanner(c'8, d'8, e'8, f'8)

    ::

        >>> f(staff)
        \new Staff {
            c'8 \glissando
            d'8 \glissando
            e'8 \glissando
            f'8
        }

    Format nonlast leaves in spanner with LilyPond glissando command.

    Return glissando spanner.
    '''

    ### INITIALIZER ###

    def __init__(self, components=None):
        Spanner.__init__(self, components)

    ### PRIVATE METHODS ###
    
    def _copy_keyword_args(self, new):
        pass

    def _format_right_of_leaf(self, leaf):
        result = []
        if not self._is_my_last_leaf(leaf) and isinstance(leaf, (chordtools.Chord, notetools.Note)):
            result.append(r'\glissando')
        return result
