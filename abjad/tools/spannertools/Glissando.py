# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools.spannertools.Spanner import Spanner
from abjad.tools.topleveltools.inspect_ import inspect_


class Glissando(Spanner):
    r'''A glissando.

    ..  container:: example

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> glissando = spannertools.Glissando()
            >>> attach(glissando, staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
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
        '_include_tied_leaves',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        include_tied_leaves=False,
        overrides=None,
        ):
        Spanner.__init__(
            self,
            overrides=overrides,
            )
        assert isinstance(include_tied_leaves, bool), repr(include_tied_leaves)
        self._include_tied_leaves = include_tied_leaves

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, leaf):
        lilypond_format_bundle = self._get_basic_lilypond_format_bundle(leaf)
        prototype = (scoretools.Chord, scoretools.Note)
        if not self._is_my_last_leaf(leaf) and isinstance(leaf, prototype):
            if self.include_tied_leaves:
                string = r'\glissando'
                lilypond_format_bundle.right.spanner_starts.append(string)
            else:
                logical_tie = inspect_(leaf).get_logical_tie()
                if leaf is logical_tie[-1]:
                    string = r'\glissando'
                    lilypond_format_bundle.right.spanner_starts.append(string)
        return lilypond_format_bundle

    ### PUBLIC PROPERTIES ###

    @property
    def include_tied_leaves(self):
        r'''Is true when glissando should include tied leaves.
        Otherwise false.

        ..  container:: example

            **Example 1.** Does not include tied leaves:

            ::

                >>> staff = Staff("c'8 cs'8 d'8 ~ d'8 ~ d'8 ~ d'8 e'4 f'4")
                >>> glissando = Glissando(
                ...     include_tied_leaves=False,
                ...     )
                >>> attach(glissando, staff[:])
                >>> show(staff) # doctest: +SKIP 

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'8 \glissando
                    cs'8 \glissando
                    d'8 ~
                    d'8 ~
                    d'8 ~
                    d'8 \glissando
                    e'4 \glissando
                    f'4
                }

            Default behavior.

        ..  container:: example

            **Example 2.** Does include tied leaves:

            ::

                >>> staff = Staff("c'8 cs'8 d'8 ~ d'8 ~ d'8 ~ d'8 e'4 f'4")
                >>> glissando = Glissando(
                ...     include_tied_leaves=True,
                ...     )
                >>> attach(glissando, staff[:])
                >>> show(staff) # doctest: +SKIP 

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'8 \glissando
                    cs'8 \glissando
                    d'8 ~ \glissando
                    d'8 ~ \glissando
                    d'8 ~ \glissando
                    d'8 \glissando
                    e'4 \glissando
                    f'4
                }




        Defaults to false.
        '''
        return self._include_tied_leaves