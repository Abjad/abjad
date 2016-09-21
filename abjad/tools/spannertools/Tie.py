# -*- coding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools import stringtools
from abjad.tools.spannertools.Spanner import Spanner
from abjad.tools.topleveltools import iterate


class Tie(Spanner):
    r'''Tie.

    ..  container:: example

        **Example 1.** Ties four notes:

        ::

            >>> staff = Staff("c'4 c' c' c'")
            >>> attach(Tie(), staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                c'4 ~
                c'4 ~
                c'4 ~
                c'4
            }

    ..  container:: example

        **Example 2.** Fails attachment test when pitches differ:

        ::

            >>> staff = Staff("c'4 d' e' f'")
            >>> attach(Tie(), staff[:])
            Traceback (most recent call last):
            ...
            Exception: Tie() attachment test fails for Selection([Note("c'4"), Note("d'4"), Note("e'4"), Note("f'4")]).

    ..  container:: example

        **Example 3.** Ties consecutive chords if all adjacent pairs have at least one pitch in common:

        ::

            >>> staff = Staff("<c'>4 <c' d'>4 <d'>4")
            >>> attach(Tie(), staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                <c'>4 ~
                <c' d'>4 ~
                <d'>4
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

    def _attachment_test(self, component):
        from abjad.tools import scoretools
        pitched_prototype = (scoretools.Note, scoretools.Chord)
        return isinstance(component, pitched_prototype)

    def _attachment_test_all(self, component_expression):
        from abjad.tools import scoretools
        from abjad.tools import sequencetools
        #if not self._at_least_two_leaves(component_expression):
        #    return False
        written_pitches = []
        if isinstance(component_expression, scoretools.Component):
            component_expression = [component_expression]
        for component in component_expression:
            if isinstance(component, scoretools.Note):
                written_pitches.append(set([component.written_pitch]))
            elif isinstance(component, scoretools.Chord):
                written_pitches.append(set(component.written_pitches))
            else:
                return False
        for pair in sequencetools.iterate_sequence_nwise(written_pitches):
            if not set.intersection(*pair):
                return False
        return True

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
        r'''Gets direction.

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

        Defaults to none.

        Set to up, down or none.

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
