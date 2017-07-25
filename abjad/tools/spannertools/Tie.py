# -*- coding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools import datastructuretools
from abjad.tools.spannertools.Spanner import Spanner
from abjad.tools.topleveltools import iterate


class Tie(Spanner):
    r'''Tie.

    ::

        >>> import abjad

    ..  container:: example

        Ties four notes:

        ::

            >>> staff = abjad.Staff("c'4 c' c' c'")
            >>> abjad.attach(abjad.Tie(), staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                c'4 ~
                c'4 ~
                c'4 ~
                c'4
            }

    ..  container:: example

        Fails attachment test when pitches differ:

        ::

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.Tie(), staff[:])
            Traceback (most recent call last):
                ...
            Exception: Tie() attachment test fails for Selection([Note("c'4"), Note("d'4"), Note("e'4"), Note("f'4")]).

    ..  container:: example

        Ties consecutive chords if all adjacent pairs have at least one pitch
        in common:

        ::

            >>> staff = abjad.Staff("<c'>4 <c' d'>4 <d'>4")
            >>> abjad.attach(abjad.Tie(), staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  docs::

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
        direction = datastructuretools.String.to_tridirectional_lilypond_symbol(
            direction)
        self._direction = direction
        self._use_messiaen_style_ties = use_messiaen_style_ties

    ### PRIVATE METHODS ###

    def _attachment_test(self, component):
        import abjad
        if self._ignore_attachment_test:
            return True
        if not isinstance(component, (abjad.Chord, abjad.Note)):
            return False
        if abjad.inspect(component).has_spanner(abjad.Tie):
            return False
        return True

    def _attachment_test_all(self, component_expression):
        import abjad
        if self._ignore_attachment_test:
            return True
        written_pitches = []
        if isinstance(component_expression, abjad.Component):
            component_expression = [component_expression]
        for component in component_expression:
            if isinstance(component, abjad.Note):
                written_pitches.append(set([component.written_pitch]))
            elif isinstance(component, abjad.Chord):
                written_pitches.append(set(component.written_pitches))
            else:
                return False
        for pair in abjad.Sequence(written_pitches).nwise():
            if not set.intersection(*pair):
                return False
        for component in component_expression:
            if abjad.inspect(component).has_spanner(abjad.Tie):
                return False
        return True

    def _copy_keyword_args(self, new):
        new._direction = self.direction
        new._use_messiaen_style_ties = self.use_messiaen_style_ties

    def _get_lilypond_format_bundle(self, leaf):
        import abjad
        bundle = self._get_basic_lilypond_format_bundle(leaf)
        prototype = (
            abjad.Container,
            abjad.Rest,
            abjad.Skip,
            abjad.MultimeasureRest,
            )
        if not self.use_messiaen_style_ties:
            if self._is_my_last_leaf(leaf):
                return bundle
            elif isinstance(leaf, prototype):
                return bundle
            elif isinstance(leaf._get_leaf(1), prototype):
                return bundle
            if self.direction is not None:
                string = '{} ~'.format(self.direction)
                bundle.right.spanners.append(string)
            else:
                bundle.right.spanners.append('~')
        else:
            if isinstance(leaf, prototype):
                return bundle
            elif self._is_my_first_leaf(leaf):
                return bundle
            if self.direction is not None:
                string = r'{} \repeatTie'.format(self.direction)
                bundle.right.spanners.append(string)
            else:
                bundle.right.spanners.append(r'\repeatTie')
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def direction(self):
        r'''Gets direction.

        ..  container:: example

            Forces ties up:

            ::

                >>> staff = abjad.Staff("c'8 c'8 c'8 c'8")
                >>> tie = abjad.Tie(direction=Up)
                >>> abjad.attach(tie, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
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

                >>> staff = abjad.Staff("c'8 c'8 c'8 c'8")
                >>> tie = abjad.Tie(direction=Down)
                >>> abjad.attach(tie, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
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

                >>> staff = abjad.Staff("c'8 c'8 c'8 c'8")
                >>> tie = abjad.Tie(direction=None)
                >>> abjad.attach(tie, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
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

            Default values for Messiaen-style ties:

            ::

                >>> staff = abjad.Staff("c'8 c'8 c'8 c'8")
                >>> tie = abjad.Tie(direction=Up, use_messiaen_style_ties=True)
                >>> abjad.attach(tie, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
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
