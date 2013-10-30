# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools import scoretools
from abjad.tools.spannertools.Spanner import Spanner


class GlissandoSpanner(Spanner):
    r'''A glissando spanner.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> glissando = spannertools.GlissandoSpanner()
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

    Formats nonlast leaves in spanner with LilyPond glissando command.
    '''

    ### INITIALIZER ###

    def __init__(
        self, 
        components=None,
        overrides=None,
        ):
        Spanner.__init__(
            self, 
            components,
            overrides=overrides,
            )

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        pass

    def _format_right_of_leaf(self, leaf):
        result = []
        if not self._is_my_last_leaf(leaf) and \
            isinstance(leaf, (scoretools.Chord, scoretools.Note)):
            result.append(r'\glissando')
        return result
