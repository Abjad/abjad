# -*- coding: utf-8 -*-
from abjad.tools import datastructuretools
from abjad.tools.spannertools.Spanner import Spanner
from abjad.tools.topleveltools import override
from abjad.tools.topleveltools import iterate


class Slur(Spanner):
    r'''Slur.

    ::

        >>> import abjad

    ..  container:: example

        Slurs four notes:

        ::

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.Slur(), staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                c'4 (
                d'4
                e'4
                f'4 )
            }

    ..  container:: example

        Requires at least two leaves:

        ::

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.Slur(), staff[:1])
            Traceback (most recent call last):
                ...
            Exception: Slur() attachment test fails for Selection([Note("c'4")]).

    Formats LilyPond ``(`` command on first leaf in spanner.

    Formats LilyPond ``)`` command on last leaf in spanner.
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
        direction = datastructuretools.String.to_tridirectional_lilypond_symbol(
            direction)
        self._direction = direction

    ### PRIVATE METHODS ###

    def _attachment_test_all(self, component_expression):
        return self._at_least_two_leaves(component_expression)

    def _copy_keyword_args(self, new):
        new._direction = self.direction

    def _get_lilypond_format_bundle(self, leaf):
        bundle = self._get_basic_lilypond_format_bundle(leaf)
        if self._is_my_only_leaf(leaf):
            pass
        elif self._is_my_first_leaf(leaf):
            if self.direction is not None:
                string = '{} ('.format(self.direction)
            else:
                string = '('
            bundle.right.spanner_starts.append(string)
        elif self._is_my_last_leaf(leaf):
            string = ')'
            bundle.right.spanner_stops.append(string)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def direction(self):
        r'''Gets direction.

        ..  container:: example

            Forces slur above staff:

            ::

                >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
                >>> slur = abjad.Slur(direction=Up)
                >>> abjad.attach(slur, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    c'8 ^ (
                    d'8
                    e'8
                    f'8 )
                    }

        ..  container:: example

            Forces slur below staff:

            ::

                >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
                >>> slur = abjad.Slur(direction=Down)
                >>> abjad.attach(slur, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    c'8 _ (
                    d'8
                    e'8
                    f'8 )
                }

        ..  container:: example

            Positions slur according to LilyPond defaults:

            ::

                >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
                >>> slur = abjad.Slur(direction=None)
                >>> abjad.attach(slur, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    c'8 (
                    d'8
                    e'8
                    f'8 )
                }

        Defaults to none.

        Set to up, down or none.

        Returns up, down or none.
        '''
        return self._direction
