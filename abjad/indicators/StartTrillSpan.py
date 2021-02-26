import typing

from ..bundle import LilyPondFormatBundle
from ..overrides import TweakInterface
from ..pitch.intervals import NamedInterval
from ..pitch.pitches import NamedPitch
from ..storage import StorageFormatManager


class StartTrillSpan:
    r"""
    LilyPond ``\startTrillSpan`` command.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> start_trill_span = abjad.StartTrillSpan()
        >>> abjad.tweak(start_trill_span).color = "#blue"
        >>> abjad.attach(start_trill_span, staff[0])
        >>> stop_trill_span = abjad.StopTrillSpan()
        >>> abjad.attach(stop_trill_span, staff[-1])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak color #blue
                \startTrillSpan
                d'4
                e'4
                f'4
                \stopTrillSpan
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_interval", "_pitch", "_tweaks")

    _context = "Voice"

    _parameter = "TRILL"

    _persistent = True

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        interval: typing.Union[str, NamedInterval] = None,
        pitch: typing.Union[str, NamedPitch] = None,
        tweaks: TweakInterface = None,
    ) -> None:
        if interval is not None:
            interval = NamedInterval(interval)
        self._interval = interval
        if pitch is not None:
            pitch = NamedPitch(pitch)
        self._pitch = pitch
        if tweaks is not None:
            assert isinstance(tweaks, TweakInterface), repr(tweaks)
        self._tweaks = TweakInterface.set_tweaks(self, tweaks)

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Is true when all initialization values of Abjad value object equal
        the initialization values of ``argument``.
        """
        return StorageFormatManager.compare_objects(self, argument)

    def __hash__(self) -> int:
        """
        Hashes Abjad value object.
        """
        hash_values = StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
            bundle.after.spanner_starts.extend(tweaks)
        string = r"\startTrillSpan"
        if self.interval or self.pitch:
            bundle.opening.spanners.append(r"\pitchedTrill")
            if self.pitch:
                pitch = self.pitch
            else:
                pitch = component.written_pitch + self.interval
            string = string + f" {pitch!s}"
        bundle.after.spanner_starts.append(string)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def context(self) -> str:
        """
        Returns (historically conventional) context ``'Voice'``.

        ..  container:: example

            >>> abjad.StartTrillSpan().context
            'Voice'

        Class constant.

        Override with ``abjad.attach(..., context='...')``.
        """
        return self._context

    @property
    def interval(self) -> typing.Optional[NamedInterval]:
        r"""
        Gets interval.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> start_trill_span = abjad.StartTrillSpan(interval='M2')
            >>> abjad.tweak(start_trill_span).color = "#blue"
            >>> abjad.attach(start_trill_span, staff[0])
            >>> stop_trill_span = abjad.StopTrillSpan()
            >>> abjad.attach(stop_trill_span, staff[-1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \pitchedTrill
                    c'4
                    - \tweak color #blue
                    \startTrillSpan d'
                    d'4
                    e'4
                    f'4
                    \stopTrillSpan
                }

        """
        return self._interval

    @property
    def parameter(self) -> str:
        """
        Returns ``'TRILL'``.

        ..  container:: example

            >>> abjad.StartTrillSpan().parameter
            'TRILL'

        Class constant.
        """
        return self._parameter

    @property
    def persistent(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> abjad.StartTrillSpan().persistent
            True

        Class constant.
        """
        return self._persistent

    @property
    def pitch(self) -> typing.Optional[NamedPitch]:
        r"""
        Gets pitch.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> start_trill_span = abjad.StartTrillSpan(pitch='C#4')
            >>> abjad.tweak(start_trill_span).color = "#blue"
            >>> abjad.attach(start_trill_span, staff[0])
            >>> stop_trill_span = abjad.StopTrillSpan()
            >>> abjad.attach(stop_trill_span, staff[-1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \pitchedTrill
                    c'4
                    - \tweak color #blue
                    \startTrillSpan cs'
                    d'4
                    e'4
                    f'4
                    \stopTrillSpan
                }

        """
        return self._pitch

    @property
    def spanner_start(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> abjad.StartTrillSpan().spanner_start
            True

        """
        return True

    @property
    def tweaks(self) -> typing.Optional[TweakInterface]:
        r"""
        Gets tweaks

        ..  container:: example

            REGRESSION. Tweaks survive copy:

            >>> import copy
            >>> start_trill_span = abjad.StartTrillSpan()
            >>> abjad.tweak(start_trill_span).color = "#blue"
            >>> string = abjad.storage(start_trill_span)
            >>> print(string)
            abjad.StartTrillSpan(
                tweaks=TweakInterface(('_literal', None), ('color', '#blue')),
                )

            >>> start_trill_span_2 = copy.copy(start_trill_span)
            >>> string = abjad.storage(start_trill_span_2)
            >>> print(string)
            abjad.StartTrillSpan(
                tweaks=TweakInterface(('_literal', None), ('color', '#blue')),
                )

        """
        return self._tweaks
