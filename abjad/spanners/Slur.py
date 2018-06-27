import typing
from abjad import enums
from abjad.utilities.String import String
from .Spanner import Spanner


class Slur(Spanner):
    r"""
    Slur.

    ..  container:: example

        Slurs four notes:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(abjad.Slur(), staff[:])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                (
                d'4
                e'4
                f'4
                )
            }

    ..  container:: example

        Tweaks slur color:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> slur = abjad.Slur()
        >>> abjad.tweak(slur).color = 'red'
        >>> abjad.attach(slur, staff[:])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                - \tweak color #red
                (
                d'4
                e'4
                f'4
                )
            }

    ..  container:: example

        Raises exception on fewer than two leaves:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(abjad.Slur(), staff[:1])
        Traceback (most recent call last):
            ...
        Exception: Slur()._attachment_test_all():
          Requires at least two leaves.
          Not just Note("c'4").

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_direction',
        '_leak',
        )

    _start_command = '('

    _stop_command = ')'

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        direction: typing.Union[str, enums.VerticalAlignment] = None,
        leak: bool = None,
        ) -> None:
        Spanner.__init__(self)
        direction = String.to_tridirectional_lilypond_symbol(direction)
        self._direction = direction
        if leak is not None:
            leak = bool(leak)
        self._leak = leak

    ### PRIVATE METHODS ###

    def _attachment_test_all(self, component_expression):
        if self.leak:
            return True
        return self._at_least_two_leaves(component_expression)

    def _copy_keywords(self, new):
        new._direction = self.direction

    def _get_lilypond_format_bundle(self, leaf):
        bundle = self._get_basic_lilypond_format_bundle(leaf)
        if self._is_my_only(leaf):
            if self.leak:
                strings = self.start_command()
                bundle.after.spanner_starts.extend(strings)
                string = self.stop_command()
                bundle.after.spanner_starts.append(string)
            return bundle
        assert 1 < len(self)
        if leaf is self[0]:
            strings = self.start_command()
            bundle.after.spanner_starts.extend(strings)
        elif leaf is self[-1]:
            string = self.stop_command()
            bundle.after.spanner_stops.append(string)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def direction(self) -> typing.Optional[String]:
        r"""
        Gets direction.

        ..  container:: example

            Forces slur above staff:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> slur = abjad.Slur(direction=abjad.Up)
            >>> abjad.attach(slur, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    ^ (
                    d'8
                    e'8
                    f'8
                    )
                }

        ..  container:: example

            Forces slur below staff:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> slur = abjad.Slur(direction=abjad.Down)
            >>> abjad.attach(slur, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    _ (
                    d'8
                    e'8
                    f'8
                    )
                }

        ..  container:: example

            Positions slur according to LilyPond defaults:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> slur = abjad.Slur(direction=None)
            >>> abjad.attach(slur, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    (
                    d'8
                    e'8
                    f'8
                    )
                }

        """
        return self._direction

    @property
    def leak(self):
        r"""
        Is true when slur leaks one leaf to the right.

        ..  container:: example

            Without leak: 

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> slur = abjad.Slur()
            >>> abjad.attach(slur, staff[:-1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    (
                    d'8
                    e'8
                    )
                    f'8
                }

            With leak: 

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> slur = abjad.Slur(leak=True)
            >>> abjad.attach(slur, staff[:-1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    (
                    d'8
                    e'8
                    <> )
                    f'8
                }

        ..  container:: example

            Leaked slurs can be attached to a lone leaf:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> slur = abjad.Slur(leak=True)
            >>> abjad.attach(slur, staff[:1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    (
                    <> )
                    d'8
                    e'8
                    f'8
                }

        """
        return self._leak

    ### PUBLIC METHODS ###

    def start_command(self) -> typing.List[str]:
        """
        Gets start command.

        ..  container:: example

            >>> abjad.Slur().start_command()
            ['(']

        """
        return super().start_command()

    def stop_command(self) -> typing.Optional[str]:
        """
        Gets stop command.

        ..  container:: example

            >>> abjad.Slur().stop_command()
            ')'

            With leak:

            >>> abjad.Slur(leak=True).stop_command()
            '<> )'

        """
        string = super().stop_command()
        if self.leak:
            string = f'{self._empty_chord} {string}'
        return string
