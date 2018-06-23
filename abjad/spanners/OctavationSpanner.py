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

    ### PRIVATE METHODS ###

    def _copy_keywords(self, new):
        new._start = self.start
        new._stop = self.stop

    def _get_lilypond_format_bundle(self, leaf):
        bundle = self._get_basic_lilypond_format_bundle(leaf)
        if leaf is self[0]:
            strings = self.start_command()
            bundle.before.commands.extend(strings)
        if leaf is self[-1]:
            string = self.stop_command()
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

    ### PUBLIC METHODS ###

    # TODO: add two or three more examples to better show what's going on
    def adjust_automatically(
        self,
        ottava_breakpoint: int = None,
        quindecisima_breakpoint: int = None,
        ) -> None:
        r"""
        Adjusts octavation spanner start and stop automatically according to
        ``ottava_breakpoint`` and ``quindecisima_breakpoint``.

        ..  container:: example

            >>> measure = abjad.Measure((4, 8), "c'''8 d'''8 ef'''8 f'''8")
            >>> octavation = abjad.OctavationSpanner(start=1)
            >>> abjad.attach(octavation, measure[:])
            >>> abjad.show(measure) # doctest: +SKIP

            >>> octavation.adjust_automatically(ottava_breakpoint=14)
            >>> abjad.show(measure) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(measure)
                {   % measure
                    \time 4/8
                    \ottava #1
                    c'''8
                    d'''8
                    ef'''8
                    f'''8
                    \ottava #0
                }   % measure

        Adjusts start and stop according to the diatonic pitch number of
        the maximum pitch in spanner.
        """
        pitches = PitchSegment.from_selection(self)
        max_pitch = max(pitches)
        max_numbered_diatonic_pitch = max_pitch._get_diatonic_pitch_number()
        if ottava_breakpoint is not None:
            if ottava_breakpoint <= max_numbered_diatonic_pitch:
                # TODO: do not adjust in place
                #       create & attach new spanner instead
                self._start = 1
                if quindecisima_breakpoint is not None:
                    if quindecisima_breakpoint <= max_numbered_diatonic_pitch:
                        self._start = 2
                        
    ### PUBLIC METHODS ###

    def start_command(self) -> typing.List[str]:
        r"""
        Gets start command.

        ..  container:: example

            >>> abjad.OctavationSpanner(start=1).start_command()
            ['\\ottava #1']

        """
        return super().start_command()

    def stop_command(self) -> typing.Optional[str]:
        r"""
        Gets stop command.

        ..  container:: example

            >>> abjad.OctavationSpanner(start=1).stop_command()
            '\\ottava #0'

        """
        return rf'\ottava #{self.stop}'
