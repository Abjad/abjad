import typing

from ..bundle import LilyPondFormatBundle
from ..overrides import TweakInterface
from ..pitch.pitchclasses import NamedPitchClass
from ..storage import FormatSpecification, StorageFormatManager
from .Mode import Mode


class KeySignature:
    r"""
    Key signature.

    ..  container:: example

        >>> staff = abjad.Staff("e'8 fs'8 gs'8 a'8")
        >>> key_signature = abjad.KeySignature('e', 'major')
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
        >>> key_signature = abjad.KeySignature('e', 'minor')
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

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_mode", "_tonic", "_tweaks")

    _context = "Staff"

    _format_slot = "opening"

    _persistent = True

    _redraw = True

    ### INITIALIZER ###

    def __init__(
        self,
        tonic: str = "c",
        mode: str = "major",
        *,
        tweaks: TweakInterface = None,
    ) -> None:
        self._tonic = NamedPitchClass(tonic)
        self._mode = Mode(mode)
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

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        values = [self.tonic, self.mode]
        return FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_is_indented=False,
            storage_format_args_values=values,
        )

    def _get_lilypond_format(self):
        return rf"\key {self.tonic!s} \{self.mode!s}"

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions(directed=False)
            bundle.before.commands.extend(tweaks)
        bundle.before.commands.append(self._get_lilypond_format())
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def context(self) -> str:
        """
        Gets (historically conventional) context.

        ..  container:: example

            E major:

            >>> key_signature = abjad.KeySignature('e', 'major')
            >>> key_signature.context
            'Staff'

        ..  container:: example

            e minor:

            >>> key_signature = abjad.KeySignature('e', 'minor')
            >>> key_signature.context
            'Staff'

        Override with ``abjad.attach(..., context='...')``.
        """
        return self._context

    @property
    def mode(self) -> Mode:
        """
        Gets mode of key signature.

        ..  container:: example

            E major:

            >>> key_signature = abjad.KeySignature('e', 'major')
            >>> key_signature.mode
            Mode('major')

        ..  container:: example

            e minor:

            >>> key_signature = abjad.KeySignature('e', 'minor')
            >>> key_signature.mode
            Mode('minor')

        """
        return self._mode

    @property
    def name(self) -> str:
        """
        Gets name of key signature.

        ..  container:: example

            E major:

            >>> key_signature = abjad.KeySignature('e', 'major')
            >>> key_signature.name
            'E major'

        ..  container:: example

            e minor:

            >>> key_signature = abjad.KeySignature('e', 'minor')
            >>> key_signature.name
            'e minor'

        """
        if self.mode.mode_name == "major":
            tonic = str(self.tonic).upper()
        else:
            tonic = str(self.tonic)
        return f"{tonic!s} {self.mode.mode_name!s}"

    @property
    def persistent(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> abjad.KeySignature('e', 'major').persistent
            True

        Class constant.
        """
        return self._persistent

    @property
    def redraw(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> abjad.KeySignature('e', 'major').redraw
            True

        Class constant.
        """
        return self._redraw

    @property
    def tonic(self) -> NamedPitchClass:
        """
        Gets tonic of key signature.

        ..  container:: example

            E major:

            >>> key_signature = abjad.KeySignature('e', 'major')
            >>> key_signature.tonic
            NamedPitchClass('e')

        ..  container:: example

            e minor:

            >>> key_signature = abjad.KeySignature('e', 'minor')
            >>> key_signature.tonic
            NamedPitchClass('e')

        """
        return self._tonic

    @property
    def tweaks(self) -> typing.Optional[TweakInterface]:
        r"""
        Gets tweaks.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> key = abjad.KeySignature('e', 'minor')
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
        return self._tweaks
