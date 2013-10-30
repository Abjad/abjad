# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools import scoretools
from abjad.tools.spannertools.Spanner import Spanner


class ComplexGlissandoSpanner(Spanner):
    r'''A rest-skipping glissando spanner.

    ::

        >>> staff = Staff("c'16 r r g' r8 c'8")
        >>> glissando = spannertools.ComplexGlissandoSpanner()
        >>> attach(glissando, staff[:])
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

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

    Should be used with BeamSpanner for best effect, along with
    an override of stemlet-length, in order to generate stemlets over
    each invisible rest.

    Formats nonlast leaves in spanner with LilyPond glissando command.

    Sets all rests to transparent.

    Sets all NoteColumns filled with silences to be skipped by glissandi.
    '''

    ### INITIALIZER ###

    def __init__(self, components=None, overrides=None):
        Spanner.__init__(
            self, 
            components,
            overrides=overrides,
            )

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        pass

    def _format_before_leaf(self, leaf):
        result = []
        if not isinstance(leaf, (scoretools.Chord, scoretools.Note)):
            result.append(r"\once \override NoteColumn #'glissando-skip = ##t")
            result.append(r"\once \override Rest #'transparent = ##t")
        return result

    def _format_right_of_leaf(self, leaf):
        r'''Spanner contribution to right of leaf.
        '''
        result = []
        if not self._is_my_last_leaf(leaf) and \
            isinstance(leaf, (scoretools.Chord, scoretools.Note)):
            result.append(r'\glissando')
        return result
