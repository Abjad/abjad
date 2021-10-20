from .. import bundle as _bundle
from .. import enums as _enums
from .. import format as _format
from .. import math as _math


class StemTremolo:
    r"""
    Stem tremolo.

    ..  container:: example

        Sixteenth-note tremolo:

        >>> note = abjad.Note("c'4")
        >>> stem_tremolo = abjad.StemTremolo(16)
        >>> abjad.attach(stem_tremolo, note)
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(note)
            >>> print(string)
            c'4
            :16

    ..  container:: example

        Thirty-second-note tremolo:

        >>> note = abjad.Note("c'4")
        >>> stem_tremolo = abjad.StemTremolo(32)
        >>> abjad.attach(stem_tremolo, note)
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(note)
            >>> print(string)
            c'4
            :32

    ..  container:: example

        REGRESSION. Consider a note, rest, chord to which a stem tremolo is attached.
        When such a note, rest, chord splits into two notes, rests, chords then a stem
        tremolo attaches to each of the resultant notes, rests, chords:

        >>> staff = abjad.Staff("c'4 c'2.")
        >>> abjad.attach(abjad.StemTremolo(), staff[1])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                c'2.
                :16
            }

        >>> abjad.Meter.rewrite_meter(staff[:], abjad.Meter((3, 4)))
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                c'2
                :16
                ~
                c'4
                :16
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_tremolo_flags",)

    _format_slot = "after"

    _time_orientation = _enums.Middle

    ### INITIALIZER ###

    def __init__(self, tremolo_flags: int = 16) -> None:
        if isinstance(tremolo_flags, type(self)):
            tremolo_flags = tremolo_flags.tremolo_flags
        tremolo_flags = int(tremolo_flags)
        if not _math.is_nonnegative_integer_power_of_two(tremolo_flags):
            raise ValueError(f"nonnegative integer power of 2: {tremolo_flags!r}.")
        self._tremolo_flags = tremolo_flags

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Delegates to ``abjad.format.compare_objects()``.
        """
        return _format.compare_objects(self, argument)

    def __hash__(self) -> int:
        """
        Hashes stem tremolo.
        """
        return hash(self.__class__.__name__ + str(self))

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return _format.get_repr(self)

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
        return f":{self.tremolo_flags!s}"

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        return _format.FormatSpecification(storage_format_is_not_indented=True)

    def _get_lilypond_format(self):
        return str(self)

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
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
