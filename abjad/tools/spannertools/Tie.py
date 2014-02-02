# -*- encoding: utf-8 -*-
from abjad.tools import stringtools
from abjad.tools.spannertools.Spanner import Spanner


class Tie(Spanner):
    r'''A collection of consecutive ties.

    ..  container:: example

        ::

            >>> staff = Staff("c'8 c'8 c'8 c'8")
            >>> tie = Tie()
            >>> attach(tie, staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print format(staff)
            \new Staff {
                c'8 ~
                c'8 ~
                c'8 ~
                c'8
            }

    Formats LilyPond ``~`` command on nonlast leaves in spanner.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_direction',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        direction=None,
        overrides=None,
        ):
        Spanner.__init__(
            self,
            overrides=overrides,
            )
        direction = stringtools.arg_to_tridirectional_lilypond_symbol(
            direction)
        self._direction = direction

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        new._direction = self.direction

    def _format_right_of_leaf(self, leaf):
        from abjad.tools import scoretools
        result = []
        prototype = (
            scoretools.Rest,
            scoretools.Skip,
            scoretools.MultimeasureRest,
            )
        if self._is_my_last_leaf(leaf):
            return result
        elif isinstance(leaf, prototype):
            return result
        elif isinstance(leaf._get_leaf(1), prototype):
            return result
        if self.direction is not None:
            string = '{} ~'.format(self.direction)
            result.append(string)
        else:
            result.append('~')
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def direction(self):
        r'''Gets direction of ties in spanner.

        ..  container:: example

            Forces ties up:

            ::

                >>> staff = Staff("c'8 c'8 c'8 c'8")
                >>> tie = Tie(direction=Up)
                >>> attach(tie, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print format(staff)
                \new Staff {
                    c'8 ^ ~
                    c'8 ^ ~
                    c'8 ^ ~
                    c'8
                }

            ::

                >>> tie.direction
                '^'

        ..  container:: example

            Forces ties down:

            ::

                >>> staff = Staff("c'8 c'8 c'8 c'8")
                >>> tie = Tie(direction=Down)
                >>> attach(tie, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print format(staff)
                \new Staff {
                    c'8 _ ~
                    c'8 _ ~
                    c'8 _ ~
                    c'8
                }

            ::

                >>> tie.direction
                '_'

        ..  container:: example

            Positions ties according to LilyPond defaults:

            ::

                >>> staff = Staff("c'8 c'8 c'8 c'8")
                >>> tie = Tie(direction=None)
                >>> attach(tie, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print format(staff)
                \new Staff {
                    c'8 ~
                    c'8 ~
                    c'8 ~
                    c'8
                }

            ::

                >>> tie.direction is None
                True

        Returns up, down or none.
        '''
        return self._direction
