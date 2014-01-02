# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools import scoretools
from abjad.tools.spannertools.Spanner import Spanner


class Glissando(Spanner):
    r'''A glissando spanner.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> glissando = spannertools.Glissando()
        >>> attach(glissando, staff[:])
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print format(staff)
        \new Staff {
            c'8 \glissando
            d'8 \glissando
            e'8 \glissando
            f'8
        }

    Can avoid rests:

    ::

        >>> staff = Staff("c'16 r r g' r8 c'8")
        >>> glissando = spannertools.Glissando(avoid_rests=True)
        >>> attach(glissando, staff[:])
        >>> beam = Beam()
        >>> attach(beam, staff[:])
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print format(staff)
        \new Staff {
            c'16 [ \glissando
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
            c'8 ]
        }

    Formats nonlast leaves in spanner with LilyPond glissando command.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_avoid_rests',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        overrides=None,
        avoid_rests=False,
        ):
        Spanner.__init__(
            self,
            overrides=overrides,
            )
        avoid_rests = bool(avoid_rests)
        self._avoid_rests = avoid_rests

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        pass

    def _format_before_leaf(self, leaf):
        result = []
        if self.avoid_rests:
            if not isinstance(leaf, (scoretools.Chord, scoretools.Note)):
                string = r"\once \override NoteColumn #'glissando-skip = ##t"
                result.append(string)
                string = r"\once \override Rest #'transparent = ##t"
                result.append(string)
        return result

    def _format_right_of_leaf(self, leaf):
        r'''Spanner contribution to right of leaf.
        '''
        result = []
        if not self._is_my_last_leaf(leaf):
            if isinstance(leaf, (scoretools.Chord, scoretools.Note)):
                result.append(r'\glissando')
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def avoid_rests(self):
        r'''Gets rest avoidance.

        ..  container:: example

            ::

                >>> glissando.avoid_rests
                True

        Returns boolean.
        '''
        return self._avoid_rests
