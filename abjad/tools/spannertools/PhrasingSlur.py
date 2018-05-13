import typing
from abjad.enumerations import VerticalAlignment
from abjad.tools.datastructuretools.String import String
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
        direction: typing.Union[str, VerticalAlignment] = None,
        leak: bool = None,
        ) -> None:
        Spanner.__init__(self, leak=leak)
        direction_ = String.to_tridirectional_lilypond_symbol(direction)
        self._direction = direction_

    ### PRIVATE METHODS ###

    def _attachment_test_all(self, argument):
        if self.leak:
            return True
        return self._at_least_two_leaves(argument)

    def _copy_keyword_args(self, new):
        new._direction = self.direction

    def _get_lilypond_format_bundle(self, leaf):
        bundle = self._get_basic_lilypond_format_bundle(leaf)
        if self._is_my_only(leaf):
            if self.leak:
                string = self.start_command()
                bundle.right.spanner_starts.append(string)
                string = self.stop_command()
                bundle.right.spanner_starts.append(string)
            return bundle
        assert 1 < len(self)
        if leaf is self[0]:
            string = self.start_command()
            bundle.right.spanner_starts.append(string)
        elif leaf is self[-1]:
            string = self.stop_command()
            bundle.right.spanner_stops.append(string)
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

    @property
    def leak(self):
        r"""
        Is true when phrasing slur leaks one leaf to the right.

        ..  container:: example

            Without leak: 

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> slur = abjad.PhrasingSlur()
            >>> abjad.attach(slur, staff[:-1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    \(
                    d'8
                    e'8
                    \)
                    f'8
                }

            With leak: 

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> slur = abjad.PhrasingSlur(leak=True)
            >>> abjad.attach(slur, staff[:-1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    \(
                    d'8
                    e'8
                    <> \)
                    f'8
                }

        ..  container:: example

            Leaked phrasing slurs can be attached to a lone leaf:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> slur = abjad.PhrasingSlur(leak=True)
            >>> abjad.attach(slur, staff[:1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    \(
                    <> \)
                    d'8
                    e'8
                    f'8
                }

        """
        return super(PhrasingSlur, self).leak

    ### PUBLIC METHODS ###

    def start_command(self) -> typing.Optional[str]:
        r"""
        Gets start command.

        ..  container:: example

            >>> abjad.PhrasingSlur().start_command()
            '\\('

            With direction:

            >>> abjad.PhrasingSlur(direction=abjad.Up).start_command()
            '^ \\('

        """
        string = super(PhrasingSlur, self).start_command()
        if self.direction:
            string = f'{self.direction} {string}'
        return string

    def stop_command(self) -> typing.Optional[str]:
        r"""
        Gets stop command.

        ..  container:: example

            >>> abjad.PhrasingSlur().stop_command()
            '\\)'

            With leak:

            >>> abjad.PhrasingSlur(leak=True).stop_command()
            '<> \\)'

        """
        string = super(PhrasingSlur, self).stop_command()
        if self.leak:
            string = f'{self._empty_chord} {string}'
        return string
