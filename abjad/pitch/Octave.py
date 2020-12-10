import functools
import math
import numbers
import re

from ..storage import FormatSpecification, StorageFormatManager
from . import _lib


@functools.total_ordering
class Octave:
    """
    Octave.

    ..  container:: example:

        Initializes octave from integer:

        >>> abjad.Octave(4)
        Octave(4)

    ..  container:: example

        Initializes octave from octave-tick string:

        >>> abjad.Octave(",,")
        Octave(1)

    ..  container:: example

        Initializes octave from named pitch:

        >>> abjad.Octave(abjad.NamedPitch("cs''"))
        Octave(5)

    ..  container:: example

        Initializes octave from other octave:

        >>> abjad.Octave(abjad.Octave(2))
        Octave(2)

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_number",)

    ### INITIALIZER ###

    def __init__(self, number=4):
        if number is None:
            number = 4
        elif isinstance(number, str):
            match = _lib._comprehensive_octave_regex.match(number)
            group_dict = match.groupdict()
            number = 3
            if group_dict["octave_number"]:
                number = int(group_dict["octave_number"])
            elif group_dict["octave_tick"]:
                if group_dict["octave_tick"].startswith("'"):
                    number += group_dict["octave_tick"].count("'")
                else:
                    number -= group_dict["octave_tick"].count(",")
        elif isinstance(number, numbers.Number):
            number = int(number)
        elif hasattr(number, "octave"):
            number = number.octave.number
        elif isinstance(number, type(self)):
            number = number.number
        self._number = number

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        """
        Is true when ``argument`` is octave with same octave number.

        ..  container:: example

            >>> octave_1 = abjad.Octave(4)
            >>> octave_2 = abjad.Octave(4)
            >>> octave_3 = abjad.Octave(5)

            >>> octave_1 == octave_1
            True
            >>> octave_1 == octave_2
            True
            >>> octave_1 == octave_3
            False

            >>> octave_2 == octave_1
            True
            >>> octave_2 == octave_2
            True
            >>> octave_2 == octave_3
            False

            >>> octave_3 == octave_1
            False
            >>> octave_3 == octave_2
            False
            >>> octave_3 == octave_3
            True

        Returns true or false.
        """
        return StorageFormatManager.compare_objects(self, argument)

    def __float__(self):
        """
        Get octave number as float.

        Returns float.
        """
        return float(self.number)

    def __hash__(self):
        """
        Hashes octave.

        Returns integer.
        """
        hash_values = StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __int__(self):
        """
        Get octave number integer.

        Returns integer.
        """
        return int(self.number)

    def __lt__(self, argument):
        """
        Is true when octave is less than ``argument``.

        ..  container:: example

            >>> octave_1 = abjad.Octave(4)
            >>> octave_2 = abjad.Octave(4)
            >>> octave_3 = abjad.Octave(5)

            >>> octave_1 < octave_1
            False
            >>> octave_1 < octave_2
            False
            >>> octave_1 < octave_3
            True

            >>> octave_2 < octave_1
            False
            >>> octave_2 < octave_2
            False
            >>> octave_2 < octave_3
            True

            >>> octave_3 < octave_1
            False
            >>> octave_3 < octave_2
            False
            >>> octave_3 < octave_3
            False

        Returns true or false.
        """
        try:
            argument = type(self)(argument)
        except Exception:
            False
        return self.number < argument.number

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    def __str__(self):
        """
        Gets string representation of octave.

        Defined equal to LilyPond octave / tick representation of octave.

        ..  container:: example

            >>> str(abjad.Octave(4))
            "'"

            >>> str(abjad.Octave(1))
            ',,'

            >>> str(abjad.Octave(3))
            ''

        Returns string.
        """
        return self.ticks

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        return FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_is_indented=False,
            storage_format_args_values=[self.number],
            storage_format_keyword_names=[],
        )

    @classmethod
    def _is_tick_string(class_, argument):
        if not isinstance(argument, str):
            return False
        return bool(class_._octave_tick_regex.match(argument))

    ### PUBLIC PROPERTIES ###

    @property
    def number(self) -> int:
        """
        Gets octave number.

        ..  container:: example

            >>> abjad.Octave(5).number
            5

        """
        return self._number

    @property
    def pitch_number(self) -> int:
        """
        Gets pitch number of first note in octave.

        ..  container:: example

            >>> abjad.Octave(4).pitch_number
            0

            >>> abjad.Octave(5).pitch_number
            12

            >>> abjad.Octave(3).pitch_number
            -12

        """
        return (self.number - 4) * 12

    @property
    def ticks(self) -> str:
        """
        Gets LilyPond octave tick string.

        ..  container:: example

            >>> for i in range(-1, 9):
            ...     print(i, abjad.Octave(i).ticks)
            -1 ,,,,
            0  ,,,
            1  ,,
            2  ,
            3
            4  '
            5  ''
            6  '''
            7  ''''
            8  '''''

        """
        if 3 < self.number:
            return "'" * (self.number - 3)
        elif self.number < 3:
            return "," * abs(3 - self.number)
        return ""

    ### PUBLIC METHODS ###

    @classmethod
    def from_pitch(class_, pitch) -> "Octave":
        """Makes octave from ``pitch``.

        ..  container:: example

            >>> abjad.Octave.from_pitch('cs')
            Octave(3)

            >>> abjad.Octave.from_pitch("cs'")
            Octave(4)

            >>> abjad.Octave.from_pitch(1)
            Octave(4)

            >>> abjad.Octave.from_pitch(13)
            Octave(5)

        """
        if isinstance(pitch, (int, float)):
            number = int(math.floor(pitch / 12)) + 4
            return class_(number)
        if hasattr(pitch, "name"):
            name = pitch.name
        elif isinstance(pitch, str):
            name = pitch
        else:
            raise TypeError(pitch)
        match = re.match(r"^([a-z]+)(\,*|'*)$", name)
        assert match is not None, repr(match)
        name, ticks = match.groups()
        return class_(ticks)
