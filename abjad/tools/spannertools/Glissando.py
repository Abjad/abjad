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

        >>> f(staff)
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

        >>> f(staff)
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

    ### INITIALIZER ###

    def __init__(
        self,
        components=None,
        overrides=None,
        avoid_rests=False,
        ):
        Spanner.__init__(
            self,
            components,
            overrides=overrides,
            )
        self._avoid_rests = bool(avoid_rests)

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        pass

    def _format_right_of_leaf(self, leaf):
        r'''Spanner contribution to right of leaf.
        '''
        result = []
        if not self._is_my_last_leaf(leaf) and \
            isinstance(leaf, (scoretools.Chord, scoretools.Note)):
            result.append(r'\glissando')
        return result

    def _format_before_leaf(self, leaf):
        result = []
        if self.avoid_rests:
            if not isinstance(leaf, (scoretools.Chord, scoretools.Note)):
                result.append(
                    r"\once \override NoteColumn #'glissando-skip = ##t")
                result.append(r"\once \override Rest #'transparent = ##t")
        return result

    ### PUBLIC PROPERTIES ###

    @apply
    def avoid_rests():
        def fget(self):
            r'''Gets and sets rest avoidance.

            ..  container:: example

                Gets property:

                ::

                    >>> glissando.avoid_rests
                    True

            ..  container:: example

                Sets property:

                ::

                    >>> glissando.avoid_rests = False
                    >>> glissando.avoid_rests
                    False

            Returns boolean.
            '''
            return self._avoid_rests
        def fset(self, expr):
            self._avoid_rests = bool(expr)
        return property(**locals())
