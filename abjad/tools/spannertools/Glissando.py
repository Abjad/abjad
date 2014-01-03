# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools.spannertools.Spanner import Spanner


class Glissando(Spanner):
    r'''A glissando.

    ..  container:: example

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

    Formats nonlast leaves in spanner with LilyPond ``\glissando`` command.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(
        self,
        overrides=None,
        ):
        Spanner.__init__(
            self,
            overrides=overrides,
            )

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        pass

    def _format_right_of_leaf(self, leaf):
        result = []
        if not self._is_my_last_leaf(leaf):
            if isinstance(leaf, (scoretools.Chord, scoretools.Note)):
                result.append(r'\glissando')
        return result
