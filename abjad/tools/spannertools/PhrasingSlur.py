from .Spanner import Spanner


class PhrasingSlur(Spanner):
    r'''Phrasing slur.

    ..  container:: example

        Spans four notes:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> slur = abjad.PhrasingSlur()
        >>> abjad.attach(slur, staff[:])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'8
                \(
                d'8
                e'8
                f'8
                \)
            }

    ..  container:: example

        Requires at least two leaves:

        >>> staff = abjad.Staff("c'8 d' e' f'")
        >>> phrasing_slur = abjad.PhrasingSlur()
        >>> abjad.attach(phrasing_slur, staff[:1])
        Traceback (most recent call last):
            ...
        Exception: PhrasingSlur()._attachment_test_all():
          Requires at least two leaves.
          Not just Note("c'8").

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
        import abjad
        Spanner.__init__(self, overrides=overrides)
        direction = abjad.String.to_tridirectional_lilypond_symbol(direction)
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
        elif leaf is self[0]:
            if self.direction is not None:
                string = '{} \('.format(self.direction)
            else:
                string = '\('
            bundle.right.spanner_starts.append(string)
        elif leaf is self[-1]:
            string = '\)'
            bundle.right.spanner_stops.append(string)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def direction(self):
        r'''Gets direction.

        ..  container:: example

            Positions phrasing slur above staff:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> slur = abjad.PhrasingSlur(direction=abjad.Up)
            >>> abjad.attach(slur, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    ^ \(
                    d'8
                    e'8
                    f'8
                    \)
                }

        ..  container:: example

            Positions phrasing slur below staff:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> slur = abjad.PhrasingSlur(direction=abjad.Down)
            >>> abjad.attach(slur, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    _ \(
                    d'8
                    e'8
                    f'8
                    \)
                }

        ..  container:: example

            Positions phrasing slur according to LilyPond defaults:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> slur = abjad.PhrasingSlur(direction=None)
            >>> abjad.attach(slur, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    \(
                    d'8
                    e'8
                    f'8
                    \)
                }

        Defaults to none.

        Set to up, down or none.

        Returns up, down or none.
        '''
        return self._direction
