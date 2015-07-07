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

            >>> print(format(staff))
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
        '_use_messiaen_style_ties',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        direction=None,
        overrides=None,
        use_messiaen_style_ties=None,
        ):
        Spanner.__init__(
            self,
            overrides=overrides,
            )
        direction = stringtools.expr_to_tridirectional_lilypond_symbol(
            direction)
        self._direction = direction
        self._use_messiaen_style_ties = use_messiaen_style_ties

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        new._direction = self.direction
        new._use_messiaen_style_ties = self.use_messiaen_style_ties

    def _format_right_of_leaf(self, leaf):
        from abjad.tools import scoretools
        result = []
        prototype = (
            scoretools.Container,
            scoretools.Rest,
            scoretools.Skip,
            scoretools.MultimeasureRest,
            )
        if not self.use_messiaen_style_ties:
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
        else:
            if isinstance(leaf, prototype):
                return result
            elif self._is_my_first_leaf(leaf):
                return result
            if self.direction is not None:
                string = r'{} \repeatTie'.format(self.direction)
                result.append(string)
            else:
                result.append(r'\repeatTie')
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

                >>> print(format(staff))
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

                >>> print(format(staff))
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

                >>> print(format(staff))
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

    @property
    def use_messiaen_style_ties(self):
        r'''Is true when tie should use Messiaen-style ties with
        the LilyPond ``\repeatTie`` command.

        ..  container:: example

            **Example 1.** Default values for Messiaen-style ties:

            ::

                >>> staff = Staff("c'8 c'8 c'8 c'8")
                >>> tie = Tie(direction=Up, use_messiaen_style_ties=True)
                >>> attach(tie, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    c'8
                    c'8 ^ \repeatTie
                    c'8 ^ \repeatTie
                    c'8 ^ \repeatTie
                }

            LilyPond's repeat ties are shorter Messiaen-style ties.

        Returns true, false or none.
        '''
        return self._use_messiaen_style_ties