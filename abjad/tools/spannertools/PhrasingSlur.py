# -*- coding: utf-8 -*-
from abjad.tools import datastructuretools
from abjad.tools.spannertools.Spanner import Spanner
from abjad.tools.topleveltools import override


class PhrasingSlur(Spanner):
    r'''Phrasing slur.

    ::

        >>> import abjad

    ..  container:: example

        Spans four notes:

        ::

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> slur = abjad.PhrasingSlur()
            >>> abjad.attach(slur, staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                c'8 \(
                d'8
                e'8
                f'8 \)
            }

    ..  container:: example

        Requires at least two leaves:

        ::

            >>> staff = abjad.Staff("c'8 d' e' f'")
            >>> phrasing_slur = abjad.PhrasingSlur()
            >>> abjad.attach(phrasing_slur, staff[:1])
            Traceback (most recent call last):
                ...
            Exception: PhrasingSlur() attachment test fails for Selection([Note("c'8")]).

    Formats LilyPond ``\(`` command on first leaf in spanner.

    Formats LilyPond ``\)`` comand on last leaf in spanner.
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

    def _attachment_test_all(self, argument):
        return self._at_least_two_leaves(argument)

    def _copy_keyword_args(self, new):
        new._direction = self.direction

    def _get_lilypond_format_bundle(self, leaf):
        bundle = self._get_basic_lilypond_format_bundle(leaf)
        if self._is_my_only_leaf(leaf):
            pass
        elif self._is_my_first_leaf(leaf):
            if self.direction is not None:
                string = '{} \('.format(self.direction)
            else:
                string = '\('
            bundle.right.spanner_starts.append(string)
        elif self._is_my_last_leaf(leaf):
            string = '\)'
            bundle.right.spanner_stops.append(string)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def direction(self):
        r'''Gets direction.

        ..  container:: example

            Positions phrasing slur above staff:

            ::

                >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
                >>> slur = abjad.PhrasingSlur(direction=Up)
                >>> abjad.attach(slur, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    c'8 ^ \(
                    d'8
                    e'8
                    f'8 \)
                }

        ..  container:: example

            Positions phrasing slur below staff:

            ::

                >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
                >>> slur = abjad.PhrasingSlur(direction=Down)
                >>> abjad.attach(slur, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    c'8 _ \(
                    d'8
                    e'8
                    f'8 \)
                }

        ..  container:: example

            Positions phrasing slur according to LilyPond defaults:

            ::

                >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
                >>> slur = abjad.PhrasingSlur(direction=None)
                >>> abjad.attach(slur, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    c'8 \(
                    d'8
                    e'8
                    f'8 \)
                }

        Defaults to none.

        Set to up, down or none.

        Returns up, down or none.
        '''
        return self._direction
