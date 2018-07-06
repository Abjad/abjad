import typing
from abjad.pitch.PitchSegment import PitchSegment
from .Spanner import Spanner


class OctavationSpanner(Spanner):
    r"""
    Octavation spanner.

    ..  container:: example

        Spans four notes:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> spanner = abjad.OctavationSpanner(start=1)
        >>> abjad.attach(spanner, staff[:])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                \ottava #1
                c'4
                d'4
                e'4
                f'4
                \ottava #0
            }

    ..  container:: example

        Spans one note:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> spanner = abjad.OctavationSpanner(start=1)
        >>> abjad.attach(spanner, staff[:1])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                \ottava #1
                c'4
                \ottava #0
                d'4
                e'4
                f'4
            }

        One-note octavation changes are allowed.

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_start',
        '_stop',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        start: int = 1,
        stop: int = 0,
        ) -> None:
        Spanner.__init__(self)
        assert isinstance(start, int)
        self._start = start
        assert isinstance(stop, int)
        self._stop = stop

    ### PRIVATE PROPERTIES ###

    @property
    def _start_command(self):
        return rf'\ottava #{self.start}'

    @property
    def _stop_command(self):
        return rf'\ottava #{self.stop}'

    ### PRIVATE METHODS ###

    def _copy_keywords(self, new):
        new._start = self.start
        new._stop = self.stop

    def _get_lilypond_format_bundle(self, leaf):
        bundle = self._get_basic_lilypond_format_bundle(leaf)
        if leaf is self[0]:
            strings = self._tweaked_start_command_strings()
            bundle.before.commands.extend(strings)
        if leaf is self[-1]:
            string = self._stop_command_string()
            bundle.after.commands.append(string)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def start(self) -> typing.Optional[int]:
        """
        Gets octavation start.

        ..  container:: example

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> spanner = abjad.OctavationSpanner(start=1)
            >>> abjad.attach(spanner, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            >>> spanner.start
            1

        """
        return self._start

    @property
    def stop(self) -> typing.Optional[int]:
        """
        Gets octavation stop.

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> spanner = abjad.OctavationSpanner(start=2, stop=1)
        >>> abjad.attach(spanner, staff[:])
        >>> abjad.show(staff) # doctest: +SKIP

        >>> spanner.stop
        1

        """
        return self._stop
