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

    def _get_lilypond_format_bundle(self, leaf):
        lilypond_format_bundle = self._get_basic_lilypond_format_bundle(leaf)
        prototype = (scoretools.Chord, scoretools.Note)
        if not self._is_my_last_leaf(leaf) and isinstance(leaf, prototype):
            string = r'\glissando'
            lilypond_format_bundle.right.spanner_starts.append(string)
        return lilypond_format_bundle
