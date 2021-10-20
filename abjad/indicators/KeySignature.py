import dataclasses
import typing

from .. import bundle as _bundle
from .. import overrides as _overrides
from ..pitch.pitchclasses import NamedPitchClass
from .Mode import Mode


@dataclasses.dataclass(unsafe_hash=True)
class KeySignature:
    r"""
    Key signature.

    ..  container:: example

        >>> staff = abjad.Staff("e'8 fs'8 gs'8 a'8")
        >>> key_signature = abjad.KeySignature("e", "major")
        >>> abjad.attach(key_signature, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \key e \major
                e'8
                fs'8
                gs'8
                a'8
            }

    ..  container:: example

        >>> staff = abjad.Staff("e'8 fs'8 g'8 a'8")
        >>> key_signature = abjad.KeySignature("e", "minor")
        >>> abjad.attach(key_signature, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \key e \minor
                e'8
                fs'8
                g'8
                a'8
            }

    ..  container:: example

        Tweaks:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> key = abjad.KeySignature("e", "minor")
        >>> abjad.tweak(key).color = "#blue"
        >>> abjad.attach(key, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \tweak color #blue
                \key e \minor
                c'4
                d'4
                e'4
                f'4
            }

    """

    tonic: typing.Union[str, NamedPitchClass] = "c"
    mode: typing.Union[str, Mode] = "major"
    tweaks: typing.Optional[_overrides.TweakInterface] = None

    _is_dataclass = True

    _format_slot = "opening"

    context = "Staff"
    persistent = True
    redraw = True

    def __post_init__(self):
        self.tonic = NamedPitchClass(self.tonic)
        self.mode = Mode(self.mode)
        self.tweaks = _overrides.TweakInterface.set_dataclass_tweaks(self, self.tweaks)

    def __str__(self) -> str:
        """
        Gets string representation of key signature.

        ..  container:: example

            E major:

            >>> str(abjad.KeySignature('e', 'major'))
            'e-major'

        ..  container:: example

            e minor:

            >>> str(abjad.KeySignature('e', 'minor'))
            'e-minor'

        """
        return f"{self.tonic!s}-{self.mode!s}"

    def _get_lilypond_format(self):
        return rf"\key {self.tonic!s} \{self.mode!s}"

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions(directed=False)
            bundle.before.commands.extend(tweaks)
        bundle.before.commands.append(self._get_lilypond_format())
        return bundle

    @property
    def name(self) -> str:
        """
        Gets name of key signature.

        ..  container:: example

            E major:

            >>> key_signature = abjad.KeySignature("e", "major")
            >>> key_signature.name
            'E major'

            e minor:

            >>> key_signature = abjad.KeySignature("e", "minor")
            >>> key_signature.name
            'e minor'

        """
        assert isinstance(self.mode, Mode)
        if self.mode.mode_name == "major":
            tonic = str(self.tonic).upper()
        else:
            tonic = str(self.tonic)
        return f"{tonic!s} {self.mode.mode_name!s}"
