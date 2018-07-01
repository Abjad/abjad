import typing
from abjad import enums
from abjad.utilities.String import String
from .Spanner import Spanner


class PhrasingSlur(Spanner):
    r"""
    Phrasing slur.

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

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_direction',
        )

    _start_command = r'\('

    _stop_command = r'\)'

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        direction: typing.Union[str, enums.VerticalAlignment] = None,
        ) -> None:
        Spanner.__init__(self)
        direction_ = String.to_tridirectional_lilypond_symbol(direction)
        self._direction = direction_

    ### PRIVATE METHODS ###

    def _attachment_test_all(self, argument):
        return self._at_least_two_leaves(argument)

    def _copy_keywords(self, new):
        new._direction = self.direction

    def _get_lilypond_format_bundle(self, leaf):
        bundle = self._get_basic_lilypond_format_bundle(leaf)
        if self._is_my_only(leaf):
            return bundle
        assert 1 < len(self)
        if leaf is self[0]:
            strings = self._tweaked_start_command_strings()
            bundle.after.spanner_starts.extend(strings)
        elif leaf is self[-1]:
            string = self._stop_command_string()
            bundle.after.spanner_stops.append(string)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def direction(self) -> typing.Optional[String]:
        r"""
        Gets direction.

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

        """
        return self._direction
