from abjad import mathtools
from abjad.system.AbjadValueObject import AbjadValueObject
from abjad.system.FormatSpecification import FormatSpecification
from abjad.system.LilyPondFormatBundle import LilyPondFormatBundle
from abjad.system.StorageFormatManager import StorageFormatManager


class StemTremolo(AbjadValueObject):
    """
    Stem tremolo.

    ..  container:: example

        Sixteenth-note tremolo:

        >>> note = abjad.Note("c'4")
        >>> stem_tremolo = abjad.StemTremolo(16)
        >>> abjad.attach(stem_tremolo, note)
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(note)
            c'4
            :16

    ..  container:: example

        Thirty-second-note tremolo:

        >>> note = abjad.Note("c'4")
        >>> stem_tremolo = abjad.StemTremolo(32)
        >>> abjad.attach(stem_tremolo, note)
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(note)
            c'4
            :32

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_tremolo_flags',
        )

    _format_slot = 'after'

    ### INITIALIZER ###

    def __init__(self, tremolo_flags: int = 16) -> None:
        if isinstance(tremolo_flags, type(self)):
            tremolo_flags = tremolo_flags.tremolo_flags
        tremolo_flags = int(tremolo_flags)
        if not mathtools.is_nonnegative_integer_power_of_two(tremolo_flags):
            message = 'nonnegative integer power of 2: {tremolo_flags!r}.'
            raise ValueError(message)
        self._tremolo_flags = tremolo_flags

    ### SPECIAL METHODS ###

    def __format__(self, format_specification='') -> str:
        """
        Formats stem tremolo.

        ..  container:: example

            Sixteenth-note tremolo:

            >>> stem_tremolo = abjad.StemTremolo(16)
            >>> print(format(stem_tremolo))
            :16

        ..  container:: example

            Thirty-second-note tremolo:

            >>> stem_tremolo = abjad.StemTremolo(32)
            >>> print(format(stem_tremolo))
            :32

        """
        if format_specification in ('', 'lilypond'):
            return self._get_lilypond_format()
        assert format_specification == 'storage'
        return StorageFormatManager(self).get_storage_format()

    def __str__(self) -> str:
        """
        Gets string representation of stem tremolo.

        ..  container:: example

            Sixteenth-note tremolo:

            >>> stem_tremolo = abjad.StemTremolo(16)
            >>> print(str(stem_tremolo))
            :16

        ..  container:: example

            Thirty-second-note tremolo:

            >>> stem_tremolo = abjad.StemTremolo(32)
            >>> print(str(stem_tremolo))
            :32

        """
        return f':{self.tremolo_flags!s}'

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        return FormatSpecification(
            client=self,
            storage_format_is_indented=False,
            )

    def _get_lilypond_format(self):
        return str(self)

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        bundle.after.stem_tremolos.append(self._get_lilypond_format())
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def tremolo_flags(self) -> int:
        """
        Gets tremolo flags of stem tremolo.

        ..  container:: example

            Sixteenth-note tremolo:

            >>> stem_tremolo = abjad.StemTremolo(16)
            >>> stem_tremolo.tremolo_flags
            16

        ..  container:: example

            Thirty-second-note tremolo:

            >>> stem_tremolo = abjad.StemTremolo(32)
            >>> stem_tremolo.tremolo_flags
            32

        Set to nonnegative integer power of 2.
        """
        return self._tremolo_flags

    @property
    def tweaks(self) -> None:
        r"""
        Are not implemented on stem tremolo.
        
        The LilyPond ``:`` command refuses tweaks.

        Override the LilyPond ``StemTremolo`` grob instead.
        """
        pass
