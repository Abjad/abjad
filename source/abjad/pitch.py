import copy
import dataclasses
import fractions
import functools
import math
import numbers
import re
import typing

from . import enums as _enums
from . import math as _math
from . import string as _string

### MAPPINGS (most will become functions) ###

_direction_number_to_direction_symbol = {0: "", 1: "+", -1: "-"}

# TODO: change to function; accommodate arbitrarily long names
_accidental_abbreviation_to_name = {
    "ss": "double sharp",
    "tqs": "three-quarters sharp",
    "s": "sharp",
    "qs": "quarter sharp",
    "": "natural",
    "qf": "quarter flat",
    "f": "flat",
    "tqf": "three-quarters flat",
    "ff": "double flat",
}

# TODO: change to function; accommodate arbitrarily long names
_accidental_abbreviation_to_semitones = {
    "ff": -2,
    "tqf": -1.5,
    "f": -1,
    "qf": -0.5,
    "": 0,
    "qs": 0.5,
    "s": 1,
    "tqs": 1.5,
    "ss": 2,
}

# TODO: change to function; accommodate arbitrarily long abbreviations
_accidental_abbreviation_to_symbol = {
    "ff": "bb",
    "tqf": "tqf",
    "f": "b",
    "qf": "qf",
    "": "",
    "qs": "qs",
    "s": "#",
    "tqs": "tqs",
    "ss": "##",
}

# TODO: change to function; accommodate arbitrarily long names
_accidental_name_to_abbreviation = {
    "double sharp": "ss",
    "three-quarters sharp": "tqs",
    "sharp": "s",
    "quarter sharp": "qs",
    "natural": "",
    "quarter flat": "qf",
    "flat": "f",
    "three-quarters flat": "tqf",
    "double flat": "ff",
}

# TODO: change to function; accommodate arbitrary numeric input
_accidental_semitones_to_abbreviation = {
    -2.0: "ff",
    -1.5: "tqf",
    -1.0: "f",
    -0.5: "qf",
    0.0: "",
    0.5: "qs",
    1.0: "s",
    1.5: "tqs",
    2.0: "ss",
}

_diatonic_pc_name_to_diatonic_pc_number = {
    "c": 0,
    "d": 1,
    "e": 2,
    "f": 3,
    "g": 4,
    "a": 5,
    "b": 6,
}

_diatonic_pc_name_to_pitch_class_number = {
    "c": 0,
    "d": 2,
    "e": 4,
    "f": 5,
    "g": 7,
    "a": 9,
    "b": 11,
}

_diatonic_pc_number_to_diatonic_pc_name = {
    0: "c",
    1: "d",
    2: "e",
    3: "f",
    4: "g",
    5: "a",
    6: "b",
}

_diatonic_pc_number_to_pitch_class_number = {
    0: 0,
    1: 2,
    2: 4,
    3: 5,
    4: 7,
    5: 9,
    6: 11,
}

_pitch_class_number_to_diatonic_pc_number = {
    0: 0,
    2: 1,
    4: 2,
    5: 3,
    7: 4,
    9: 5,
    11: 6,
}

_pitch_class_number_to_pitch_class_name = {
    0.0: "c",
    0.5: "cqs",
    1.0: "cs",
    1.5: "dqf",
    2.0: "d",
    2.5: "dqs",
    3.0: "ef",
    3.5: "eqf",
    4.0: "e",
    4.5: "eqs",
    5.0: "f",
    5.5: "fqs",
    6.0: "fs",
    6.5: "gqf",
    7.0: "g",
    7.5: "gqs",
    8.0: "af",
    8.5: "aqf",
    9.0: "a",
    9.5: "aqs",
    10.0: "bf",
    10.5: "bqf",
    11.0: "b",
    11.5: "bqs",
}

_pitch_class_number_to_pitch_class_name_with_flats = {
    0.0: "c",
    0.5: "dtqf",
    1.0: "df",
    1.5: "dqf",
    2.0: "d",
    2.5: "etqf",
    3.0: "ef",
    3.5: "eqf",
    4.0: "e",
    4.5: "fqf",
    5.0: "f",
    5.5: "gtqf",
    6.0: "gf",
    6.5: "gqf",
    7.0: "g",
    7.5: "atqf",
    8.0: "af",
    8.5: "aqf",
    9.0: "a",
    9.5: "btqf",
    10.0: "bf",
    10.5: "bqf",
    11.0: "b",
    11.5: "cqf",
}

_pitch_class_number_to_pitch_class_name_with_sharps = {
    0.0: "c",
    0.5: "cqs",
    1.0: "cs",
    1.5: "ctqs",
    2.0: "d",
    2.5: "dqs",
    3.0: "ds",
    3.5: "dtqs",
    4.0: "e",
    4.5: "eqs",
    5.0: "f",
    5.5: "fqs",
    6.0: "fs",
    6.5: "ftqs",
    7.0: "g",
    7.5: "gqs",
    8.0: "gs",
    8.5: "gtqs",
    9.0: "a",
    9.5: "aqs",
    10.0: "as",
    10.5: "atqs",
    11.0: "b",
    11.5: "bqs",
}

_diatonic_number_to_quality_dictionary = {
    1: {"d": -1, "P": 0, "A": 1},
    2: {"d": 0, "m": 1, "M": 2, "A": 3},
    3: {"d": 2, "m": 3, "M": 4, "A": 5},
    4: {"d": 4, "P": 5, "A": 6},
    5: {"d": 6, "P": 7, "A": 8},
    6: {"d": 7, "m": 8, "M": 9, "A": 10},
    7: {"d": 9, "m": 10, "M": 11, "A": 12},
    8: {"d": 11, "P": 12, "A": 13},
}


def _diatonic_number_to_octaves_and_diatonic_remainder(number):
    """
    Captures the idea that diatonic numbers 1 (unison), 8 (octave), 15 (two octaves)
    are all "types of octave."

    Likewise, diatonic numbers 2 (second), 9 (second + octave), 16 (second + two octaves)
    are all "types of (diatonic) second."

    ..  container:: example

        >>> function = abjad.pitch._diatonic_number_to_octaves_and_diatonic_remainder
        >>> for number in range(1, 22 + 1):
        ...     octaves, diatonic_remainder = function(number)
        ...     print(f"{number}: {octaves} octave(s) + {diatonic_remainder}")
        1: 0 octave(s) + 1
        2: 0 octave(s) + 2
        3: 0 octave(s) + 3
        4: 0 octave(s) + 4
        5: 0 octave(s) + 5
        6: 0 octave(s) + 6
        7: 0 octave(s) + 7
        8: 1 octave(s) + 1
        9: 1 octave(s) + 2
        10: 1 octave(s) + 3
        11: 1 octave(s) + 4
        12: 1 octave(s) + 5
        13: 1 octave(s) + 6
        14: 1 octave(s) + 7
        15: 2 octave(s) + 1
        16: 2 octave(s) + 2
        17: 2 octave(s) + 3
        18: 2 octave(s) + 4
        19: 2 octave(s) + 5
        20: 2 octave(s) + 6
        21: 2 octave(s) + 7
        22: 3 octave(s) + 1

    """
    octaves = (number - 1) // 7
    remainder = number - 7 * octaves
    return octaves, remainder


def _diatonic_number_and_quality_to_semitones(number, quality):
    """
    Setup:

    >>> function = abjad.pitch._diatonic_number_and_quality_to_semitones

    Number of semitones in perfect octaves:

        >>> function(1, "P")
        0

        >>> function(8, "P")
        12

        >>> function(15, "P")
        24

    Number of semitones in diminished octaves:

        >>> function(1, "d")
        -1

        >>> function(8, "d")
        11

        >>> function(15, "d")
        23

    Number of semitones in minor seconds:

        >>> function(2, "m")
        1

        >>> function(9, "m")
        13

        >>> function(16, "m")
        25

    Number of semitones in major seconds:

        >>> function(2, "M")
        2

        >>> function(9, "M")
        14

        >>> function(16, "M")
        26

    """
    octaves, diatonic_remainder = _diatonic_number_to_octaves_and_diatonic_remainder(
        number
    )
    quality_to_semitones = _diatonic_number_to_quality_dictionary[diatonic_remainder]
    semitones = quality_to_semitones[quality]
    semitones += 12 * octaves
    return semitones


# TODO: change to function; accommodate arbitrarily large number of semitones
_semitones_to_quality_and_diatonic_number = {
    0: ("P", 1),
    1: ("m", 2),
    2: ("M", 2),
    3: ("m", 3),
    4: ("M", 3),
    5: ("P", 4),
    6: ("d", 5),
    7: ("P", 5),
    8: ("m", 6),
    9: ("M", 6),
    10: ("m", 7),
    11: ("M", 7),
    12: ("P", 8),
}

# TODO: change to function; accommodate arbitrarily large strings like "ddd"
_quality_abbreviation_to_quality_string = {
    "M": "major",
    "m": "minor",
    "P": "perfect",
    "aug": "augmented",
    "dim": "diminished",
    "A": "augmented",
    "d": "diminished",
}

# TODO: change to function; accommodate strings like "double-diminished"
_quality_string_to_quality_abbreviation = {
    "major": "M",
    "minor": "m",
    "perfect": "P",
    "augmented": "A",
    "diminished": "d",
}

# TODO: change to function; accommodate arbitrarily large number of semitones
_semitones_to_quality_string_and_number = {
    0: ("perfect", 1),
    1: ("minor", 2),
    2: ("major", 2),
    3: ("minor", 3),
    4: ("major", 3),
    5: ("perfect", 4),
    6: ("diminished", 5),
    7: ("perfect", 5),
    8: ("minor", 6),
    9: ("major", 6),
    10: ("minor", 7),
    11: ("major", 7),
}

### REGEX ATOMS ###

_integer_regex_atom = r"-?\d+"

_alphabetic_accidental_regex_atom = (
    "(?P<alphabetic_accidental>[s]*(qs)?|[f]*(qf)?|t?q?[fs]|)"
)

_symbolic_accidental_regex_atom = "(?P<symbolic_accidental>[#]+[+]?|[b]+[~]?|[+]|[~]|)"

_octave_number_regex_atom = f"(?P<octave_number>{_integer_regex_atom}|)"

_octave_tick_regex_atom = "(?P<octave_tick>,+|'+|)"

_diatonic_pc_name_regex_atom = "(?P<diatonic_pc_name>[A-Ga-g])"

### REGEX BODIES ###

_comprehensive_accidental_regex_body = ("(?P<comprehensive_accidental>{}|{})").format(
    _alphabetic_accidental_regex_atom, _symbolic_accidental_regex_atom
)

_comprehensive_octave_regex_body = ("(?P<comprehensive_octave>{}|{})").format(
    _octave_number_regex_atom, _octave_tick_regex_atom
)

_comprehensive_pitch_class_name_regex_body = (
    "(?P<comprehensive_pitch_class_name>{}{})"
).format(_diatonic_pc_name_regex_atom, _comprehensive_accidental_regex_body)

_comprehensive_pitch_name_regex_body = ("(?P<comprehensive_pitch_name>{}{}{})").format(
    _diatonic_pc_name_regex_atom,
    _comprehensive_accidental_regex_body,
    _comprehensive_octave_regex_body,
)

_pitch_class_name_regex_body = ("(?P<pitch_class_name>{}{})").format(
    _diatonic_pc_name_regex_atom, _alphabetic_accidental_regex_atom
)

_pitch_name_regex_body = ("(?P<pitch_name>{}{}{})").format(
    _diatonic_pc_name_regex_atom,
    _alphabetic_accidental_regex_atom,
    _octave_tick_regex_atom,
)

_pitch_class_octave_number_regex_body = (
    "(?P<pitch_class_octave_number>{}{}{})"
).format(
    _diatonic_pc_name_regex_atom,
    _comprehensive_accidental_regex_body,
    _octave_number_regex_atom,
)

_pitch_class_octave_number_regex = re.compile(
    "^{}$".format(_pitch_class_octave_number_regex_body), re.VERBOSE
)

_interval_name_abbreviation_regex_body = r"""
    (?P<direction>[+,-]?)  # one plus, one minus, or neither
    (?P<quality>           # exactly one quality abbreviation
        M|                 # major
        m|                 # minor
        P|                 # perfect
        aug|               # augmented
        A+|                # (possibly) multi-augmented
        dim|               # dimished
        d+                 # (possibly) multi-diminished
    )
    (?P<quartertone>[+~]?) # followed by an optional quartertone inflection
    (?P<number>\d+)        # followed by one or more digits
    """

_range_string_regex_body = r"""
    (?P<open_bracket>
        [\[(]       # open bracket or open parenthesis
    )
    (?P<start_pitch>
        {}|{}|(?P<start_pitch_number>-?\d+) # start pitch
    )
    ,               # comma
    [ ]*            # any amount of whitespace
    (?P<stop_pitch>
        {}|{}|(?P<stop_pitch_number>-?\d+) # stop pitch
    )
    (?P<close_bracket>
        [\])]       # close bracket or close parenthesis
    )
    """.format(
    _pitch_class_octave_number_regex_body.replace("<", "<us_start_"),
    _pitch_name_regex_body.replace("<", "<ly_start_"),
    _pitch_class_octave_number_regex_body.replace("<", "<us_stop_"),
    _pitch_name_regex_body.replace("<", "<ly_stop_"),
)

_range_string_regex = re.compile("^{}$".format(_range_string_regex_body), re.VERBOSE)

### REGEX PATTERNS ###

_alphabetic_accidental_regex = re.compile(
    "^{}$".format(_alphabetic_accidental_regex_atom), re.VERBOSE
)

_symbolic_accidental_regex = re.compile(
    "^{}$".format(_symbolic_accidental_regex_atom), re.VERBOSE
)

_comprehensive_accidental_regex = re.compile(
    "^{}$".format(_comprehensive_accidental_regex_body), re.VERBOSE
)

_octave_tick_regex = re.compile("^{}$".format(_octave_tick_regex_atom), re.VERBOSE)

_octave_number_regex = re.compile("^{}$".format(_octave_number_regex_atom), re.VERBOSE)

_diatonic_pc_name_regex = re.compile(
    "^{}$".format(_diatonic_pc_name_regex_atom), re.VERBOSE
)

_comprehensive_accidental_regex = re.compile(
    "^{}$".format(_comprehensive_accidental_regex_body), re.VERBOSE
)

_comprehensive_octave_regex = re.compile(
    "^{}$".format(_comprehensive_octave_regex_body), re.VERBOSE
)

_comprehensive_pitch_class_name_regex = re.compile(
    "^{}$".format(_comprehensive_pitch_class_name_regex_body), re.VERBOSE
)

_comprehensive_pitch_name_regex = re.compile(
    "^{}$".format(_comprehensive_pitch_name_regex_body), re.VERBOSE
)

_pitch_class_name_regex = re.compile(
    "^{}$".format(_pitch_class_name_regex_body), re.VERBOSE
)

_pitch_name_regex = re.compile("^{}$".format(_pitch_name_regex_body), re.VERBOSE)

_interval_name_abbreviation_regex = re.compile(
    "^{}$".format(_interval_name_abbreviation_regex_body), re.VERBOSE
)


@functools.total_ordering
@dataclasses.dataclass(slots=True, unsafe_hash=True)
class Accidental:
    """
    Accidental.

    ..  container:: example

        >>> abjad.Accidental("ff")
        Accidental(name='double flat')

        >>> abjad.Accidental("tqf")
        Accidental(name='three-quarters flat')

        >>> abjad.Accidental("f")
        Accidental(name='flat')

        >>> abjad.Accidental("")
        Accidental(name='natural')

        >>> abjad.Accidental("qs")
        Accidental(name='quarter sharp')

        >>> abjad.Accidental("s")
        Accidental(name='sharp')

        >>> abjad.Accidental("tqs")
        Accidental(name='three-quarters sharp')

        >>> abjad.Accidental("ss")
        Accidental(name='double sharp')

    ..  container:: example

        Generalized accidentals are allowed:

        >>> abjad.Accidental("ssss")
        Accidental(name='ssss')

    ..  container:: example

        Less than is true when ``argument`` is an accidental with semitones greater
        than those of this accidental:

        >>> accidental_1 = abjad.Accidental("f")
        >>> accidental_2 = abjad.Accidental("f")
        >>> accidental_3 = abjad.Accidental("s")

        >>> accidental_1 < accidental_1
        False
        >>> accidental_1 < accidental_2
        False
        >>> accidental_1 < accidental_3
        True

        >>> accidental_2 < accidental_1
        False
        >>> accidental_2 < accidental_2
        False
        >>> accidental_2 < accidental_3
        True

        >>> accidental_3 < accidental_1
        False
        >>> accidental_3 < accidental_2
        False
        >>> accidental_3 < accidental_3
        False

    ..  container:: example

        >>> abjad.Accidental("ff").semitones
        -2

        >>> abjad.Accidental("tqf").semitones
        -1.5

        >>> abjad.Accidental("f").semitones
        -1

        >>> abjad.Accidental("").semitones
        0

        >>> abjad.Accidental("qs").semitones
        0.5

        >>> abjad.Accidental("s").semitones
        1

        >>> abjad.Accidental("tqs").semitones
        1.5

        >>> abjad.Accidental("ss").semitones
        2

    ..  container:: example

        >>> abjad.Accidental("ff").name
        'double flat'

        >>> abjad.Accidental("tqf").name
        'three-quarters flat'

        >>> abjad.Accidental("f").name
        'flat'

        >>> abjad.Accidental("").name
        'natural'

        >>> abjad.Accidental("qs").name
        'quarter sharp'

        >>> abjad.Accidental("s").name
        'sharp'

        >>> abjad.Accidental("tqs").name
        'three-quarters sharp'

        >>> abjad.Accidental("ss").name
        'double sharp'

    """

    name: str = "natural"
    arrow: bool = dataclasses.field(default=False, repr=False)
    semitones: int = dataclasses.field(compare=False, init=False, repr=False)

    def __post_init__(self):
        semitones = 0
        _arrow = None
        if self.name is None:
            pass
        elif isinstance(self.name, str):
            if self.name in _accidental_name_to_abbreviation:
                self.name = _accidental_name_to_abbreviation[self.name]
                semitones = _accidental_abbreviation_to_semitones[self.name]
            else:
                match = _comprehensive_accidental_regex.match(self.name)
                group_dict = match.groupdict()
                if group_dict["alphabetic_accidental"]:
                    prefix, _, suffix = self.name.partition("q")
                    if prefix.startswith("s"):
                        semitones += len(prefix)
                    elif prefix.startswith("f"):
                        semitones -= len(prefix)
                    if suffix == "s":
                        semitones += 0.5
                        if prefix == "t":
                            semitones += 1
                    elif suffix == "f":
                        semitones -= 0.5
                        if prefix == "t":
                            semitones -= 1
                elif group_dict["symbolic_accidental"]:
                    semitones += self.name.count("#")
                    semitones -= self.name.count("b")
                    if self.name.endswith("+"):
                        semitones += 0.5
                    elif self.name.endswith("~"):
                        semitones -= 0.5
        elif isinstance(self.name, numbers.Number):
            semitones = float(self.name)
            assert (semitones % 1.0) in (0.0, 0.5)
        elif hasattr(self.name, "accidental"):
            _arrow = self.name.accidental.arrow
            semitones = self.name.accidental.semitones
        elif isinstance(self.name, type(self)):
            _arrow = self.name.arrow
            semitones = self.name.semitones
        semitones = _math.integer_equivalent_number_to_integer(semitones)
        self.semitones = semitones
        if self.arrow is not None:
            self.arrow = _string.to_tridirectional_ordinal_constant(self.arrow)
            if self.arrow is _enums.CENTER:
                self.arrow = None
        else:
            self.arrow = _arrow
        try:
            abbreviation = _accidental_semitones_to_abbreviation[self.semitones]
            name = _accidental_abbreviation_to_name[abbreviation]
        except KeyError:
            name = str(self)
        self.name = name

    def __add__(self, argument):
        """
        Adds ``argument`` to accidental.

        ..  container:: example

            >>> accidental = abjad.Accidental("qs")

            >>> accidental + accidental
            Accidental(name='sharp')

            >>> accidental + accidental + accidental
            Accidental(name='three-quarters sharp')

        Returns new accidental.
        """
        if not isinstance(argument, type(self)):
            raise TypeError("can only add accidental to other accidental.")
        semitones = self.semitones + argument.semitones
        return type(self)(semitones)

    def __call__(self, argument):
        """
        Calls accidental on ``argument``.

        >>> accidental = abjad.Accidental("s")

        ..  container:: example

            Calls accidental on pitches:

            >>> accidental(abjad.NamedPitch("c''"))
            NamedPitch("cs''")

            >>> accidental(abjad.NamedPitch("cqs''"))
            NamedPitch("ctqs''")

            >>> accidental(abjad.NumberedPitch(12))
            NumberedPitch(13)

            >>> accidental(abjad.NumberedPitch(12.5))
            NumberedPitch(13.5)

        ..  container:: example

            Calls accidental on pitch-classes:

            >>> accidental(abjad.NamedPitchClass("c"))
            NamedPitchClass('cs')

            >>> accidental(abjad.NamedPitchClass("cqs"))
            NamedPitchClass('ctqs')

            >>> accidental(abjad.NumberedPitchClass(0))
            NumberedPitchClass(1)

            >>> accidental(abjad.NumberedPitchClass(0.5))
            NumberedPitchClass(1.5)

        Returns new object of ``argument`` type.
        """
        if not hasattr(argument, "_apply_accidental"):
            raise TypeError(f"do not know how to apply accidental to {argument!r}.")
        return argument._apply_accidental(self)

    def __lt__(self, argument):
        """
        Returns true or false.
        """
        return self.semitones < argument.semitones

    def __neg__(self):
        """
        Negates accidental.

        ..  container:: example

            >>> -abjad.Accidental("ff")
            Accidental(name='double sharp')

            >>> -abjad.Accidental("tqf")
            Accidental(name='three-quarters sharp')

            >>> -abjad.Accidental("f")
            Accidental(name='sharp')

            >>> -abjad.Accidental("")
            Accidental(name='natural')

            >>> -abjad.Accidental("qs")
            Accidental(name='quarter flat')

            >>> -abjad.Accidental("s")
            Accidental(name='flat')

            >>> -abjad.Accidental("tqs")
            Accidental(name='three-quarters flat')

            >>> -abjad.Accidental("ss")
            Accidental(name='double flat')

        Returns new accidental.
        """
        return type(self)(-self.semitones)

    def __radd__(self, argument):
        """
        Raises not implemented error on accidental.
        """
        raise NotImplementedError

    # TODO: remove?
    def __str__(self) -> str:
        """
        Gets string representation of accidental.

        ..  container:: example

            >>> str(abjad.Accidental("ff"))
            'ff'

            >>> str(abjad.Accidental("tqf"))
            'tqf'

            >>> str(abjad.Accidental("f"))
            'f'

            >>> str(abjad.Accidental(""))
            ''

            >>> str(abjad.Accidental("qs"))
            'qs'

            >>> str(abjad.Accidental("s"))
            's'

            >>> str(abjad.Accidental("tqs"))
            'tqs'

            >>> str(abjad.Accidental("ss"))
            'ss'

        """
        if self.semitones in _accidental_semitones_to_abbreviation:
            return _accidental_semitones_to_abbreviation[self.semitones]
        character = "s"
        if self.semitones < 0:
            character = "f"
        semitones, remainder = divmod(abs(self.semitones), 1.0)
        abbreviation = character * int(semitones)
        if remainder:
            abbreviation += f"q{character}"
        return abbreviation

    def __sub__(self, argument):
        """
        Subtracts ``argument`` from accidental.

        ..  container:: example

            >>> accidental = abjad.Accidental("qs")

            >>> accidental - accidental
            Accidental(name='natural')

            >>> accidental - accidental - accidental
            Accidental(name='quarter flat')

        Returns new accidental.
        """
        if not isinstance(argument, type(self)):
            raise TypeError("can only subtract accidental from other accidental.")
        semitones = self.semitones - argument.semitones
        return type(self)(semitones)

    @staticmethod
    def _get_all_accidental_abbreviations(class_):
        return list(_accidental_abbreviation_to_symbol.keys())

    @staticmethod
    def _get_all_accidental_names(class_):
        return list(_accidental_name_to_abbreviation.keys())

    staticmethod

    def _get_all_accidental_semitone_values(class_):
        return list(_accidental_semitones_to_abbreviation.keys())

    def _get_lilypond_format(self):
        return self._abbreviation

    @classmethod
    def _is_abbreviation(class_, argument):
        if not isinstance(argument, str):
            return False
        return bool(_alphabetic_accidental_regex.match(argument))

    @classmethod
    def _is_symbol(class_, argument):
        if not isinstance(argument, str):
            return False
        return bool(_symbolic_accidental_regex.match(argument))

    @property
    def symbol(self) -> str:
        """
        Gets symbol of accidental.

        ..  container:: example

            >>> abjad.Accidental("ff").symbol
            'bb'

            >>> abjad.Accidental("tqf").symbol
            'tqf'

            >>> abjad.Accidental("f").symbol
            'b'

            >>> abjad.Accidental("").symbol
            ''

            >>> abjad.Accidental("qs").symbol
            'qs'

            >>> abjad.Accidental("s").symbol
            '#'

            >>> abjad.Accidental("tqs").symbol
            'tqs'

            >>> abjad.Accidental("ss").symbol
            '##'

        """
        abbreviation = _accidental_semitones_to_abbreviation[self.semitones]
        symbol = _accidental_abbreviation_to_symbol[abbreviation]
        return symbol


@dataclasses.dataclass(order=True, slots=True, unsafe_hash=True)
class Octave:
    """
    Octave.

    ..  container:: example:

        Initializes octave from integer:

        >>> abjad.Octave(4)
        Octave(number=4)

    ..  container:: example

        Initializes octave from named pitch:

        >>> abjad.Octave(abjad.NamedPitch("cs''"))
        Octave(number=5)

    ..  container:: example

        Initializes octave from other octave:

        >>> abjad.Octave(abjad.Octave(2))
        Octave(number=2)

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

    """

    number: int = 4

    def __post_init__(self):
        if isinstance(self.number, int | float):
            self.number = int(self.number)
        elif hasattr(self.number, "octave"):
            self.number = self.number.octave.number
        elif isinstance(self.number, type(self)):
            self.number = self.number.number
        else:
            raise Exception(f"must be number or string: {self.number!r}.")

    # TODO: remove
    def __float__(self):
        """
        Get octave number as float.

        Returns float.
        """
        return float(self.number)

    # TODO: remove
    def __int__(self):
        """
        Get octave number integer.

        Returns integer.
        """
        return int(self.number)

    def _is_tick_string(argument):
        if not isinstance(argument, str):
            return False
        return bool(_octave_tick_regex.match(argument))

    # TODO: replace with Octave.pitch that returns abjad.NamedPitch
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

    @classmethod
    def from_pitch(class_, pitch) -> "Octave":
        """
        Makes octave from ``pitch``.

        ..  container:: example

            >>> abjad.Octave.from_pitch("cs")
            Octave(number=3)

            >>> abjad.Octave.from_pitch("cs'")
            Octave(number=4)

            >>> abjad.Octave.from_pitch(1)
            Octave(number=4)

            >>> abjad.Octave.from_pitch(13)
            Octave(number=5)

        """
        if isinstance(pitch, int | float):
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
        return class_.from_ticks(ticks)

    @classmethod
    def from_ticks(class_, ticks: str) -> "Octave":
        """
        Makes octave from ``ticks`` string.

        ..  container:: example

            >>> abjad.Octave.from_ticks("'")
            Octave(number=4)

            >>> abjad.Octave.from_ticks(",,")
            Octave(number=1)

        """
        assert isinstance(ticks, str), repr(ticks)
        number = 3
        if ticks.startswith("'"):
            number += ticks.count("'")
        else:
            number -= ticks.count(",")
        return class_(number)


@functools.total_ordering
class IntervalClass:
    """
    Abstract interval-class.
    """

    __slots__ = ()

    _is_abstract = True

    def __init__(self, argument):
        if isinstance(argument, str):
            match = _interval_name_abbreviation_regex.match(argument)
            if match is None:
                try:
                    argument = float(argument)
                    self._from_number(argument)
                    return
                except ValueError:
                    message = (
                        f"can not initialize {type(self).__name__} from {argument!r}."
                    )
                    raise ValueError(message)
                message = f"can not initialize {type(self).__name__} from {argument!r}."
                raise ValueError(message)
            group_dict = match.groupdict()
            direction = group_dict["direction"]
            if direction == "-":
                direction = -1
            else:
                direction = 1
            quality = group_dict["quality"]
            diatonic_number = int(group_dict["number"])
            quality = self._validate_quality_and_diatonic_number(
                quality, diatonic_number
            )
            quartertone = group_dict["quartertone"]
            quality += quartertone
            self._from_named_parts(direction, quality, diatonic_number)
        elif isinstance(argument, tuple) and len(argument) == 2:
            quality, number = argument
            direction = _math.sign(number)
            diatonic_number = abs(number)
            quality = self._validate_quality_and_diatonic_number(
                quality, diatonic_number
            )
            self._from_named_parts(direction, quality, diatonic_number)
        elif isinstance(argument, numbers.Number):
            self._from_number(argument)
        elif isinstance(argument, Interval | IntervalClass):
            self._from_interval_or_interval_class(argument)
        else:
            message = f"can not initialize {type(self).__name__} from {argument!r}."
            raise ValueError(message)

    def __abs__(self):
        """
        Gets absolute value of interval-class.

        Returns new interval-class.
        """
        return type(self)(abs(self._number))

    def __eq__(self, argument) -> bool:
        """
        Compares ``number``.
        """
        if isinstance(argument, type(self)):
            return self.number == argument.number
        return False

    def __hash__(self) -> int:
        """
        Hashes interval-class.
        """
        return hash(self.__class__.__name__ + repr(self))

    def __lt__(self, argument) -> bool:
        """
        Compares ``number``.
        """
        assert isinstance(argument, type(self))
        return self.number < argument.number

    @staticmethod
    def _named_to_numbered(direction, quality, diatonic_number):
        octave_number = 0
        diatonic_pc_number = abs(diatonic_number)
        while diatonic_pc_number >= 8:
            diatonic_pc_number -= 7
            octave_number += 1
        quartertone = ""
        if quality.endswith(("+", "~")):
            quality, quartertone = quality[:-1], quality[-1]
        base_quality = quality
        if base_quality == "P" and octave_number and diatonic_pc_number == 1:
            return 12 * direction
        if len(quality) > 1:
            base_quality = quality[0]
        semitones = _diatonic_number_and_quality_to_semitones(
            diatonic_pc_number,
            base_quality,
        )
        if base_quality == "d":
            semitones -= len(quality) - 1
        elif base_quality == "A":
            semitones += len(quality) - 1
        if quartertone == "+":
            semitones += 0.5
        elif quartertone == "~":
            semitones -= 0.5
        if abs(diatonic_number) == 1:
            semitones = abs(semitones)
        while abs(semitones) > 12:
            semitones = (abs(semitones) - 12) * _math.sign(semitones)
        semitones *= direction
        return _math.integer_equivalent_number_to_integer(semitones)

    @classmethod
    def _numbered_to_named(cls, number):
        number = cls._to_nearest_quarter_tone(float(number))
        direction = _math.sign(number)
        octaves, semitones = divmod(abs(number), 12)
        if semitones == 0 and octaves:
            semitones = 12
        quartertone = ""
        if semitones % 1:
            semitones -= 0.5
            quartertone = "+"
        (
            quality,
            diatonic_pc_number,
        ) = _semitones_to_quality_and_diatonic_number[semitones]
        quality += quartertone
        diatonic_pc_number = cls._to_nearest_quarter_tone(diatonic_pc_number)
        return direction, quality, diatonic_pc_number

    @staticmethod
    def _to_nearest_quarter_tone(number):
        number = round(float(number) * 4) / 4
        div, mod = divmod(number, 1)
        if mod == 0.75:
            div += 1
        elif mod == 0.5:
            div += 0.5
        return _math.integer_equivalent_number_to_integer(div)

    @classmethod
    def _validate_quality_and_diatonic_number(cls, quality, diatonic_number):
        if quality in _quality_string_to_quality_abbreviation:
            quality = _quality_string_to_quality_abbreviation[quality]
        if quality == "aug":
            quality = "A"
        if quality == "dim":
            quality = "d"
        octaves = 0
        diatonic_pc_number = diatonic_number
        while diatonic_pc_number > 7:
            diatonic_pc_number -= 7
            octaves += 1
        quality_to_semitones = _diatonic_number_to_quality_dictionary[
            diatonic_pc_number
        ]
        if quality[0] not in quality_to_semitones:
            name = cls.__name__
            number = diatonic_number
            message = f"can not initialize {name} from {quality!r} and {number!r}."
            raise ValueError(message)
        return quality

    @property
    def number(self):
        """
        Gets number of interval-class.

        Returns number.
        """
        return self._number

    def transpose(self, pitch_carrier):
        """
        Transposes ``pitch_carrier`` by interval-class.

        Returns new pitch carrier.
        """
        if hasattr(pitch_carrier, "transpose"):
            return pitch_carrier.transpose(self)
        elif hasattr(pitch_carrier, "written_pitch"):
            new_note = copy.copy(pitch_carrier)
            new_pitch = pitch_carrier.written_pitch.transpose(self)
            new_note.written_pitch = new_pitch
            return new_note
        elif hasattr(pitch_carrier, "written_pitches"):
            new_chord = copy.copy(pitch_carrier)
            pairs = zip(new_chord.note_heads, pitch_carrier.note_heads)
            for new_nh, old_nh in pairs:
                new_pitch = old_nh.written_pitch.transpose(self)
                new_nh.written_pitch = new_pitch
            return new_chord
        return pitch_carrier


class NamedIntervalClass(IntervalClass):
    """
    Named interval-class.

    ..  container:: example

        Initializes from name:

        >>> abjad.NamedIntervalClass("-M9")
        NamedIntervalClass('-M2')

    """

    __slots__ = ("_number", "_quality")

    def __init__(self, name="P1"):
        super().__init__(name or "P1")

    def __abs__(self):
        """
        Gets absolute value of named interval-class.

        ..  container:: example

            >>> abs(abjad.NamedIntervalClass("-M9"))
            NamedIntervalClass('+M2')

        Returns new named interval-class.
        """
        return type(self)((self.quality, abs(self.number)))

    def __add__(self, argument):
        """
        Adds ``argument`` to named interval-class.

        Returns new named interval-class.
        """
        try:
            argument = type(self)(argument)
        except Exception:
            return NotImplemented
        dummy_pitch = NamedPitch(0)
        new_pitch = dummy_pitch + self + argument
        interval = NamedInterval.from_pitch_carriers(dummy_pitch, new_pitch)
        return type(self)(interval)

    def __eq__(self, argument):
        """
        Is true when ``argument`` is a named interval-class with direction
        number, quality string and number equal to those of this named
        interval-class.

        ..  container:: example

            >>> interval_class_1 = abjad.NamedIntervalClass("P1")
            >>> interval_class_2 = abjad.NamedIntervalClass("P1")
            >>> interval_class_3 = abjad.NamedIntervalClass("m2")

            >>> interval_class_1 == interval_class_1
            True
            >>> interval_class_1 == interval_class_2
            True
            >>> interval_class_1 == interval_class_3
            False

            >>> interval_class_2 == interval_class_1
            True
            >>> interval_class_2 == interval_class_2
            True
            >>> interval_class_2 == interval_class_3
            False

            >>> interval_class_3 == interval_class_1
            False
            >>> interval_class_3 == interval_class_2
            False
            >>> interval_class_3 == interval_class_3
            True

        Returns true or false.
        """
        return super().__eq__(argument)

    # TODO: remove
    def __float__(self):
        """
        Coerce to float.

        Returns float.
        """
        return float(
            self._named_to_numbered(
                self.direction_number, self._quality, abs(self._number)
            )
        )

    def __hash__(self):
        """
        Hashes named interval-class.

        Returns integer.
        """
        return super().__hash__()

    def __lt__(self, argument) -> bool:
        """
        Is true when ``argument`` is a named interval class with a number greater than
        that of this named interval.

        ..  container:: example

            >>> interval_class_1 = abjad.NamedIntervalClass("P1")
            >>> interval_class_2 = abjad.NamedIntervalClass("P1")
            >>> interval_class_3 = abjad.NamedIntervalClass("m2")

            >>> interval_class_1 < interval_class_1
            False
            >>> interval_class_1 < interval_class_2
            False
            >>> interval_class_1 < interval_class_3
            True

            >>> interval_class_2 < interval_class_1
            False
            >>> interval_class_2 < interval_class_2
            False
            >>> interval_class_2 < interval_class_3
            True

            >>> interval_class_3 < interval_class_1
            False
            >>> interval_class_3 < interval_class_2
            False
            >>> interval_class_3 < interval_class_3
            False

        """
        try:
            argument = type(self)(argument)
        except Exception:
            return False
        if self.number == argument.number:
            self_semitones = NamedInterval(self).semitones
            argument_semitones = NamedInterval(argument).semitones
            return self_semitones < argument_semitones
        return self.number < argument.number

    def __radd__(self, argument):
        """
        Adds interval-class to ``argument``

        Returns new named interval-class.
        """
        try:
            argument = type(self)(argument)
        except Exception:
            return NotImplemented
        return argument.__add__(self)

    def __repr__(self):
        """
        Gets repr.
        """
        return f"{type(self).__name__}({self.name!r})"

    def __sub__(self, argument):
        """
        Subtracts ``argument`` from named interval-class.

        Returns new named interval-class.
        """
        try:
            argument = type(self)(argument)
        except Exception:
            return NotImplemented
        dummy_pitch = NamedPitch(0)
        new_pitch = dummy_pitch + self - argument
        interval = NamedInterval.from_pitch_carriers(dummy_pitch, new_pitch)
        return type(self)(interval)

    def _from_interval_or_interval_class(self, argument):
        try:
            quality = argument.quality
            diatonic_number = abs(argument.number)
            direction = _math.sign(argument.number)
        except AttributeError:
            direction, quality, diatonic_number = self._numbered_to_named(argument)
        self._from_named_parts(direction, quality, diatonic_number)

    def _from_named_parts(self, direction, quality, diatonic_number):
        self._quality = quality
        diatonic_pc_number = diatonic_number
        while diatonic_pc_number > 7:
            diatonic_pc_number -= 7
        if diatonic_pc_number == 1 and diatonic_number >= 8:
            if quality == "P":
                diatonic_pc_number = 8
            elif quality.startswith("d") or quality == "P~":
                direction *= -1
        if not (diatonic_number == 1 and quality == "P"):
            diatonic_pc_number *= direction
        self._number = diatonic_pc_number

    def _from_number(self, argument):
        direction, quality, diatonic_number = self._numbered_to_named(argument)
        self._from_named_parts(direction, quality, diatonic_number)

    @property
    def direction_number(self):
        """
        Gets direction number of named interval-class.

        ..  container:: example

            >>> abjad.NamedIntervalClass("P1").direction_number
            0

            >>> abjad.NamedIntervalClass("+M2").direction_number
            1

            >>> abjad.NamedIntervalClass("-M2").direction_number
            -1

        Returns -1, 0 or 1.
        """
        if self.quality == "P" and abs(self.number) == 1:
            return 0
        return _math.sign(self.number)

    @property
    def name(self):
        """
        Gets name of named interval-class.

        ..  container:: example

            >>> abjad.NamedIntervalClass("-M9").name
            '-M2'

        Returns string.
        """
        return "{}{}{}".format(
            _direction_number_to_direction_symbol[self.direction_number],
            self._quality,
            abs(self.number),
        )

    @property
    def quality(self):
        """
        Gets quality of named interval-class.

        Returns string.
        """
        return self._quality

    @classmethod
    def from_pitch_carriers(class_, pitch_carrier_1, pitch_carrier_2):
        """
        Makes named interval-class from ``pitch_carrier_1`` and
        ``pitch_carrier_2``

        ..  container:: example

            >>> abjad.NamedIntervalClass.from_pitch_carriers(
            ...     abjad.NamedPitch(-2),
            ...     abjad.NamedPitch(12),
            ...     )
            NamedIntervalClass('+M2')

        ..  container:: example

            >>> abjad.NamedIntervalClass.from_pitch_carriers(
            ...     abjad.NamedPitch(0),
            ...     abjad.NamedPitch(12),
            ...     )
            NamedIntervalClass('+P8')

        ..  container:: example

            >>> abjad.NamedIntervalClass.from_pitch_carriers(
            ...     abjad.NamedPitch(12),
            ...     abjad.NamedPitch(12),
            ...     )
            NamedIntervalClass('P1')

        ..  container:: example

            >>> abjad.NamedIntervalClass.from_pitch_carriers(
            ...     abjad.NamedPitch(12),
            ...     abjad.NamedPitch(-3),
            ...     )
            NamedIntervalClass('-m3')

        ..  container:: example

            >>> abjad.NamedIntervalClass.from_pitch_carriers(
            ...     abjad.NamedPitch(12),
            ...     abjad.NamedPitch(9),
            ...     )
            NamedIntervalClass('-m3')

        Returns newly constructed named interval-class.
        """
        named_interval = NamedInterval.from_pitch_carriers(
            pitch_carrier_1, pitch_carrier_2
        )
        return class_(named_interval)


class NamedInversionEquivalentIntervalClass(NamedIntervalClass):
    """
    Named inversion-equivalent interval-class.

    ..  container:: example

        Initializes from string:

        >>> abjad.NamedInversionEquivalentIntervalClass("-m14")
        NamedInversionEquivalentIntervalClass('+M2')

    ..  container:: example

        Initializes from pair:

        >>> abjad.NamedInversionEquivalentIntervalClass(("perfect", 1))
        NamedInversionEquivalentIntervalClass('P1')

        >>> abjad.NamedInversionEquivalentIntervalClass(("perfect", -1))
        NamedInversionEquivalentIntervalClass('P1')

        >>> abjad.NamedInversionEquivalentIntervalClass(("augmented", 4))
        NamedInversionEquivalentIntervalClass('+A4')

        >>> abjad.NamedInversionEquivalentIntervalClass(("augmented", -4))
        NamedInversionEquivalentIntervalClass('+A4')

        >>> abjad.NamedInversionEquivalentIntervalClass(("augmented", 11))
        NamedInversionEquivalentIntervalClass('+A4')

        >>> abjad.NamedInversionEquivalentIntervalClass(("augmented", -11))
        NamedInversionEquivalentIntervalClass('+A4')

    ..  container:: example

        Initializes from other interval-class:

        >>> interval_class = abjad.NamedInversionEquivalentIntervalClass("P1")
        >>> abjad.NamedInversionEquivalentIntervalClass(interval_class)
        NamedInversionEquivalentIntervalClass('P1')

    """

    __slots__ = ()

    def __init__(self, name="P1"):
        super().__init__(name or "P1")
        self._quality, self._number = self._process_quality_and_number(
            self._quality, self._number
        )

    def __eq__(self, argument):
        """
        Compares ``name``.

        ..  container:: example

            >>> class_ = abjad.NamedInversionEquivalentIntervalClass
            >>> interval_class_1 = class_("P1")
            >>> interval_class_2 = class_("P1")
            >>> interval_class_3 = class_("m2")

            >>> interval_class_1 == interval_class_1
            True
            >>> interval_class_1 == interval_class_2
            True
            >>> interval_class_1 == interval_class_3
            False

            >>> interval_class_2 == interval_class_1
            True
            >>> interval_class_2 == interval_class_2
            True
            >>> interval_class_2 == interval_class_3
            False

            >>> interval_class_3 == interval_class_1
            False
            >>> interval_class_3 == interval_class_2
            False
            >>> interval_class_3 == interval_class_3
            True

        Returns true or false.
        """
        return super().__eq__(argument)

    def __hash__(self):
        """
        Hashes named inversion-equivalent interval-class.

        Returns integer.
        """
        return super().__hash__()

    @classmethod
    def _invert_quality_string(class_, quality):
        inversions = {"M": "m", "m": "M", "P": "P"}
        if quality in inversions:
            return inversions[quality]
        if quality[0] == "A":
            return "d" * len(quality)
        return "A" * len(quality)

    @classmethod
    def _is_representative_number(class_, argument):
        if isinstance(argument, numbers.Number):
            if 1 <= argument <= 4 or argument == 8:
                return True
        return False

    @classmethod
    def _process_quality_and_number(class_, quality, number):
        if number == 0:
            raise ValueError("named interval can not equal zero.")
        elif abs(number) == 1:
            number = 1
        elif abs(number) % 7 == 0:
            number = 7
        elif abs(number) % 7 == 1:
            number = 8
        else:
            number = abs(number) % 7
        if class_._is_representative_number(number):
            quality = quality
            number = number
        else:
            quality = class_._invert_quality_string(quality)
            number = 9 - number
        return quality, number

    @classmethod
    def from_pitch_carriers(class_, pitch_carrier_1, pitch_carrier_2):
        """
        Makes named inversion-equivalent interval-class from ``pitch_carrier_1`` and
        ``pitch_carrier_2``.

        ..  container:: example

            >>> class_ = abjad.NamedInversionEquivalentIntervalClass
            >>> class_.from_pitch_carriers(
            ...     abjad.NamedPitch(-2),
            ...     abjad.NamedPitch(12),
            ...     )
            NamedInversionEquivalentIntervalClass('+M2')

        Returns new named inversion-equivalent interval-class.
        """
        named_interval = NamedInterval.from_pitch_carriers(
            pitch_carrier_1, pitch_carrier_2
        )
        string = named_interval.name
        return class_(string)


class NumberedIntervalClass(IntervalClass):
    """
    Numbered interval-class.

    ..  container:: example

        Initializes from integer:

        >>> abjad.NumberedIntervalClass(-14)
        NumberedIntervalClass(-2)

    ..  container:: example

        Initializes from float:

        >>> abjad.NumberedIntervalClass(-14.5)
        NumberedIntervalClass(-2.5)

    ..  container:: example

        Initializes from string:

        >>> abjad.NumberedIntervalClass("-14.5")
        NumberedIntervalClass(-2.5)

        >>> abjad.NumberedIntervalClass("P8")
        NumberedIntervalClass(12)

        >>> abjad.NumberedIntervalClass("-P8")
        NumberedIntervalClass(-12)

    """

    __slots__ = ("_number",)

    def __init__(self, number=0):
        super().__init__(number or 0)

    def __abs__(self):
        """
        Gets absolute value of numbered interval-class.

        Returns new numbered interval-class.
        """
        return type(self)(abs(self.number))

    def __add__(self, argument):
        """
        Adds ``argument`` to numbered interval-class.

        Returns new numbered interval-class.
        """
        try:
            argument = type(self)(argument)
        except Exception:
            return NotImplemented
        return type(self)(float(self) + float(argument))

    def __eq__(self, argument) -> bool:
        """
        Compares ``number``.

        ..  container:: example

            >>> interval_class_1 = abjad.NumberedIntervalClass(0)
            >>> interval_class_2 = abjad.NumberedIntervalClass(0)
            >>> interval_class_3 = abjad.NumberedIntervalClass(1)

            >>> interval_class_1 == interval_class_1
            True
            >>> interval_class_1 == interval_class_2
            True
            >>> interval_class_1 == interval_class_3
            False

            >>> interval_class_2 == interval_class_1
            True
            >>> interval_class_2 == interval_class_2
            True
            >>> interval_class_2 == interval_class_3
            False

            >>> interval_class_3 == interval_class_1
            False
            >>> interval_class_3 == interval_class_2
            False
            >>> interval_class_3 == interval_class_3
            True

        """
        return super().__eq__(argument)

    # TODO: remove
    def __float__(self):
        """
        Coerce to semitones as float.

        Returns float.
        """
        return float(self._number)

    def __hash__(self):
        """
        Hashes numbered interval-class.

        Returns integer.
        """
        return super().__hash__()

    def __lt__(self, argument):
        """
        Compares ``number``.

        ..  container:: example

            >>> interval_class_1 = abjad.NumberedIntervalClass(0)
            >>> interval_class_2 = abjad.NumberedIntervalClass(0)
            >>> interval_class_3 = abjad.NumberedIntervalClass(1)

            >>> interval_class_1 < interval_class_1
            False
            >>> interval_class_1 < interval_class_2
            False
            >>> interval_class_1 < interval_class_3
            True

            >>> interval_class_2 < interval_class_1
            False
            >>> interval_class_2 < interval_class_2
            False
            >>> interval_class_2 < interval_class_3
            True

            >>> interval_class_3 < interval_class_1
            False
            >>> interval_class_3 < interval_class_2
            False
            >>> interval_class_3 < interval_class_3
            False

        Returns true or false.
        """
        try:
            argument = type(self)(argument)
        except Exception:
            return False
        return self.number < argument.number

    def __radd__(self, argument):
        """
        Adds ``argument`` to numbered interval-class.

        Returns new numbered interval-class.
        """
        try:
            argument = type(self)(argument)
        except Exception:
            return NotImplemented
        return type(self)(float(self) + float(argument))

    def __repr__(self):
        """
        Gets repr.
        """
        return f"{type(self).__name__}({self.number!r})"

    def __sub__(self, argument):
        """
        Subtracts ``argument`` from numbered interval-class.

        Returns new numbered interval-class.
        """
        try:
            argument = type(self)(argument)
        except Exception:
            return NotImplemented
        return type(self)(float(self) - float(argument))

    def _from_interval_or_interval_class(self, argument):
        self._from_number(float(argument))

    def _from_named_parts(self, direction, quality, diatonic_number):
        self._number = self._named_to_numbered(direction, quality, diatonic_number)

    def _from_number(self, argument):
        direction = _math.sign(argument)
        number = self._to_nearest_quarter_tone(abs(argument))
        pc_number = number % 12
        if pc_number == 0 and number:
            pc_number = 12
        self._number = pc_number * direction

    @property
    def direction_number(self) -> int:
        """
        Gets direction number of numbered interval-class.

        Returns -1, 0 or 1.
        """
        if self.number < 1:
            return -1
        elif self.number == 1:
            return 0
        else:
            return 1

    @property
    def signed_string(self):
        """
        Gets signed string.
        """
        direction_symbol = _direction_number_to_direction_symbol[
            _math.sign(self.number)
        ]
        return f"{direction_symbol}{abs(self.number)}"

    @classmethod
    def from_pitch_carriers(
        class_, pitch_carrier_1, pitch_carrier_2
    ) -> "NumberedIntervalClass":
        """
        Makes numbered interval-class from ``pitch_carrier_1`` and ``pitch_carrier_2``

        ..  container:: example

            >>> abjad.NumberedIntervalClass.from_pitch_carriers(
            ...     abjad.NamedPitch(-2),
            ...     abjad.NamedPitch(12),
            ...     )
            NumberedIntervalClass(2)

            >>> abjad.NumberedIntervalClass.from_pitch_carriers(
            ...     abjad.NamedPitch(0),
            ...     abjad.NamedPitch(12),
            ...     )
            NumberedIntervalClass(12)

            >>> abjad.NumberedIntervalClass.from_pitch_carriers(
            ...     abjad.NamedPitch(9),
            ...     abjad.NamedPitch(12),
            ...     )
            NumberedIntervalClass(3)

            >>> abjad.NumberedIntervalClass.from_pitch_carriers(
            ...     abjad.NamedPitch(12),
            ...     abjad.NamedPitch(9),
            ...     )
            NumberedIntervalClass(-3)

            >>> abjad.NumberedIntervalClass.from_pitch_carriers(
            ...     abjad.NamedPitch(12),
            ...     abjad.NamedPitch(12),
            ...     )
            NumberedIntervalClass(0)

            >>> abjad.NumberedIntervalClass.from_pitch_carriers(
            ...     abjad.NamedPitch(24),
            ...     abjad.NamedPitch(0),
            ...     )
            NumberedIntervalClass(-12)

            >>> abjad.NumberedIntervalClass.from_pitch_carriers(
            ...     abjad.NamedPitch(12),
            ...     abjad.NamedPitch(-2),
            ...     )
            NumberedIntervalClass(-2)

        Returns numbered interval-class.
        """
        interval = NumberedInterval.from_pitch_carriers(
            pitch_carrier_1, pitch_carrier_2
        )
        return class_(interval)


class NumberedInversionEquivalentIntervalClass(NumberedIntervalClass):
    """
    Numbered inversion-equivalent interval-class.

    ..  container:: example

        Initializes from integer:

        >>> abjad.NumberedInversionEquivalentIntervalClass(0)
        NumberedInversionEquivalentIntervalClass(0)

        >>> abjad.NumberedInversionEquivalentIntervalClass(1)
        NumberedInversionEquivalentIntervalClass(1)

    ..  container:: example

        Initializes from float:

        >>> abjad.NumberedInversionEquivalentIntervalClass(1.5)
        NumberedInversionEquivalentIntervalClass(1.5)

    ..  container:: example

        Initializes from string:

        >>> abjad.NumberedInversionEquivalentIntervalClass("1")
        NumberedInversionEquivalentIntervalClass(1)

    """

    __slots__ = ()

    def __init__(self, number=0):
        super().__init__(number or 0)
        self._number %= 12
        if 6 < self._number:
            self._number = 12 - self._number

    def __abs__(self):
        """
        Gets absolute value of numbered inversion-equivalent
        interval-class.

        ..  container:: example

            >>> abs(abjad.NumberedInversionEquivalentIntervalClass(0))
            NumberedInversionEquivalentIntervalClass(0)

            >>> abs(abjad.NumberedInversionEquivalentIntervalClass(1.5))
            NumberedInversionEquivalentIntervalClass(1.5)

        Returns new numbered inversion-equivalent interval-class.
        """
        return type(self)(abs(self.number))

    def __lt__(self, argument):
        """
        Compares ``number``.
        """
        if isinstance(argument, type(self)):
            return self.number < argument.number
        return False

    def __neg__(self):
        """
        Negates numbered inversion-equivalent interval-class.

        ..  container:: example

            >>> -abjad.NumberedInversionEquivalentIntervalClass(0)
            NumberedInversionEquivalentIntervalClass(0)

            >>> -abjad.NumberedInversionEquivalentIntervalClass(1.5)
            NumberedInversionEquivalentIntervalClass(1.5)

        Returns new numbered inversion-equivalent interval-class.
        """
        return type(self)(self.number)

    def __repr__(self):
        """
        Gets repr.
        """
        return f"{type(self).__name__}({self.number!r})"


@functools.total_ordering
class Interval:
    """
    Abstract interval.
    """

    __slots__ = ("_interval_class", "_octaves")

    _is_abstract = True

    def __init__(self, argument):
        if isinstance(argument, str):
            match = _interval_name_abbreviation_regex.match(argument)
            if match is None:
                try:
                    argument = float(argument)
                    self._from_number(argument)
                    return
                except ValueError:
                    class_name = type(self).__name__
                    message = f"can not initialize {class_name} from {argument!r}."
                    raise ValueError(message)
                class_name = type(self).__name__
                message = f"can not initialize {class_name} from {argument!r}."
                raise ValueError(message)
            group_dict = match.groupdict()
            direction = group_dict["direction"]
            if direction == "-":
                direction = -1
            else:
                direction = 1
            quality = group_dict["quality"]
            diatonic_number = int(group_dict["number"])
            quality = self._validate_quality_and_diatonic_number(
                quality, diatonic_number
            )
            quartertone = group_dict["quartertone"]
            quality += quartertone
            self._from_named_parts(direction, quality, diatonic_number)
        elif isinstance(argument, tuple) and len(argument) == 2:
            quality, number = argument
            direction = _math.sign(number)
            diatonic_number = abs(number)
            quality = self._validate_quality_and_diatonic_number(
                quality, diatonic_number
            )
            self._from_named_parts(direction, quality, diatonic_number)
        elif isinstance(argument, numbers.Number):
            self._from_number(argument)
        else:
            self._from_interval_or_interval_class(argument)

    def __eq__(self, argument) -> bool:
        """
        Compares repr formats.
        """
        if isinstance(argument, type(self)):
            return repr(self) == repr(argument)
        return False

    def __hash__(self) -> int:
        """
        Hashes interval.
        """
        return hash(self.__class__.__name__ + repr(self))

    def __lt__(self, argument):
        """
        Is true when interval is less than ``argument``

        Returns true or false.
        """
        raise NotImplementedError

    def _from_interval_or_interval_class(self, argument):
        raise NotImplementedError

    def _from_named_parts(self, direction, quality, diatonic_number):
        raise NotImplementedError

    def _from_number(self, argument):
        raise NotImplementedError

    @staticmethod
    def _named_to_numbered(direction, quality, diatonic_number):
        octave_number = 0
        diatonic_pc_number = abs(diatonic_number)
        while diatonic_pc_number >= 8:
            diatonic_pc_number -= 7
            octave_number += 1
        quartertone = ""
        if quality.endswith(("+", "~")):
            quality, quartertone = quality[:-1], quality[-1]
        base_quality = quality
        if len(quality) > 1:
            base_quality = quality[0]
        semitones = _diatonic_number_and_quality_to_semitones(
            diatonic_pc_number, base_quality
        )
        if base_quality == "d":
            semitones -= len(quality) - 1
        elif base_quality == "A":
            semitones += len(quality) - 1
        if quartertone == "+":
            semitones += 0.5
        elif quartertone == "~":
            semitones -= 0.5
        if abs(diatonic_number) == 1:
            semitones = abs(semitones)
        else:
            semitones += octave_number * 12
        semitones *= direction
        return _math.integer_equivalent_number_to_integer(semitones)

    @classmethod
    def _numbered_to_named(cls, number):
        number = cls._to_nearest_quarter_tone(float(number))
        direction = _math.sign(number)
        octaves, semitones = divmod(abs(number), 12)
        quartertone = ""
        if semitones % 1:
            semitones -= 0.5
            quartertone = "+"
        (
            quality,
            diatonic_number,
        ) = _semitones_to_quality_and_diatonic_number[semitones]
        quality += quartertone
        diatonic_number += octaves * 7
        diatonic_number = cls._to_nearest_quarter_tone(diatonic_number)
        return direction, quality, diatonic_number

    @staticmethod
    def _to_nearest_quarter_tone(number):
        number = round(float(number) * 4) / 4
        div, mod = divmod(number, 1)
        if mod == 0.75:
            div += 1
        elif mod == 0.5:
            div += 0.5
        return _math.integer_equivalent_number_to_integer(div)

    @classmethod
    def _validate_quality_and_diatonic_number(cls, quality, diatonic_number):
        if quality in _quality_string_to_quality_abbreviation:
            quality = _quality_string_to_quality_abbreviation[quality]
        if quality == "aug":
            quality = "A"
        if quality == "dim":
            quality = "d"
        octaves = 0
        diatonic_pc_number = diatonic_number
        while diatonic_pc_number > 7:
            diatonic_pc_number -= 7
            octaves += 1
        quality_to_semitones = _diatonic_number_to_quality_dictionary[
            diatonic_pc_number
        ]
        if quality[0] not in quality_to_semitones:
            name = cls.__name__
            number = diatonic_number
            message = f"can not initialize {name} from {quality!r} and {number!r}."
            raise ValueError(message)
        return quality

    @property
    def cents(self):
        """
        Gets cents of interval.

        Returns nonnegative number.
        """
        return 100 * self.semitones

    @property
    def direction_number(self):
        """
        Gets direction number of interval

        Returns integer.
        """
        raise NotImplementedError

    @property
    def interval_class(self):
        """
        Gets interval-class of interval.

        Returns interval-class.
        """
        raise NotImplementedError

    @property
    def number(self):
        """
        Gets number of interval.

        Returns integer.
        """
        raise NotImplementedError

    @property
    def octaves(self):
        """
        Gets octaves of interval.

        Returns nonnegative number.
        """
        raise NotImplementedError

    @property
    def semitones(self):
        """
        Gets semitones of interval.

        Returns integer or float.
        """
        raise NotImplementedError

    def transpose(self, pitch_carrier):
        """
        Transposes ``pitch_carrier`` by interval.

        Returns new pitch carrier.
        """
        if hasattr(pitch_carrier, "transpose"):
            return pitch_carrier.transpose(self)
        elif hasattr(pitch_carrier, "written_pitch"):
            new_note = copy.copy(pitch_carrier)
            new_pitch = pitch_carrier.written_pitch.transpose(self)
            new_note.written_pitch = new_pitch
            return new_note
        elif hasattr(pitch_carrier, "written_pitches"):
            new_chord = copy.copy(pitch_carrier)
            pairs = zip(new_chord.note_heads, pitch_carrier.note_heads)
            for new_nh, old_nh in pairs:
                new_pitch = old_nh.written_pitch.transpose(self)
                new_nh.written_pitch = new_pitch
            return new_chord
        return pitch_carrier


class NamedInterval(Interval):
    """
    Named interval.

    ..  container:: example

        Initializes ascending major ninth from string:

        >>> abjad.NamedInterval("+M9")
        NamedInterval('+M9')

    ..  container:: example

        Initializes descending major third from number of semitones:

        >>> abjad.NamedInterval(-4)
        NamedInterval('-M3')

    ..  container:: example

        Initializes from other named interval:

        >>> abjad.NamedInterval(abjad.NamedInterval(-4))
        NamedInterval('-M3')

    ..  container:: example

        Initializes from numbered interval:

        >>> abjad.NamedInterval(abjad.NumberedInterval(3))
        NamedInterval('+m3')

    ..  container:: example

        Initializes from pair of quality and diatonic number:

        >>> abjad.NamedInterval(("M", 3))
        NamedInterval('+M3')

    """

    __slots__ = ()

    def __init__(self, name="P1"):
        super().__init__(name or "P1")

    def __abs__(self) -> "NamedInterval":
        """
        Gets absolute value of named interval.

        ..  container:: example

            >>> abs(abjad.NamedInterval("+M9"))
            NamedInterval('+M9')

            >>> abs(abjad.NamedInterval("-M9"))
            NamedInterval('+M9')

        """
        return type(self)((self.quality, abs(self.number)))

    def __add__(self, argument) -> "NamedInterval":
        """
        Adds ``argument`` to named interval.

        ..  container:: example

            >>> abjad.NamedInterval("M9") + abjad.NamedInterval("M2")
            NamedInterval('+M10')

        """
        try:
            argument = type(self)(argument)
        except Exception:
            return NotImplemented
        dummy_pitch = NamedPitch(0)
        new_pitch = dummy_pitch + self + argument
        return NamedInterval.from_pitch_carriers(dummy_pitch, new_pitch)

    def __copy__(self, *arguments) -> "NamedInterval":
        """
        Copies named interval.

        >>> import copy

        ..  container:: example

            >>> copy.copy(abjad.NamedInterval("+M9"))
            NamedInterval('+M9')

        """
        return type(self)((self.quality, self.number))

    def __eq__(self, argument) -> bool:
        """
        Compares ``name``.

        ..  container:: example

            >>> interval_1 = abjad.NamedInterval("m2")
            >>> interval_2 = abjad.NamedInterval("m2")
            >>> interval_3 = abjad.NamedInterval("m9")

            >>> interval_1 == interval_1
            True
            >>> interval_1 == interval_2
            True
            >>> interval_1 == interval_3
            False

            >>> interval_2 == interval_1
            True
            >>> interval_2 == interval_2
            True
            >>> interval_2 == interval_3
            False

            >>> interval_3 == interval_1
            False
            >>> interval_3 == interval_2
            False
            >>> interval_3 == interval_3
            True

        """
        if isinstance(argument, type(self)):
            return self.name == argument.name
        return False

    # TODO: remove
    def __float__(self):
        """
        Coerce to semitones as float.

        Returns float.
        """
        return float(self.semitones)

    def __hash__(self):
        """
        Hashes named interval.

        Returns number.
        """
        return super().__hash__()

    def __lt__(self, argument) -> bool:
        """
        Compares ``semitones``.

        ..  container:: example

            >>> abjad.NamedInterval("+M9") < abjad.NamedInterval("+M10")
            True

            >>> abjad.NamedInterval("+m9") < abjad.NamedInterval("+M9")
            True

            >>> abjad.NamedInterval("+M9") < abjad.NamedInterval("+M2")
            False

        """
        if isinstance(argument, type(self)):
            return self.semitones < argument.semitones
        return False

    def __mul__(self, argument) -> "NamedInterval":
        """
        Multiplies named interval by ``argument``

        ..  container:: example

            >>> 3 * abjad.NamedInterval("+M9")
            NamedInterval('+A25')

        """
        if not isinstance(argument, int):
            raise TypeError(f"must be integer: {argument!r}.")
        dummy_pitch = NamedPitch(0)
        for i in range(abs(argument)):
            dummy_pitch += self
        result = NamedInterval.from_pitch_carriers(NamedPitch(0), dummy_pitch)
        if argument < 0:
            return -result
        return result

    def __neg__(self) -> "NamedInterval":
        """
        Negates named interval.

        ..  container:: example

            >>> -abjad.NamedInterval("+M9")
            NamedInterval('-M9')

            >>> -abjad.NamedInterval("-M9")
            NamedInterval('+M9')

        """
        return type(self)((self.quality, -self.number))

    def __radd__(self, argument) -> "NamedInterval":
        """
        Adds named interval to ``argument``

        ..  container:: example

            >>> abjad.NamedInterval("M9") + abjad.NamedInterval("M2")
            NamedInterval('+M10')

        """
        try:
            argument = type(self)(argument)
        except Exception:
            return NotImplemented
        return argument.__add__(self)

    def __repr__(self):
        """
        Gets repr.
        """
        return f"{type(self).__name__}({self.name!r})"

    def __rmul__(self, argument) -> "NamedInterval":
        """
        Multiplies ``argument`` by named interval.

        ..  container:: example

            >>> abjad.NamedInterval("+M9") * 3
            NamedInterval('+A25')

        """
        return self * argument

    def __sub__(self, argument) -> "NamedInterval":
        """
        Subtracts ``argument`` from named interval.

        ..  container:: example

            >>> abjad.NamedInterval("+M9") - abjad.NamedInterval("+M2")
            NamedInterval('+P8')

            >>> abjad.NamedInterval("+M2") - abjad.NamedInterval("+M9")
            NamedInterval('-P8')

        """
        try:
            argument = type(self)(argument)
        except Exception:
            return NotImplemented
        dummy_pitch = NamedPitch(0)
        new_pitch = dummy_pitch + self - argument
        return NamedInterval.from_pitch_carriers(dummy_pitch, new_pitch)

    def _from_interval_or_interval_class(self, argument):
        try:
            quality = argument.quality
            diatonic_number = abs(argument.number)
            direction = _math.sign(argument.number)
        except AttributeError:
            direction, quality, diatonic_number = self._numbered_to_named(argument)
        self._from_named_parts(direction, quality, diatonic_number)

    def _from_named_parts(self, direction, quality, diatonic_number):
        octaves = 0
        diatonic_pc_number = abs(diatonic_number)
        while diatonic_pc_number > 7:
            octaves += 1
            diatonic_pc_number -= 7
        if diatonic_pc_number == 1 and quality == "P" and diatonic_number >= 8:
            octaves -= 1
            diatonic_pc_number = 8
        self._octaves = octaves
        if direction:
            diatonic_pc_number *= direction
        self._interval_class = NamedIntervalClass((quality, diatonic_pc_number))

    def _from_number(self, argument):
        direction, quality, diatonic_number = self._numbered_to_named(argument)
        self._from_named_parts(direction, quality, diatonic_number)

    @property
    def direction_number(self) -> int:
        """
        Gets direction number of named interval.

        ..  container:: example

            >>> abjad.NamedInterval("+M9").direction_number
            1

            >>> abjad.NamedInterval("+dim2").direction_number
            1

            >>> abjad.NamedInterval("+A1").direction_number
            1

            >>> abjad.NamedInterval("P1").direction_number
            0

            >>> abjad.NamedInterval("-m3").direction_number
            -1

        """
        if self.quality == "P" and abs(self.number) == 1:
            return 0
        return _math.sign(self.number)

    @property
    def interval_class(self) -> "NamedIntervalClass":
        """
        Gets named interval class.

        ..  container:: example

            >>> abjad.NamedInterval("+M9").interval_class
            NamedIntervalClass('+M2')

            >>> abjad.NamedInterval("-M9").interval_class
            NamedIntervalClass('-M2')

            >>> abjad.NamedInterval("P1").interval_class
            NamedIntervalClass('P1')

            >>> abjad.NamedInterval("+P8").interval_class
            NamedIntervalClass('+P8')

        """
        return self._interval_class

    @property
    def name(self) -> str:
        """
        Gets name of named interval.

        ..  container:: example

            >>> abjad.NamedInterval("+M9").name
            '+M9'

        """
        direction_symbol = _direction_number_to_direction_symbol[self.direction_number]
        return "{}{}{}".format(
            direction_symbol, self._interval_class.quality, abs(self.number)
        )

    @property
    def number(self) -> int | float:
        """
        Gets number of named interval.

        ..  container:: example

            >>> abjad.NamedInterval("+M9").number
            9

        """
        number = self._interval_class._number
        direction = _math.sign(number)
        number = abs(number) + (7 * self.octaves)
        return number * direction

    @property
    def octaves(self) -> int:
        """
        Gets octaves of interval.
        """
        return self._octaves

    @property
    def quality(self) -> str:
        """
        Gets quality of named interval.
        """
        return self._interval_class.quality

    @property
    def semitones(self) -> int:
        """
        Gets semitones of named interval.

        ..  container:: example

            >>> abjad.NamedInterval("+M9").semitones
            14

            >>> abjad.NamedInterval("-M9").semitones
            -14

            >>> abjad.NamedInterval("P1").semitones
            0

            >>> abjad.NamedInterval("+P8").semitones
            12

            >>> abjad.NamedInterval("-P8").semitones
            -12

        """
        direction = self.direction_number
        diatonic_number = abs(self._interval_class._number)
        quality = self._validate_quality_and_diatonic_number(
            self.quality, diatonic_number
        )
        diatonic_number += 7 * self._octaves
        return self._named_to_numbered(direction, quality, diatonic_number)

    @property
    def staff_spaces(self) -> float | int:
        """
        Gets staff spaces of named interval.

        ..  container:: example

            >>> abjad.NamedInterval("+M9").staff_spaces
            8

            >>> abjad.NamedInterval("-M9").staff_spaces
            -8

            >>> abjad.NamedInterval("P1").staff_spaces
            0

            >>> abjad.NamedInterval("+P8").staff_spaces
            7

            >>> abjad.NamedInterval("-P8").staff_spaces
            -7

        """
        if self.direction_number == -1:
            return self.number + 1
        elif not self.direction_number:
            return 0
        else:
            assert self.direction_number == 1
            return self.number - 1

    @classmethod
    def from_pitch_carriers(
        class_, pitch_carrier_1, pitch_carrier_2
    ) -> "NamedInterval":
        """
        Makes named interval calculated from ``pitch_carrier_1`` to ``pitch_carrier_2``.

        ..  container:: example

            >>> abjad.NamedInterval.from_pitch_carriers(
            ...     abjad.NamedPitch(-2),
            ...     abjad.NamedPitch(12),
            ...     )
            NamedInterval('+M9')

            >>> abjad.NamedInterval.from_pitch_carriers(
            ...     abjad.NamedPitch("css'"),
            ...     abjad.NamedPitch("cff'"),
            ...     )
            NamedInterval('-AAAA1')

            >>> abjad.NamedInterval.from_pitch_carriers(
            ...     abjad.NamedPitch("ds'"),
            ...     abjad.NamedPitch("ef''"),
            ...     )
            NamedInterval('+d9')

            >>> abjad.NamedInterval.from_pitch_carriers("c'", "cs'''")
            NamedInterval('+A15')

            >>> abjad.NamedInterval.from_pitch_carriers("c", "cqs")
            NamedInterval('+P+1')

            >>> abjad.NamedInterval.from_pitch_carriers("cf'", "bs")
            NamedInterval('-dd2')

            >>> abjad.NamedInterval.from_pitch_carriers("cff'", "aqs")
            NamedInterval('-ddd+3')

            >>> abjad.NamedInterval.from_pitch_carriers("cff'", "atqs")
            NamedInterval('-dddd+3')

            >>> abjad.NamedInterval.from_pitch_carriers("c'", "d''")
            NamedInterval('+M9')

            >>> abjad.NamedInterval.from_pitch_carriers("c'", "df''")
            NamedInterval('+m9')

            >>> abjad.NamedInterval.from_pitch_carriers("c'", "dff''")
            NamedInterval('+d9')

            >>> abjad.NamedInterval.from_pitch_carriers("c'", "dfff''")
            NamedInterval('+dd9')

            >>> abjad.NamedInterval.from_pitch_carriers("c'", "dffff''")
            NamedInterval('+ddd9')

        """
        pitch_1 = NamedPitch(pitch_carrier_1)
        pitch_2 = NamedPitch(pitch_carrier_2)
        degree_1 = pitch_1._get_diatonic_pitch_number()
        degree_2 = pitch_2._get_diatonic_pitch_number()
        named_sign = _math.sign(degree_1 - degree_2)
        named_i_number = abs(degree_1 - degree_2) + 1
        numbered_sign = _math.sign(
            float(NumberedPitch(pitch_1)) - float(NumberedPitch(pitch_2))
        )
        numbered_i_number = abs(
            float(NumberedPitch(pitch_1)) - float(NumberedPitch(pitch_2))
        )
        (
            octaves,
            named_ic_number,
        ) = _diatonic_number_to_octaves_and_diatonic_remainder(named_i_number)
        numbered_ic_number = numbered_i_number - 12 * octaves
        # multiply-diminished intervals can have opposite signs
        if named_sign and (named_sign == -numbered_sign):
            numbered_ic_number *= -1
        quartertone = ""
        if numbered_ic_number % 1:
            quartertone = "+"
            numbered_ic_number -= 0.5
        quality_to_semitones = _diatonic_number_to_quality_dictionary[named_ic_number]
        semitones_to_quality: dict = {
            value: key for key, value in quality_to_semitones.items()
        }
        quality = ""
        while numbered_ic_number > max(semitones_to_quality):
            numbered_ic_number -= 1
            quality += "A"
        while numbered_ic_number < min(semitones_to_quality):
            numbered_ic_number += 1
            quality += "d"
        quality += semitones_to_quality[numbered_ic_number]
        quality += quartertone
        direction = 1
        if pitch_2 < pitch_1:
            direction = -1
        return class_((quality, named_i_number * direction))

    def transpose(self, pitch_carrier):
        """
        Transposes ``pitch_carrier`` by named interval.

        ..  container:: example

            Transposes chord:

            >>> chord = abjad.Chord("<c' e' g'>4")

            >>> interval = abjad.NamedInterval("+m2")
            >>> interval.transpose(chord)
            Chord("<df' f' af'>4")

        Returns new (copied) object of ``pitch_carrier`` type.
        """
        return super().transpose(pitch_carrier)


class NumberedInterval(Interval):
    """
    Numbered interval.

    ..  container:: example

        Initializes from number of semitones:

        >>> abjad.NumberedInterval(-14)
        NumberedInterval(-14)

        Initializes from other numbered interval:

        >>> abjad.NumberedInterval(abjad.NumberedInterval(-14))
        NumberedInterval(-14)

        Initializes from named interval:

        >>> abjad.NumberedInterval(abjad.NamedInterval("-P4"))
        NumberedInterval(-5)

        Initializes from interval string:

        >>> abjad.NumberedInterval("-P4")
        NumberedInterval(-5)

    """

    __slots__ = ()

    def __init__(self, number=0):
        super().__init__(number or 0)

    def __abs__(self) -> "NumberedInterval":
        """
        Absolute value of numbered interval.

        ..  container:: example

            >>> abs(abjad.NumberedInterval(-14))
            NumberedInterval(14)

        """
        return type(self)(abs(self.number))

    def __add__(self, argument) -> "NumberedInterval":
        """
        Adds ``argument`` to numbered interval.

        ..  container:: example

            >>> abjad.NumberedInterval(3) + abjad.NumberedInterval(14)
            NumberedInterval(17)

            >>> abjad.NumberedInterval(3) + abjad.NumberedInterval(-14)
            NumberedInterval(-11)

        """
        try:
            argument = type(self)(argument)
        except Exception:
            return NotImplemented
        return type(self)(float(self) + float(argument))

    def __copy__(self) -> "NumberedInterval":
        """
        Copies numbered interval.

        >>> import copy

        ..  container:: example

            >>> copy.copy(abjad.NumberedInterval(-14))
            NumberedInterval(-14)

        """
        return type(self)(self.number)

    def __eq__(self, argument) -> bool:
        """
        Compares ``number``.

        ..  container:: example

            >>> interval_1 = abjad.NumberedInterval(12)
            >>> interval_2 = abjad.NumberedInterval(12)
            >>> interval_3 = abjad.NumberedInterval(13)

            >>> interval_1 == interval_1
            True
            >>> interval_1 == interval_2
            True
            >>> interval_1 == interval_3
            False

            >>> interval_2 == interval_1
            True
            >>> interval_2 == interval_2
            True
            >>> interval_2 == interval_3
            False

            >>> interval_3 == interval_1
            False
            >>> interval_3 == interval_2
            False
            >>> interval_3 == interval_3
            True

        """
        if isinstance(argument, type(self)):
            return self.number == argument.number
        return False

    # TODO: remove
    def __float__(self):
        """
        Coerce to float.

        Returns float.
        """
        return float(self.number)

    def __hash__(self):
        """
        Hashes numbered interval.

        Returns integer.
        """
        return super().__hash__()

    def __lt__(self, argument) -> bool:
        """
        Is true when ``argument`` is a numbered interval with same direction number as
        this numbered interval and with number greater than that of this numbered
        interval.

        ..  container:: example

            >>> interval_1 = abjad.NumberedInterval(12)
            >>> interval_2 = abjad.NumberedInterval(12)
            >>> interval_3 = abjad.NumberedInterval(13)

            >>> interval_1 < interval_1
            False

            >>> interval_1 < interval_2
            False

            >>> interval_1 < interval_3
            True

            >>> interval_2 < interval_1
            False

            >>> interval_2 < interval_2
            False

            >>> interval_2 < interval_3
            True

            >>> interval_3 < interval_1
            False

            >>> interval_3 < interval_2
            False

            >>> interval_3 < interval_3
            False

        Returns true or false.
        """
        if isinstance(argument, type(self)):
            return self.number < argument.number
        return False

    def __neg__(self) -> "NumberedInterval":
        """
        Negates numbered interval.

        ..  container:: example

            >>> -abjad.NumberedInterval(-14)
            NumberedInterval(14)

        """
        return type(self)(-self.number)

    def __radd__(self, argument) -> "NumberedInterval":
        """
        Adds numbered interval to ``argument``

        ..  container:: example

            >>> interval = abjad.NumberedInterval(14)
            >>> abjad.NumberedInterval(3).__radd__(interval)
            NumberedInterval(17)

            >>> interval = abjad.NumberedInterval(-14)
            >>> abjad.NumberedInterval(3).__radd__(interval)
            NumberedInterval(-11)

        """
        try:
            argument = type(self)(argument)
        except Exception:
            return NotImplemented
        return type(self)(float(self) + float(argument))

    def __repr__(self):
        """
        Gets repr.
        """
        return f"{type(self).__name__}({self.number!r})"

    def __sub__(self, argument) -> "NumberedInterval":
        """
        Subtracts ``argument`` from numbered interval.
        """
        try:
            argument = type(self)(argument)
        except Exception:
            return NotImplemented
        return type(self)(float(self) - float(argument))

    def _from_interval_or_interval_class(self, argument):
        self._from_number(float(argument))

    def _from_named_parts(self, direction, quality, diatonic_number):
        self._from_number(self._named_to_numbered(direction, quality, diatonic_number))

    def _from_number(self, argument):
        number = self._to_nearest_quarter_tone(argument)
        direction = _math.sign(number)
        octaves = 0
        pc_number = abs(number)
        while pc_number > 12:
            pc_number -= 12
            octaves += 1
        self._octaves = octaves
        self._interval_class = NumberedIntervalClass(pc_number * direction)

    @property
    def direction_number(self) -> int:
        """
        Gets direction number of numbered interval.

        ..  container:: example

            >>> abjad.NumberedInterval(-14).direction_number
            -1

            >>> abjad.NumberedInterval(0).direction_number
            0

            >>> abjad.NumberedInterval(6).direction_number
            1

        """
        return _math.sign(self.number)

    @property
    def interval_class(self) -> "NumberedIntervalClass":
        """
        Gets numbered interval class.
        """
        return self._interval_class

    @property
    def number(self) -> float | int:
        """
        Gets number of numbered interval.

        ..  container:: example

            >>> abjad.NumberedInterval(-14).number
            -14

            >>> abjad.NumberedInterval(-2).number
            -2

            >>> abjad.NumberedInterval(0).number
            0

        """
        number = self._interval_class._number
        direction = _math.sign(number)
        number = abs(number) + (12 * self.octaves)
        return number * direction

    @property
    def octaves(self) -> int:
        """
        Gets octaves of interval.
        """
        return self._octaves

    @property
    def semitones(self) -> int | float:
        """
        Gets semitones corresponding to numbered interval.

        ..  container:: example

            >>> abjad.NumberedInterval(-14).semitones
            -14

        """
        return self.number

    @property
    def signed_string(self):
        """
        Gets signed string.
        """
        direction_symbol = _direction_number_to_direction_symbol[
            _math.sign(self.number)
        ]
        return f"{direction_symbol}{abs(self.number)}"

    @classmethod
    def from_pitch_carriers(
        class_, pitch_carrier_1, pitch_carrier_2
    ) -> "NumberedInterval":
        """
        Makes numbered interval from ``pitch_carrier_1`` and ``pitch_carrier_2``.

        ..  container:: example

            >>> abjad.NumberedInterval.from_pitch_carriers(
            ...     abjad.NamedPitch(-2),
            ...     abjad.NamedPitch(12),
            ...     )
            NumberedInterval(14)

            >>> abjad.NumberedInterval.from_pitch_carriers(
            ...     abjad.NamedPitch(12),
            ...     abjad.NamedPitch(12),
            ...     )
            NumberedInterval(0)

            >>> abjad.NumberedInterval.from_pitch_carriers(
            ...     abjad.NamedPitch(9),
            ...     abjad.NamedPitch(12),
            ...     )
            NumberedInterval(3)

            >>> abjad.NumberedInterval.from_pitch_carriers(
            ...     abjad.NamedPitch(12),
            ...     abjad.NamedPitch(9),
            ...     )
            NumberedInterval(-3)

            >>> abjad.NumberedInterval.from_pitch_carriers(
            ...     abjad.NamedPitch(12),
            ...     abjad.NamedPitch(-2),
            ...     )
            NumberedInterval(-14)

        """
        pitch_1 = NamedPitch(pitch_carrier_1)
        pitch_2 = NamedPitch(pitch_carrier_2)
        number = NumberedPitch(pitch_2).number - NumberedPitch(pitch_1).number
        number = _math.integer_equivalent_number_to_integer(number)
        return class_(number)

    def transpose(self, pitch_carrier):
        """
        Transposes ``pitch_carrier``

        ..  container:: example

            Transposes chord:

            >>> chord = abjad.Chord("<c' e' g'>4")

            >>> interval = abjad.NumberedInterval(1)
            >>> interval.transpose(chord)
            Chord("<df' f' af'>4")

        Returns newly constructed object of ``pitch_carrier`` type.
        """
        return super().transpose(pitch_carrier)


@functools.total_ordering
class PitchClass:
    """
    Abstract pitch-class.
    """

    __slots__ = ()

    _is_abstract = True

    def __init__(self, argument):
        if isinstance(argument, str):
            match = _comprehensive_pitch_name_regex.match(argument)
            if not match:
                match = _comprehensive_pitch_class_name_regex.match(argument)
            if not match:
                class_name = type(self).__name__
                message = f"can not instantiate {class_name} from {argument!r}."
                raise ValueError(message)
            group_dict = match.groupdict()
            dpc_name = group_dict["diatonic_pc_name"].lower()
            dpc_number = _diatonic_pc_name_to_diatonic_pc_number[dpc_name]
            alteration = Accidental(group_dict["comprehensive_accidental"]).semitones
            self._from_named_parts(dpc_number, alteration)
        elif isinstance(argument, numbers.Number):
            self._from_number(argument)
        elif isinstance(argument, Pitch | PitchClass):
            self._from_pitch_or_pitch_class(argument)
        else:
            try:
                pitch = NamedPitch(argument)
                self._from_pitch_or_pitch_class(pitch)
            except Exception:
                class_name = type(self).__name__
                message = f"can not instantiate {class_name} from {argument!r}."
                raise ValueError(message)

    def __eq__(self, argument) -> bool:
        """
        Compares reprs.
        """
        if isinstance(argument, type(self)):
            return repr(self) == repr(argument)
        return False

    # TODO: remove
    def __float__(self):
        """
        Coerce to float.

        Returns float.
        """
        return float(self.number)

    def __hash__(self) -> int:
        """
        Hashes pitch-class.
        """
        return hash(self.__class__.__name__ + repr(self))

    def __lt__(self, argument):
        """
        Is true when pitch-class is less than ``argument``.

        Returns true or false.
        """
        raise NotImplementedError

    def _from_named_parts(self, dpc_number, alteration):
        raise NotImplementedError

    def _from_number(self, number):
        raise NotImplementedError

    def _from_pitch_or_pitch_class(self, pitch_or_pitch_class):
        raise NotImplementedError

    def _get_alteration(self):
        raise NotImplementedError

    def _get_diatonic_pc_number(self):
        raise NotImplementedError

    def _get_lilypond_format(self):
        raise NotImplementedError

    @staticmethod
    def _to_nearest_quarter_tone(number):
        number = round((float(number) % 12) * 4) / 4
        div, mod = divmod(number, 1)
        if mod == 0.75:
            div += 1
        elif mod == 0.5:
            div += 0.5
        div %= 12
        return _math.integer_equivalent_number_to_integer(div)

    def accidental(self):
        """
        Gets accidental of pitch-class.
        """
        raise NotImplementedError

    def pitch_class_label(self):
        """
        Gets pitch-class label of pitch-class.
        """
        raise NotImplementedError

    def invert(self, axis=None):
        """
        Inverts pitch-class about ``axis``.

        Returns new pitch-class.
        """
        raise NotImplementedError

    def multiply(self, n=1):
        """
        Multiplies pitch-class by ``n``.

        Returns new pitch-class.
        """
        raise NotImplementedError

    def transpose(self, n=0):
        """
        Transposes pitch-class by index ``n``.

        Returns new pitch-class.
        """
        raise NotImplementedError


class NamedPitchClass(PitchClass):
    """
    Named pitch-class.

    ..  container:: example

        Initializes from pitch-class name:

        >>> abjad.NamedPitchClass("cs")
        NamedPitchClass('cs')

        >>> abjad.NamedPitchClass("cqs")
        NamedPitchClass('cqs')

        Initializes from number of semitones:

        >>> abjad.NamedPitchClass(14)
        NamedPitchClass('d')

        >>> abjad.NamedPitchClass(14.5)
        NamedPitchClass('dqs')

        Initializes from named pitch:

        >>> abjad.NamedPitchClass(abjad.NamedPitch("d"))
        NamedPitchClass('d')

        >>> abjad.NamedPitchClass(abjad.NamedPitch("dqs"))
        NamedPitchClass('dqs')

        Initializes from numbered pitch:

        >>> abjad.NamedPitchClass(abjad.NumberedPitch(14))
        NamedPitchClass('d')

        >>> abjad.NamedPitchClass(abjad.NumberedPitch(14.5))
        NamedPitchClass('dqs')

        Initializes from numbered pitch-class:

        >>> abjad.NamedPitchClass(abjad.NumberedPitchClass(2))
        NamedPitchClass('d')

        >>> abjad.NamedPitchClass(abjad.NumberedPitchClass(2.5))
        NamedPitchClass('dqs')

        Initializes from pitch-class / octave-number string:

        >>> abjad.NamedPitchClass("C#5")
        NamedPitchClass('cs')

        >>> abjad.NamedPitchClass("Cs5")
        NamedPitchClass('cs')

        Initializes quartertone from pitch-class / octave-number string:

        >>> abjad.NamedPitchClass("C+5")
        NamedPitchClass('cqs')

        >>> abjad.NamedPitchClass("Cqs5")
        NamedPitchClass('cqs')

        Initializes from pitch-class string:

        >>> abjad.NamedPitchClass("C#")
        NamedPitchClass('cs')

        >>> abjad.NamedPitchClass("Cs")
        NamedPitchClass('cs')

        >>> abjad.NamedPitchClass("cs")
        NamedPitchClass('cs')

        Initializes quartertone from pitch-class string

        >>> abjad.NamedPitchClass("C+")
        NamedPitchClass('cqs')

        >>> abjad.NamedPitchClass("Cqs")
        NamedPitchClass('cqs')

        >>> abjad.NamedPitchClass("cqs")
        NamedPitchClass('cqs')

        Initializes from note:

        >>> abjad.NamedPitchClass(abjad.Note("d''8."))
        NamedPitchClass('d')

        >>> abjad.NamedPitchClass(abjad.Note("dqs''8."))
        NamedPitchClass('dqs')

    """

    __slots__ = ("_diatonic_pc_number", "_accidental")

    def __init__(self, name="c", *, accidental=None, arrow=None):
        super().__init__(name or "c")
        if accidental is not None:
            self._accidental = type(self._accidental)(accidental)
        if arrow is not None:
            self._accidental = type(self._accidental)(self._accidental, arrow=arrow)

    def __add__(self, named_interval) -> "NamedPitchClass":
        """
        Adds ``named_interval`` to named pitch-class.

        ..  container:: example

            >>> abjad.NamedPitchClass("cs") + abjad.NamedInterval("+M9")
            NamedPitchClass('ds')

            >>> abjad.NamedPitchClass("cs") + abjad.NamedInterval("-M9")
            NamedPitchClass('b')

        """
        dummy_pitch = NamedPitch((self.name, 4))
        pitch = named_interval.transpose(dummy_pitch)
        return type(self)(pitch)

    def __eq__(self, argument) -> bool:
        """
        Compares string formats.

        ..  container:: example

            >>> pitch_class_1 = abjad.NamedPitchClass("cs")
            >>> pitch_class_2 = abjad.NamedPitchClass("cs")
            >>> pitch_class_3 = abjad.NamedPitchClass("df")

            >>> pitch_class_1 == pitch_class_1
            True
            >>> pitch_class_1 == pitch_class_2
            True
            >>> pitch_class_1 == pitch_class_3
            False

            >>> pitch_class_2 == pitch_class_1
            True
            >>> pitch_class_2 == pitch_class_2
            True
            >>> pitch_class_2 == pitch_class_3
            False

            >>> pitch_class_3 == pitch_class_1
            False
            >>> pitch_class_3 == pitch_class_2
            False
            >>> pitch_class_3 == pitch_class_3
            True

        """
        return super().__eq__(argument)

    def __hash__(self):
        """
        Hashes named pitch-class.

        Returns integer.
        """
        return super().__hash__()

    def __lt__(self, argument) -> bool:
        """
        Compares ``number``.

        ..  container:: example

            >>> abjad.NamedPitchClass("cs") < abjad.NamedPitchClass("d")
            True

            >>> abjad.NamedPitchClass("d") < abjad.NamedPitchClass("cs")
            False

        """
        assert isinstance(argument, type(self))
        return self.number < argument.number

    def __radd__(self, interval):
        """
        Right-addition not defined on named pitch-classes.

        ..  container:: example

            >>> abjad.NamedPitchClass("cs").__radd__(1)
            Traceback (most recent call last):
                ...
            NotImplementedError: right-addition not defined on NamedPitchClass.

        """
        message = f"right-addition not defined on {type(self).__name__}."
        raise NotImplementedError(message)

    def __repr__(self):
        """
        Gets repr.
        """
        return f"{type(self).__name__}({self.name!r})"

    def __sub__(self, argument) -> "NamedInversionEquivalentIntervalClass":
        """
        Subtracts ``argument`` from named pitch-class.

        ..  container:: example

            >>> abjad.NamedPitchClass("cs") - abjad.NamedPitchClass("g")
            NamedInversionEquivalentIntervalClass('+A4')

            >>> abjad.NamedPitchClass("c") - abjad.NamedPitchClass("cf")
            NamedInversionEquivalentIntervalClass('+A1')

            >>> abjad.NamedPitchClass("cf") - abjad.NamedPitchClass("c")
            NamedInversionEquivalentIntervalClass('+A1')

        """
        assert isinstance(argument, type(self))
        pitch_1 = NamedPitch((self.name, 4))
        pitch_2 = NamedPitch((argument.name, 4))
        mdi = NamedInterval.from_pitch_carriers(pitch_1, pitch_2)
        pair = (mdi.quality, mdi.number)
        dic = NamedInversionEquivalentIntervalClass(pair)
        return dic

    def _apply_accidental(self, accidental=None):
        accidental = Accidental(accidental)
        new_accidental = self.accidental + accidental
        new_name = self._get_diatonic_pc_name() + str(new_accidental)
        return type(self)(new_name)

    def _from_named_parts(self, dpc_number, alteration):
        self._diatonic_pc_number = dpc_number
        self._accidental = Accidental(alteration)

    def _from_number(self, number):
        numbered_pitch_class = NumberedPitchClass(number)
        self._from_pitch_or_pitch_class(numbered_pitch_class)

    def _from_pitch_or_pitch_class(self, pitch_or_pitch_class):
        if isinstance(pitch_or_pitch_class, Pitch):
            pitch_or_pitch_class = pitch_or_pitch_class.pitch_class
        self._diatonic_pc_number = pitch_or_pitch_class._get_diatonic_pc_number()
        self._accidental = Accidental(
            pitch_or_pitch_class._get_alteration(),
            arrow=pitch_or_pitch_class.arrow,
        )

    def _get_alteration(self):
        return self._accidental.semitones

    def _get_diatonic_pc_name(self):
        return _diatonic_pc_number_to_diatonic_pc_name[self._diatonic_pc_number]

    def _get_diatonic_pc_number(self):
        return self._diatonic_pc_number

    def _get_lilypond_format(self):
        name = self._get_diatonic_pc_name()
        accidental = Accidental(self._get_alteration())
        return f"{name}{accidental!s}"

    @property
    def accidental(self):
        """
        Gets accidental.

        ..  container:: example

            >>> abjad.NamedPitchClass("cs").accidental
            Accidental(name='sharp')

        """
        return self._accidental

    @property
    def arrow(self):
        """
        Gets arrow of named pitch-class.

        Returns up, down or none.
        """
        return self._accidental.arrow

    @property
    def name(self) -> str:
        """
        Gets name of named pitch-class.

        ..  container:: example

            >>> abjad.NamedPitchClass("cs").name
            'cs'

        """
        diatonic_pc_name = _diatonic_pc_number_to_diatonic_pc_name[
            self._diatonic_pc_number
        ]
        return f"{diatonic_pc_name}{self._accidental!s}"

    @property
    def number(self) -> int | float:
        """
        Gets number.

        ..  container:: example

            >>> abjad.NamedPitchClass("cs").number
            1

        """
        dictionary = _diatonic_pc_number_to_pitch_class_number
        result = dictionary[self._diatonic_pc_number]
        result += self._accidental.semitones
        result %= 12
        return result

    @property
    def pitch_class_label(self):
        """
        Gets pitch-class label.

        ..  container:: example

            >>> abjad.NamedPitchClass("cs").pitch_class_label
            'C#'

        """
        pc = self._get_diatonic_pc_name().upper()
        return f"{pc}{self.accidental.symbol}"

    def invert(self, axis=None) -> "NamedPitchClass":
        """
        Inverts named pitch-class.
        """
        axis = axis or NamedPitch("c")
        axis = NamedPitch(axis)
        this = NamedPitch(self)
        interval = this - axis
        result = axis.transpose(interval)
        result = type(self)(result)
        return result

    def multiply(self, n=1) -> "NamedPitchClass":
        """
        Multiplies named pitch-class by ``n``.

        ..  container:: example

            >>> abjad.NamedPitchClass("cs").multiply(3)
            NamedPitchClass('ef')

        """
        return type(self)(n * self.number)

    def transpose(self, n=0) -> "NamedPitchClass":
        """
        Transposes named pitch-class by index named interval ``n``.

        ..  container:: example

            >>> interval = abjad.NamedInterval("-M2")
            >>> abjad.NamedPitchClass("cs").transpose(interval)
            NamedPitchClass('b')

            >>> interval = abjad.NamedInterval("P1")
            >>> abjad.NamedPitchClass("cs").transpose(interval)
            NamedPitchClass('cs')

            >>> interval = abjad.NamedInterval("+M2")
            >>> abjad.NamedPitchClass("cs").transpose(interval)
            NamedPitchClass('ds')

        """
        interval = NamedInterval(n)
        pitch = NamedPitch((self.name, 4))
        pitch = interval.transpose(pitch)
        return type(self)(pitch)


class NumberedPitchClass(PitchClass):
    """
    Numbered pitch-class.

    ..  container:: example

        Initializes from number of semitones:

        >>> abjad.NumberedPitchClass(13)
        NumberedPitchClass(1)

        Initializes from pitch name:

        >>> abjad.NumberedPitchClass("d")
        NumberedPitchClass(2)

        Initializes from named pitch:

        >>> abjad.NumberedPitchClass(abjad.NamedPitch("g,"))
        NumberedPitchClass(7)

        Initializes from numbered pitch:

        >>> abjad.NumberedPitchClass(abjad.NumberedPitch(15))
        NumberedPitchClass(3)

        Initializes from named pitch-class:

        >>> abjad.NumberedPitchClass(abjad.NamedPitchClass("e"))
        NumberedPitchClass(4)

        Initializes from pitch-class / octave string:

        >>> abjad.NumberedPitchClass("C#5")
        NumberedPitchClass(1)

        Initializes from other numbered pitch-class:

        >>> abjad.NumberedPitchClass(abjad.NumberedPitchClass(9))
        NumberedPitchClass(9)

        Initializes from note:

        >>> abjad.NumberedPitchClass(abjad.Note("a'8."))
        NumberedPitchClass(9)

    """

    __slots__ = ("_arrow", "_number")

    def __init__(self, number=0, *, arrow=None):
        super().__init__(number or 0)
        if arrow is not None:
            arrow = _string.to_tridirectional_ordinal_constant(arrow)
            if arrow is _enums.CENTER:
                arrow = None
            self._arrow = arrow

    def __add__(self, argument) -> "NumberedPitchClass":
        """
        Adds ``argument`` to numbered pitch-class.

        ..  container:: example

            >>> pitch_class = abjad.NumberedPitchClass(9)

            >>> pitch_class + abjad.NumberedInterval(0)
            NumberedPitchClass(9)

            >>> pitch_class + abjad.NumberedInterval(1)
            NumberedPitchClass(10)

            >>> pitch_class + abjad.NumberedInterval(2)
            NumberedPitchClass(11)

            >>> pitch_class + abjad.NumberedInterval(3)
            NumberedPitchClass(0)

        """
        interval = NumberedInterval(argument)
        return type(self)(self.number + interval.number % 12)

    def __copy__(self, *arguments) -> "NumberedPitchClass":
        """
        Copies numbered pitch-class.

        ..  container:: example

            >>> import copy
            >>> pitch_class = abjad.NumberedPitchClass(9)
            >>> copy.copy(pitch_class)
            NumberedPitchClass(9)

        """
        return type(self)(self)

    def __eq__(self, argument):
        """
        Compares ``number``.

        ..  container:: example

            >>> pitch_class_1 = abjad.NumberedPitchClass(0)
            >>> pitch_class_2 = abjad.NumberedPitchClass(0)
            >>> pitch_class_3 = abjad.NumberedPitchClass(1)

            >>> pitch_class_1 == pitch_class_1
            True
            >>> pitch_class_1 == pitch_class_2
            True
            >>> pitch_class_1 == pitch_class_3
            False

            >>> pitch_class_2 == pitch_class_1
            True
            >>> pitch_class_2 == pitch_class_2
            True
            >>> pitch_class_2 == pitch_class_3
            False

            >>> pitch_class_3 == pitch_class_1
            False
            >>> pitch_class_3 == pitch_class_2
            False
            >>> pitch_class_3 == pitch_class_3
            True

        """
        if isinstance(argument, type(self)):
            return self.number == argument.number

    def __hash__(self):
        """
        Hashes numbered pitch-class.

        Returns integer.
        """
        return super().__hash__()

    def __lt__(self, argument) -> bool:
        """
        Compares ``number``.

        ..  container:: example

            >>> abjad.NumberedPitchClass(1) < abjad.NumberedPitchClass(2)
            True

            >>> abjad.NumberedPitchClass(2) < abjad.NumberedPitchClass(1)
            False

        """
        if not isinstance(argument, type(self)):
            raise TypeError(f"can not compare numbered pitch-class to {argument!r}.")
        return self.number < argument.number

    def __neg__(self) -> "NumberedPitchClass":
        """
        Negates numbered pitch-class.

        ..  container:: example

            >>> pitch_class = abjad.NumberedPitchClass(9)
            >>> -pitch_class
            NumberedPitchClass(3)

        """
        return type(self)(-self.number)

    def __radd__(self, argument):
        """
        Right-addition not defined on numbered pitch-classes.

        ..  container:: example

            >>> 1 + abjad.NumberedPitchClass(9)
            Traceback (most recent call last):
                ...
            NotImplementedError: right-addition not defined on NumberedPitchClass.

        Raises not implemented error.
        """
        message = f"right-addition not defined on {type(self).__name__}."
        raise NotImplementedError(message)

    def __repr__(self):
        """
        Gets repr.
        """
        return f"{type(self).__name__}({self.number!r})"

    def __sub__(
        self, argument
    ) -> typing.Union["NumberedPitchClass", "NumberedInversionEquivalentIntervalClass"]:
        """
        Subtracts ``argument`` from numbered pitch-class.

        Subtraction is defined against both numbered intervals and against other
        pitch-classes.

        ..  container:: example

            >>> abjad.NumberedPitchClass(6) - abjad.NumberedPitchClass(6)
            NumberedInversionEquivalentIntervalClass(0)

            >>> abjad.NumberedPitchClass(6) - abjad.NumberedPitchClass(7)
            NumberedInversionEquivalentIntervalClass(1)

            >>> abjad.NumberedPitchClass(7) - abjad.NumberedPitchClass(6)
            NumberedInversionEquivalentIntervalClass(1)

            >>> abjad.NumberedPitchClass(6) - abjad.NumberedInterval(-1)
            NumberedPitchClass(5)

            >>> abjad.NumberedPitchClass(6) - abjad.NumberedInterval(0)
            NumberedPitchClass(6)

            >>> abjad.NumberedPitchClass(6) - abjad.NumberedInterval(1)
            NumberedPitchClass(5)

        """
        if isinstance(argument, type(self)):
            interval_class_number = abs(self.number - argument.number)
            if 6 < interval_class_number:
                interval_class_number = 12 - interval_class_number
            return NumberedInversionEquivalentIntervalClass(interval_class_number)
        interval_class = NumberedInversionEquivalentIntervalClass(argument)
        return type(self)(self.number - interval_class.number % 12)

    def _apply_accidental(self, accidental=None):
        accidental = Accidental(accidental)
        semitones = self.number + accidental.semitones
        return type(self)(semitones)

    def _from_named_parts(self, dpc_number, alteration):
        number = _diatonic_pc_number_to_pitch_class_number[dpc_number]
        number += alteration
        self._from_number(number)

    def _from_number(self, number):
        self._arrow = None
        self._number = self._to_nearest_quarter_tone(number)

    def _from_pitch_or_pitch_class(self, pitch_or_pitch_class):
        self._arrow = pitch_or_pitch_class.arrow
        self._number = self._to_nearest_quarter_tone(float(pitch_or_pitch_class))

    def _get_alteration(self):
        dpc_number = self._get_diatonic_pc_number()
        pc_number = _diatonic_pc_number_to_pitch_class_number[dpc_number]
        return float(self) - pc_number

    def _get_diatonic_pc_name(self):
        return self.name[0]

    def _get_diatonic_pc_number(self):
        return _diatonic_pc_name_to_diatonic_pc_number[self._get_diatonic_pc_name()]

    def _get_lilypond_format(self):
        return NamedPitchClass(self)._get_lilypond_format()

    @property
    def accidental(self):
        """
        Gets accidental.

        ..  container:: example

            >>> abjad.NumberedPitchClass(1).accidental
            Accidental(name='sharp')

        """
        return NamedPitch(self.number).accidental

    @property
    def arrow(self):
        """
        Gets arrow of numbered pitch-class.

        Returns up, down or none.
        """
        return self._arrow

    @property
    def name(self) -> str:
        """
        Gets name of numbered pitch-class.

        ..  container:: example

            >>> abjad.NumberedPitchClass(13).name
            'cs'

        """
        return _pitch_class_number_to_pitch_class_name[self.number]

    @property
    def number(self) -> int | float:
        """
        Gets number.

        ..  container:: example

            >>> abjad.NumberedPitchClass(1).number
            1

            >>> abjad.NumberedPitchClass(13).number
            1

        """
        return self._number

    @property
    def pitch_class_label(self):
        """
        Gets pitch-class / octave label.

        ..  container:: example

            >>> abjad.NumberedPitchClass(13).pitch_class_label
            'C#'

        """
        name = self._get_diatonic_pc_name().upper()
        return f"{name}{self.accidental.symbol}"

    def invert(self, axis=None) -> "NumberedPitchClass":
        """
        Inverts numbered pitch-class.

        ..  container:: example

            >>> for n in range(12):
            ...     pitch_class = abjad.NumberedPitchClass(n)
            ...     print(repr(pitch_class), repr(pitch_class.invert()))
            ...
            NumberedPitchClass(0) NumberedPitchClass(0)
            NumberedPitchClass(1) NumberedPitchClass(11)
            NumberedPitchClass(2) NumberedPitchClass(10)
            NumberedPitchClass(3) NumberedPitchClass(9)
            NumberedPitchClass(4) NumberedPitchClass(8)
            NumberedPitchClass(5) NumberedPitchClass(7)
            NumberedPitchClass(6) NumberedPitchClass(6)
            NumberedPitchClass(7) NumberedPitchClass(5)
            NumberedPitchClass(8) NumberedPitchClass(4)
            NumberedPitchClass(9) NumberedPitchClass(3)
            NumberedPitchClass(10) NumberedPitchClass(2)
            NumberedPitchClass(11) NumberedPitchClass(1)

        Interprets axis of inversion equal to pitch-class 0.
        """
        axis = axis or NumberedPitch("c")
        axis = NumberedPitch(axis)
        this = NumberedPitch(self)
        interval = this - axis
        result = axis.transpose(interval)
        result = type(self)(result)
        return result

    def multiply(self, n=1) -> "NumberedPitchClass":
        """
        Multiplies pitch-class number by ``n``.

        ..  container:: example

            >>> for n in range(12):
            ...     pitch_class = abjad.NumberedPitchClass(n)
            ...     print(repr(pitch_class), repr(pitch_class.multiply(5)))
            ...
            NumberedPitchClass(0) NumberedPitchClass(0)
            NumberedPitchClass(1) NumberedPitchClass(5)
            NumberedPitchClass(2) NumberedPitchClass(10)
            NumberedPitchClass(3) NumberedPitchClass(3)
            NumberedPitchClass(4) NumberedPitchClass(8)
            NumberedPitchClass(5) NumberedPitchClass(1)
            NumberedPitchClass(6) NumberedPitchClass(6)
            NumberedPitchClass(7) NumberedPitchClass(11)
            NumberedPitchClass(8) NumberedPitchClass(4)
            NumberedPitchClass(9) NumberedPitchClass(9)
            NumberedPitchClass(10) NumberedPitchClass(2)
            NumberedPitchClass(11) NumberedPitchClass(7)

        """
        return type(self)(n * self.number)

    def transpose(self, n=0) -> "NumberedPitchClass":
        """
        Transposes numbered pitch-class by index ``n``.

        ..  container:: example

            >>> for n in range(12):
            ...     pitch_class = abjad.NumberedPitchClass(n)
            ...     print(repr(pitch_class), repr(pitch_class.transpose(-13)))
            ...
            NumberedPitchClass(0) NumberedPitchClass(11)
            NumberedPitchClass(1) NumberedPitchClass(0)
            NumberedPitchClass(2) NumberedPitchClass(1)
            NumberedPitchClass(3) NumberedPitchClass(2)
            NumberedPitchClass(4) NumberedPitchClass(3)
            NumberedPitchClass(5) NumberedPitchClass(4)
            NumberedPitchClass(6) NumberedPitchClass(5)
            NumberedPitchClass(7) NumberedPitchClass(6)
            NumberedPitchClass(8) NumberedPitchClass(7)
            NumberedPitchClass(9) NumberedPitchClass(8)
            NumberedPitchClass(10) NumberedPitchClass(9)
            NumberedPitchClass(11) NumberedPitchClass(10)

        """
        return type(self)(self.number + n)


@functools.total_ordering
class Pitch:
    """
    Abstract pitch.
    """

    __slots__ = ("_pitch_class", "_octave")

    _is_abstract = True

    def __init__(self, argument, accidental=None, arrow=None, octave=None):
        if isinstance(argument, str):
            match = _comprehensive_pitch_name_regex.match(argument)
            if not match:
                match = _comprehensive_pitch_class_name_regex.match(argument)
            if not match:
                class_name = type(self).__name__
                message = f"can not instantiate {class_name} from {argument!r}."
                raise ValueError(message)
            group_dict = match.groupdict()
            _dpc_name = group_dict["diatonic_pc_name"].lower()
            _dpc_number = _diatonic_pc_name_to_diatonic_pc_number[_dpc_name]
            _alteration = Accidental(group_dict["comprehensive_accidental"]).semitones
            foo = group_dict.get("comprehensive_octave", "")
            assert isinstance(foo, str), repr(foo)
            if foo.isdigit():
                number = int(foo)
                _octave = Octave(number).number
            else:
                _octave = Octave.from_ticks(foo).number
            self._from_named_parts(_dpc_number, _alteration, _octave)
        elif isinstance(argument, numbers.Number):
            self._from_number(argument)
        elif isinstance(argument, Pitch | PitchClass):
            self._from_pitch_or_pitch_class(argument)
        elif isinstance(argument, tuple) and len(argument) == 2:
            _pitch_class = NamedPitchClass(argument[0])
            _octave = Octave(argument[1])
            self._from_named_parts(
                _pitch_class._get_diatonic_pc_number(),
                _pitch_class._get_alteration(),
                _octave.number,
            )
        elif hasattr(argument, "written_pitch"):
            self._from_pitch_or_pitch_class(argument.written_pitch)
        elif hasattr(argument, "note_heads") and len(argument.note_heads):
            self._from_pitch_or_pitch_class(argument.note_heads[0])
        else:
            class_name = type(self).__name__
            raise ValueError(f"can not instantiate {class_name} from {argument!r}.")
        if accidental is not None:
            accidental = Accidental(accidental)
            self._pitch_class = type(self._pitch_class)(
                self._pitch_class, accidental=accidental
            )
        if arrow is not None:
            self._pitch_class = type(self._pitch_class)(self._pitch_class, arrow=arrow)
        if octave is not None:
            octave = Octave(octave)
            self._octave = octave

    # TODO: remove
    def __float__(self):
        """
        Coerce to float.

        Returns float.
        """
        return float(self.number)

    def __hash__(self) -> int:
        """
        Hashes pitch.
        """
        return hash(self.__class__.__name__ + repr(self))

    def __lt__(self, argument):
        """
        Is true when pitch is less than ``argument``.

        Returns true or false.
        """
        raise NotImplementedError

    def _get_lilypond_format(self):
        raise NotImplementedError

    @staticmethod
    def _to_nearest_octave(pitch_number, pitch_class_number):
        target_pc = pitch_number % 12
        down = (target_pc - pitch_class_number) % 12
        up = (pitch_class_number - target_pc) % 12
        if up < down:
            return pitch_number + up
        else:
            return pitch_number - down

    @staticmethod
    def _to_nearest_quarter_tone(number):
        number = round(float(number) * 4) / 4
        quotient, remainder = divmod(number, 1)
        if remainder == 0.75:
            quotient += 1
        elif remainder == 0.5:
            quotient += 0.5
        return _math.integer_equivalent_number_to_integer(quotient)

    @staticmethod
    def _to_pitch_class_item_class(item_class):
        item_class = item_class or NumberedPitch
        if item_class in (NamedPitchClass, NumberedPitchClass):
            return item_class
        elif item_class is NamedPitch:
            return NamedPitchClass
        elif item_class is NumberedPitch:
            return NumberedPitchClass
        else:
            raise TypeError(item_class)

    @staticmethod
    def _to_pitch_item_class(item_class):
        item_class = item_class or NumberedPitch
        if item_class in (NamedPitch, NumberedPitch):
            return item_class
        elif item_class is NamedPitchClass:
            return NamedPitch
        elif item_class is NumberedPitchClass:
            return NumberedPitch
        else:
            raise TypeError(item_class)

    @property
    def arrow(self):
        """
        Gets arrow of pitch.
        """
        raise NotImplementedError

    @property
    def hertz(self) -> float:
        """
        Gets frequency of pitch in Hertz.
        """
        hertz = pow(2.0, (float(self.number) - 9.0) / 12.0) * 440.0
        return hertz

    @property
    def name(self):
        """
        Gets name of pitch.

        Returns string.
        """
        raise NotImplementedError

    @property
    def number(self):
        """
        Gets number of pitch.

        Returns number.
        """
        raise NotImplementedError

    @property
    def octave(self):
        """
        Gets octave of pitch.

        Returns octave.
        """
        raise NotImplementedError

    @property
    def pitch_class(self):
        """
        Gets pitch-class of pitch.

        Returns pitch-class.
        """
        raise NotImplementedError

    @classmethod
    def from_hertz(class_, hertz):
        """
        Creates pitch from ``hertz``.

        Returns new pitch.
        """
        midi = 9.0 + (12.0 * math.log(float(hertz) / 440.0, 2))
        pitch = class_(midi)
        return pitch

    def get_name(self, locale=None):
        """
        Gets name of pitch according to ``locale``.

        Returns string.
        """
        raise NotImplementedError

    def invert(self, axis=None):
        """
        Inverts pitch about ``axis``.

        Interprets ``axis`` of none equal to middle C.

        Returns new pitch.
        """
        axis = axis or NamedPitch("c'")
        axis = type(self)(axis)
        interval = self - axis
        result = axis.transpose(interval)
        return result

    def multiply(self, n=1):
        """
        Multiplies pitch by ``n``.

        Returns new pitch.
        """
        return type(self)(n * self.number)

    def transpose(self, n):
        """
        Transposes pitch by index ``n``.

        Returns new pitch.
        """
        raise NotImplementedError


@functools.total_ordering
class NamedPitch(Pitch):
    r"""
    Named pitch.

    ..  container:: example

        Initializes from pitch name:

        >>> abjad.NamedPitch("cs''")
        NamedPitch("cs''")

        Initializes quartertone from pitch name:

        >>> abjad.NamedPitch("aqs")
        NamedPitch('aqs')

        Initializes from pitch-class / octave string:

        >>> abjad.NamedPitch("C#5")
        NamedPitch("cs''")

        Initializes quartertone from pitch-class / octave string:

        >>> abjad.NamedPitch("A+3")
        NamedPitch('aqs')

        >>> abjad.NamedPitch("Aqs3")
        NamedPitch('aqs')

        Initializes arrowed pitch:

        >>> abjad.NamedPitch("C#5", arrow=abjad.UP)
        NamedPitch("cs''", arrow=Vertical.UP)

    ..  container:: example

        REGRESSION. Small floats just less than a C initialize in the correct octave:

        Initializes c / C3:

        >>> abjad.NamedPitch(-12.1)
        NamedPitch('c')

        Initializes c' / C4:

        >>> abjad.NamedPitch(-0.1)
        NamedPitch("c'")

        Initializes c'' / C5:

        >>> abjad.NamedPitch(11.9)
        NamedPitch("c''")

    """

    __slots__ = ()

    def __init__(self, name="c'", *, accidental=None, arrow=None, octave=None):
        super().__init__(
            name or "c'", accidental=accidental, arrow=arrow, octave=octave
        )

    def __add__(self, interval) -> "NamedPitch":
        """
        Adds named pitch to ``interval``.

        ..  container:: example

            >>> abjad.NamedPitch("cs''") + abjad.NamedInterval("-M2")
            NamedPitch("b'")

            >>> abjad.NamedPitch("cs''") + abjad.NamedInterval("P1")
            NamedPitch("cs''")

            >>> abjad.NamedPitch("cs''") + abjad.NamedInterval("+M2")
            NamedPitch("ds''")

        """
        interval = NamedInterval(interval)
        return interval.transpose(self)

    def __copy__(self, *arguments) -> "NamedPitch":
        """
        Copies named pitch.

        >>> import copy

        ..  container:: example

            >>> copy.copy(abjad.NamedPitch("c''"))
            NamedPitch("c''")

            >>> copy.copy(abjad.NamedPitch("cs''"))
            NamedPitch("cs''")

            >>> copy.copy(abjad.NamedPitch("df''"))
            NamedPitch("df''")

            Copies arrowed pitch:

            >>> pitch = abjad.NamedPitch("cs''", arrow=abjad.UP)
            >>> copy.copy(pitch)
            NamedPitch("cs''", arrow=Vertical.UP)

        """
        return type(self)(self, arrow=self.arrow)

    def __eq__(self, argument) -> bool:
        """
        Is true when ``argument`` is a named pitch equal to this named pitch.

        ..  container:: example

            >>> pitch_1 = abjad.NamedPitch("fs")
            >>> pitch_2 = abjad.NamedPitch("fs")
            >>> pitch_3 = abjad.NamedPitch("gf")

            >>> pitch_1 == pitch_1
            True
            >>> pitch_1 == pitch_2
            True
            >>> pitch_1 == pitch_3
            False

            >>> pitch_2 == pitch_1
            True
            >>> pitch_2 == pitch_2
            True
            >>> pitch_2 == pitch_3
            False

            >>> pitch_3 == pitch_1
            False
            >>> pitch_3 == pitch_2
            False
            >>> pitch_3 == pitch_3
            True

        Returns true or false.
        """
        if isinstance(argument, str):
            argument = NamedPitch(argument)
        if isinstance(argument, type(self)):
            return (
                self.number == argument.number
                and self.accidental == argument.accidental
                and self.arrow == argument.arrow
                and self.octave == argument.octave
            )
        return False

    def __hash__(self):
        """
        Hashes numbered pitch.
        """
        return super().__hash__()

    # mypy currently does not support functools.total_ordering
    # https://github.com/python/mypy/issues/4610
    # remove __le__ (in favor of __lt__) when mypy supports functools.total_ordering
    # or, refactor this class as a dataclass and then remove __le__
    def __le__(self, argument) -> bool:
        """
        Is true when named pitch is less than or equal to ``argument``.

        ..  container:: example

            >>> pitch_1 = abjad.NamedPitch("fs")
            >>> pitch_2 = abjad.NamedPitch("fs")
            >>> pitch_3 = abjad.NamedPitch("gf")

            >>> pitch_1 <= pitch_1
            True
            >>> pitch_1 <= pitch_2
            True
            >>> pitch_1 <= pitch_3
            True

            >>> pitch_2 <= pitch_1
            True
            >>> pitch_2 <= pitch_2
            True
            >>> pitch_2 <= pitch_3
            True

            >>> pitch_3 <= pitch_1
            False
            >>> pitch_3 <= pitch_2
            False
            >>> pitch_3 <= pitch_3
            True

        """
        try:
            argument = type(self)(argument)
        except (TypeError, ValueError):
            return False
        self_dpn = self._get_diatonic_pitch_number()
        argument_dpn = argument._get_diatonic_pitch_number()
        if self_dpn == argument_dpn:
            return self.accidental <= argument.accidental
        return self_dpn <= argument_dpn

    def __lt__(self, argument) -> bool:
        """
        Is true when named pitch is less than ``argument``.

        ..  container:: example

            >>> pitch_1 = abjad.NamedPitch("fs")
            >>> pitch_2 = abjad.NamedPitch("fs")
            >>> pitch_3 = abjad.NamedPitch("gf")

            >>> pitch_1 < pitch_1
            False
            >>> pitch_1 < pitch_2
            False
            >>> pitch_1 < pitch_3
            True

            >>> pitch_2 < pitch_1
            False
            >>> pitch_2 < pitch_2
            False
            >>> pitch_2 < pitch_3
            True

            >>> pitch_3 < pitch_1
            False
            >>> pitch_3 < pitch_2
            False
            >>> pitch_3 < pitch_3
            False

        Returns true or false.
        """
        try:
            argument = type(self)(argument)
        except (TypeError, ValueError):
            return False
        self_dpn = self._get_diatonic_pitch_number()
        argument_dpn = argument._get_diatonic_pitch_number()
        if self_dpn == argument_dpn:
            return self.accidental < argument.accidental
        return self_dpn < argument_dpn

    def __radd__(self, interval):
        """
        Right-addition not defined on named pitches.

        ..  container:: example

            >>> abjad.NamedPitch("cs'").__radd__(1)
            Traceback (most recent call last):
                ...
            NotImplementedError: right-addition not defined on NamedPitch.

        """
        message = f"right-addition not defined on {type(self).__name__}."
        raise NotImplementedError(message)

    def __repr__(self):
        """
        Gets repr.
        """
        if self.arrow is not None:
            return f"{type(self).__name__}({self.name!r}, arrow={self.arrow})"
        else:
            return f"{type(self).__name__}({self.name!r})"

    def __sub__(self, argument) -> "NamedInterval":
        """
        Subtracts ``argument`` from named pitch.

        ..  container:: example

            >>> abjad.NamedPitch("cs''") - abjad.NamedPitch("b'")
            NamedInterval('-M2')

            >>> abjad.NamedPitch("cs''") - abjad.NamedPitch("fs''")
            NamedInterval('+P4')

        """
        if isinstance(argument, type(self)):
            return NamedInterval.from_pitch_carriers(self, argument)
        interval = NamedInterval(argument)
        interval = -interval
        return interval.transpose(self)

    def _apply_accidental(self, accidental):
        name = self._get_diatonic_pc_name()
        name += str(self.accidental + Accidental(accidental))
        name += self.octave.ticks
        return type(self)(name)

    def _from_named_parts(self, dpc_number, alteration, octave):
        dpc_name = _diatonic_pc_number_to_diatonic_pc_name[dpc_number]
        accidental = Accidental(alteration)
        octave = Octave(octave)
        self._octave = octave
        self._pitch_class = NamedPitchClass(dpc_name + str(accidental))

    def _from_number(self, number):
        number = self._to_nearest_quarter_tone(number)
        quotient, remainder = divmod(number, 12)
        pitch_class = NumberedPitchClass(remainder)
        self._from_named_parts(
            dpc_number=pitch_class._get_diatonic_pc_number(),
            alteration=pitch_class._get_alteration(),
            octave=quotient + 4,
        )

    def _from_pitch_or_pitch_class(self, pitch_or_pitch_class):
        name = pitch_or_pitch_class._get_lilypond_format()
        if not isinstance(pitch_or_pitch_class, Pitch):
            name += "'"
        if isinstance(pitch_or_pitch_class, Pitch):
            self._pitch_class = NamedPitchClass(pitch_or_pitch_class.pitch_class)
            self._octave = pitch_or_pitch_class.octave
        else:
            self._pitch_class = NamedPitchClass(pitch_or_pitch_class)
            self._octave = Octave()

    def _get_alteration(self):
        return self.accidental.semitones

    def _get_diatonic_pc_name(self):
        return _diatonic_pc_number_to_diatonic_pc_name[
            self.pitch_class._diatonic_pc_number
        ]

    def _get_diatonic_pc_number(self):
        diatonic_pc_name = self._get_diatonic_pc_name()
        diatonic_pc_number = _diatonic_pc_name_to_diatonic_pc_number[diatonic_pc_name]
        return diatonic_pc_number

    def _get_diatonic_pitch_number(self):
        diatonic_pitch_number = 7 * (self.octave.number - 4)
        diatonic_pitch_number += self._get_diatonic_pc_number()
        return diatonic_pitch_number

    def _get_lilypond_format(self):
        return self.name

    def _list_contributions(self):
        contributions = []
        if self.arrow is None:
            return contributions
        string = r"\once \override Accidental.stencil ="
        string += " #ly:text-interface::print"
        contributions.append(string)
        glyph = f"accidentals.{self.accidental.name}"
        glyph += f".arrow{str(self.arrow).lower()}"
        string = r"\once \override Accidental.text ="
        string += rf' \markup {{ \musicglyph #"{glyph}" }}'
        contributions.append(string)
        return contributions

    @property
    def accidental(self) -> "Accidental":
        """
        Gets accidental of named pitch.

        ..  container:: example

            >>> abjad.NamedPitch("c''").accidental
            Accidental(name='natural')

            >>> abjad.NamedPitch("cs''").accidental
            Accidental(name='sharp')

            >>> abjad.NamedPitch("df''").accidental
            Accidental(name='flat')

        """
        return self.pitch_class.accidental

    @property
    def arrow(self):
        """
        Gets arrow of named pitch.

        ..  container:: example

            >>> abjad.NamedPitch("cs''").arrow is None
            True

            >>> abjad.NamedPitch("cs''", arrow=abjad.UP).arrow
            <Vertical.UP: 1>

            >>> abjad.NamedPitch("cs''", arrow=abjad.DOWN).arrow
            <Vertical.DOWN: -1>

            Displays arrow in interpreter representation:

            >>> abjad.NamedPitch("cs''", arrow=abjad.DOWN)
            NamedPitch("cs''", arrow=Vertical.DOWN)

        Returns up, down or none.
        """
        return self._pitch_class.arrow

    @property
    def hertz(self) -> float:
        """
        Gets frequency of named pitch in Hertz.

        ..  container:: example

            >>> abjad.NamedPitch("c''").hertz
            523.25...

            >>> abjad.NamedPitch("cs''").hertz
            554.36...

            >>> abjad.NamedPitch("df''").hertz
            554.36...

        """
        return super().hertz

    @property
    def name(self) -> str:
        """
        Gets name of named pitch.

        ..  container:: example

            >>> abjad.NamedPitch("c''").name
            "c''"

            >>> abjad.NamedPitch("cs''").name
            "cs''"

            >>> abjad.NamedPitch("df''").name
            "df''"

        """
        return f"{self.pitch_class.name}{self.octave.ticks}"

    @property
    def number(self) -> int | float:
        """
        Gets number of named pitch.

        ..  container:: example

            >>> abjad.NamedPitch("c''").number
            12

            >>> abjad.NamedPitch("cs''").number
            13

            >>> abjad.NamedPitch("df''").number
            13

            >>> abjad.NamedPitch("cf'").number
            -1

        """
        diatonic_pc_number = self.pitch_class._get_diatonic_pc_number()
        pc_number = _diatonic_pc_number_to_pitch_class_number[diatonic_pc_number]
        alteration = self.pitch_class._get_alteration()
        octave_base_pitch = (self.octave.number - 4) * 12
        return _math.integer_equivalent_number_to_integer(
            pc_number + alteration + octave_base_pitch
        )

    @property
    def octave(self) -> Octave:
        """
        Gets octave of named pitch.

        ..  container:: example

            >>> abjad.NamedPitch("c''").octave
            Octave(number=5)

            >>> abjad.NamedPitch("cs''").octave
            Octave(number=5)

            >>> abjad.NamedPitch("df''").octave
            Octave(number=5)

        """
        return self._octave

    @property
    def pitch_class(self) -> NamedPitchClass:
        """
        Gets pitch-class of named pitch.

        ..  container:: example

            >>> abjad.NamedPitch("c''").pitch_class
            NamedPitchClass('c')

            >>> abjad.NamedPitch("cs''").pitch_class
            NamedPitchClass('cs')

            >>> abjad.NamedPitch("df''").pitch_class
            NamedPitchClass('df')

        """
        return self._pitch_class

    @classmethod
    def from_hertz(class_, hertz) -> "NamedPitch":
        """
        Makes named pitch from ``hertz``.

        ..  container:: example

            >>> abjad.NamedPitch.from_hertz(440)
            NamedPitch("a'")

            REGRESSION. Returns c'' (C5) and not c' (C4):

            >>> abjad.NamedPitch.from_hertz(519)
            NamedPitch("c''")

        """
        return super().from_hertz(hertz)

    def get_name(self, locale=None) -> str:
        """
        Gets name of named pitch according to ``locale``.

        ..  container:: example

            >>> abjad.NamedPitch("cs''").get_name()
            "cs''"

            >>> abjad.NamedPitch("cs''").get_name(locale="us")
            'C#5'

        Set ``locale`` to ``'us'`` or none.
        """
        if locale is None:
            return self.name
        elif locale == "us":
            name = self._get_diatonic_pc_name().upper()
            return f"{name}{self.accidental.symbol}{self.octave.number}"
        else:
            raise ValueError(f'must be "us" or none: {locale!r}.')

    def invert(self, axis=None) -> "NamedPitch":
        """
        Inverts named pitch around ``axis``.

        Inverts pitch around middle C explicitly:

        ..  container:: example

            >>> abjad.NamedPitch("d'").invert("c'")
            NamedPitch('bf')

            >>> abjad.NamedPitch('bf').invert("c'")
            NamedPitch("d'")

            Inverts pitch around middle C implicitly:

            >>> abjad.NamedPitch("d'").invert()
            NamedPitch('bf')

            >>> abjad.NamedPitch("bf").invert()
            NamedPitch("d'")

            Inverts pitch around A3:

            >>> abjad.NamedPitch("d'").invert("a")
            NamedPitch('e')

        Interprets none-valued ``axis`` equal to middle C.
        """
        return super().invert(axis=axis)

    def multiply(self, n=1) -> "NamedPitch":
        """
        Multiplies named pitch.

        ..  container:: example

            >>> abjad.NamedPitch("d'").multiply(1)
            NamedPitch("d'")

            >>> abjad.NamedPitch("d'").multiply(3)
            NamedPitch("fs'")

            >>> abjad.NamedPitch("d'").multiply(6)
            NamedPitch("c''")

            >>> abjad.NamedPitch("d'").multiply(6.5)
            NamedPitch("cs''")

        """
        return super().multiply(n=n)

    def respell(self, accidental="sharps"):
        """
        Respells named pitch with ``accidental``.

        ..  container:: example

            >>> abjad.NamedPitch("cs").respell(accidental="flats")
            NamedPitch('df')

            >>> abjad.NamedPitch("df").respell(accidental="sharps")
            NamedPitch('cs')

        """
        if accidental == "sharps":
            dictionary = _pitch_class_number_to_pitch_class_name_with_sharps
        else:
            assert accidental == "flats"
            dictionary = _pitch_class_number_to_pitch_class_name_with_flats
        name = dictionary[self.pitch_class.number]
        candidate = type(self)((name, self.octave.number))
        if candidate.number == self.number - 12:
            candidate = type(self)(candidate, octave=candidate.octave.number + 1)
        elif candidate.number == self.number + 12:
            candidate = type(self)(candidate, octave=candidate.octave.number - 1)
        assert candidate.number == self.number
        return candidate

    def simplify(self) -> "NamedPitch":
        """
        Reduce alteration to between -2 and 2 while maintaining identical pitch number.

            >>> abjad.NamedPitch("cssqs'").simplify()
            NamedPitch("dqs'")

            >>> abjad.NamedPitch("cfffqf'").simplify()
            NamedPitch('aqf')

            >>> float(abjad.NamedPitch("cfffqf'").simplify()) == float(abjad.NamedPitch("aqf"))
            True

        ..  note:: LilyPond by default only supports accidentals from
                   double-flat to double-sharp.

        Returns named pitch.
        """
        alteration = self._get_alteration()
        if abs(alteration) <= 2:
            return self
        diatonic_pc_number = self._get_diatonic_pc_number()
        octave = int(self.octave)
        while alteration > 2:
            step_size = 2
            if diatonic_pc_number == 2:  # e to f
                step_size = 1
            elif diatonic_pc_number == 6:  # b to c
                step_size = 1
                octave += 1
            diatonic_pc_number = (diatonic_pc_number + 1) % 7
            alteration -= step_size
        while alteration < -2:
            step_size = 2
            if diatonic_pc_number == 3:  # f to e
                step_size = 1
            elif diatonic_pc_number == 0:  # c to b
                step_size = 1
                octave -= 1
            diatonic_pc_number = (diatonic_pc_number - 1) % 7
            alteration += step_size
        diatonic_pc_name = _diatonic_pc_number_to_diatonic_pc_name[diatonic_pc_number]
        accidental = Accidental(alteration)
        pitch_name = f"{diatonic_pc_name}{accidental!s}{octave!s}"
        return type(self)(pitch_name, arrow=self.arrow)

    def transpose(self, n=0) -> "NamedPitch":
        """
        Transposes named pitch by index ``n``.

        ..  container:: example

            Transposes C4 up a minor second:

            >>> abjad.NamedPitch("c'").transpose(n="m2")
            NamedPitch("df'")

            Transposes C4 down a major second:

            >>> abjad.NamedPitch("c'").transpose(n="-M2")
            NamedPitch('bf')

        """
        interval = NamedInterval(n)
        pitch_number = self.number + interval.semitones
        diatonic_pc_number = self._get_diatonic_pc_number()
        diatonic_pc_number += interval.staff_spaces
        diatonic_pc_number %= 7
        diatonic_pc_name = _diatonic_pc_number_to_diatonic_pc_name[diatonic_pc_number]
        pc = _diatonic_pc_name_to_pitch_class_number[diatonic_pc_name]
        nearest_neighbor = self._to_nearest_octave(pitch_number, pc)
        semitones = pitch_number - nearest_neighbor
        accidental = Accidental(semitones)
        octave_number = int(math.floor((pitch_number - semitones) / 12)) + 4
        octave = Octave(octave_number)
        name = diatonic_pc_name + str(accidental) + octave.ticks
        return type(self)(name)


# mypy currently does not support functools.total_ordering
# https://github.com/python/mypy/issues/4610
@functools.total_ordering
class NumberedPitch(Pitch):
    r"""
    Numbered pitch.

    ..  container:: example

        Initializes from number:

        >>> abjad.NumberedPitch(13)
        NumberedPitch(13)

        Initializes from other numbered pitch:

        >>> abjad.NumberedPitch(abjad.NumberedPitch(13))
        NumberedPitch(13)

        Initializes from pitch-class / octave pair:

        >>> abjad.NumberedPitch((1, 5))
        NumberedPitch(13)

    """

    __slots__ = ("_number",)

    def __init__(self, number=0, *, arrow=None, octave=None):
        super().__init__(number or 0, arrow=arrow, octave=octave)

    def __add__(self, argument) -> "NumberedPitch":
        """
        Adds ``argument`` to numbered pitch.

        ..  container:: example

            >>> abjad.NumberedPitch(12) + abjad.NumberedPitch(13)
            NumberedPitch(25)

            >>> abjad.NumberedPitch(13) + abjad.NumberedPitch(12)
            NumberedPitch(25)

        """
        argument = type(self)(argument)
        semitones = float(self) + float(argument)
        return type(self)(semitones)

    def __eq__(self, argument) -> bool:
        """
        Is true when ``argument`` is a numbered pitch with ``number`` the same as this
        numbered pitch.
        """
        if isinstance(argument, int | float):
            argument = type(self)(argument)
        if isinstance(argument, type(self)):
            return (
                self.number == argument.number
                and self.arrow == argument.arrow
                and self.octave == argument.octave
            )
        return False

    def __hash__(self):
        """
        Hashes numbered pitch.
        """
        return super().__hash__()

    # mypy currently does not support functools.total_ordering
    # https://github.com/python/mypy/issues/4610
    # remove __le__ (in favor of __lt__) when mypy supports functools.total_ordering
    # or, refactor this class as a dataclass and then remove __le__
    def __le__(self, argument) -> bool:
        r"""Is true when ``argument`` can be coerced to a numbered pitch and when this
        numbered pitch is less or equal to ``argument``.

        ..  container:: example

            >>> pitch_1 = abjad.NumberedPitch(12)
            >>> pitch_2 = abjad.NumberedPitch(12)
            >>> pitch_3 = abjad.NumberedPitch(13)

            >>> pitch_1 <= pitch_1
            True
            >>> pitch_1 <= pitch_2
            True
            >>> pitch_1 <= pitch_3
            True

            >>> pitch_2 <= pitch_1
            True
            >>> pitch_2 <= pitch_2
            True
            >>> pitch_2 <= pitch_3
            True

            >>> pitch_3 <= pitch_1
            False
            >>> pitch_3 <= pitch_2
            False
            >>> pitch_3 <= pitch_3
            True

        """
        try:
            argument = type(self)(argument)
        except (ValueError, TypeError):
            return False
        return self.number <= argument.number

    def __lt__(self, argument) -> bool:
        r"""Is true when ``argument`` can be coerced to a numbered pitch and when this
        numbered pitch is less than ``argument``.

        ..  container:: example

            >>> pitch_1 = abjad.NumberedPitch(12)
            >>> pitch_2 = abjad.NumberedPitch(12)
            >>> pitch_3 = abjad.NumberedPitch(13)

            >>> pitch_1 < pitch_1
            False
            >>> pitch_1 < pitch_2
            False
            >>> pitch_1 < pitch_3
            True

            >>> pitch_2 < pitch_1
            False
            >>> pitch_2 < pitch_2
            False
            >>> pitch_2 < pitch_3
            True

            >>> pitch_3 < pitch_1
            False
            >>> pitch_3 < pitch_2
            False
            >>> pitch_3 < pitch_3
            False

        """
        try:
            argument = type(self)(argument)
        except (ValueError, TypeError):
            return False
        return self.number < argument.number

    def __neg__(self) -> "NumberedPitch":
        """
        Negates numbered pitch.

        ..  container:: example

            >>> -abjad.NumberedPitch(13.5)
            NumberedPitch(-13.5)

            >>> -abjad.NumberedPitch(-13.5)
            NumberedPitch(13.5)

        """
        return type(self)(-self.number)

    def __radd__(self, argument) -> "NumberedPitch":
        """
        Adds numbered pitch to ``argument``.

        ..  container:: example

            >>> pitch = abjad.NumberedPitch(13)
            >>> abjad.NumberedPitch(12).__radd__(pitch)
            NumberedPitch(25)

            >>> pitch = abjad.NumberedPitch(12)
            >>> abjad.NumberedPitch(13).__radd__(pitch)
            NumberedPitch(25)

        """
        argument = type(self)(argument)
        return argument.__add__(self)

    def __repr__(self):
        """
        Gets repr.
        """
        return f"{type(self).__name__}({self.number!r})"

    def __sub__(self, argument) -> "NumberedInterval":
        """
        Subtracts ``argument`` from numbered pitch.

        ..  container:: example

            >>> abjad.NumberedPitch(12) - abjad.NumberedPitch(12)
            NumberedInterval(0)

            >>> abjad.NumberedPitch(12) - abjad.NumberedPitch(13)
            NumberedInterval(1)

            >>> abjad.NumberedPitch(13) - abjad.NumberedPitch(12)
            NumberedInterval(-1)

        """
        if isinstance(argument, type(self)):
            return NumberedInterval.from_pitch_carriers(self, argument)
        interval = NumberedInterval(argument)
        interval = -interval
        return interval.transpose(self)

    def _apply_accidental(self, accidental=None):
        accidental = Accidental(accidental)
        semitones = self.number + accidental.semitones
        return type(self)(semitones)

    def _from_named_parts(self, dpc_number, alteration, octave):
        pc_number = _diatonic_pc_number_to_pitch_class_number[dpc_number]
        pc_number += alteration
        pc_number += (octave - 4) * 12
        self._number = _math.integer_equivalent_number_to_integer(pc_number)
        octave_number, pc_number = divmod(self._number, 12)
        self._pitch_class = NumberedPitchClass(pc_number)
        self._octave = Octave(octave_number + 4)

    def _from_number(self, number):
        self._number = self._to_nearest_quarter_tone(number)
        octave_number, pc_number = divmod(self._number, 12)
        self._octave = Octave(octave_number + 4)
        self._pitch_class = NumberedPitchClass(pc_number)

    def _from_pitch_or_pitch_class(self, pitch_or_pitch_class):
        self._number = self._to_nearest_quarter_tone(float(pitch_or_pitch_class))
        octave_number, pc_number = divmod(self._number, 12)
        self._octave = Octave(octave_number + 4)
        self._pitch_class = NumberedPitchClass(
            pc_number, arrow=pitch_or_pitch_class.arrow
        )

    def _get_diatonic_pc_name(self):
        return self.pitch_class._get_diatonic_pc_name()

    def _get_diatonic_pc_number(self):
        return self.numbered_pitch_class._get_diatonic_pc_number()

    def _get_diatonic_pitch_number(self):
        result = 7 * (self.octave.number - 4)
        result += self._get_diatonic_pc_number()
        return result

    def _get_lilypond_format(self):
        return self.name

    @property
    def accidental(self) -> Accidental:
        """
        Gets accidental of numbered pitch.

        ..  container:: example

            >>> abjad.NumberedPitchClass(13).accidental
            Accidental(name='sharp')

        """
        return self.pitch_class.accidental

    @property
    def arrow(self):
        """
        Gets arrow of numbered pitch.

        ..  container:: example

            >>> abjad.NumberedPitch(13).arrow is None
            True

            >>> abjad.NumberedPitch(13, arrow=abjad.UP).arrow
            <Vertical.UP: 1>

            >>> abjad.NumberedPitch(13, arrow=abjad.DOWN).arrow
            <Vertical.DOWN: -1>

        Returns up, down or none.
        """
        return self._pitch_class.arrow

    @property
    def hertz(self) -> float:
        """
        Gets frequency of numbered pitch in Hertz.

        ..  container:: example

            >>> abjad.NumberedPitch(9).hertz
            440.0

            >>> abjad.NumberedPitch(0).hertz
            261.62...

            >>> abjad.NumberedPitch(12).hertz
            523.25...

        """
        return super().hertz

    @property
    def name(self) -> str:
        """
        Gets name of numbered pitch.

        ..  container:: example

            >>> abjad.NumberedPitch(13).name
            "cs''"

        """
        return f"{self.pitch_class.name}{self.octave.ticks}"

    @property
    def number(self) -> int | float:
        """
        Gets number of numbered pitch.

        ..  container:: example

            >>> abjad.NumberedPitch(13).number
            13

        """
        pc_number = float(self.pitch_class)
        octave_base_pitch = (self.octave.number - 4) * 12
        return _math.integer_equivalent_number_to_integer(pc_number + octave_base_pitch)

    @property
    def octave(self) -> Octave:
        """
        Gets octave of numbered pitch.

        ..  container:: example

            >>> abjad.NumberedPitch(13).octave
            Octave(number=5)

        """
        return self._octave

    @property
    def pitch_class(self) -> NumberedPitchClass:
        """
        Gets pitch-class of numbered pitch.

        ..  container:: example

            >>> abjad.NumberedPitch(13).pitch_class
            NumberedPitchClass(1)

        """
        return self._pitch_class

    @classmethod
    def from_hertz(class_, hertz) -> "NumberedPitch":
        """
        Makes numbered pitch from ``hertz``.

        ..  container:: example

            >>> abjad.NumberedPitch.from_hertz(440)
            NumberedPitch(9)

            REGRESSION. Returns 12 (not 0):

            >>> abjad.NumberedPitch.from_hertz(519)
            NumberedPitch(12)

        """
        return super().from_hertz(hertz)

    def get_name(self, locale: str | None = None) -> str:
        """
        Gets name of numbered pitch name according to ``locale``.

        ..  container:: example

            >>> abjad.NumberedPitch(13).get_name()
            "cs''"

            >>> abjad.NumberedPitch(13).get_name(locale="us")
            'C#5'

        Set ``locale`` to ``"us"`` or none.
        """
        return NamedPitch(self).get_name(locale=locale)

    def interpolate(self, stop_pitch, fraction) -> "NumberedPitch":
        """
        Interpolates between numbered pitch and ``stop_pitch`` by ``fraction``.

        ..  container:: example

            Interpolates from C4 to C5:

            >>> start_pitch = abjad.NumberedPitch(0)
            >>> stop_pitch = abjad.NumberedPitch(12)

            >>> start_pitch.interpolate(stop_pitch, 0)
            NumberedPitch(0)
            >>> start_pitch.interpolate(stop_pitch, (1, 4))
            NumberedPitch(3)
            >>> start_pitch.interpolate(stop_pitch, (1, 2))
            NumberedPitch(6)
            >>> start_pitch.interpolate(stop_pitch, (3, 4))
            NumberedPitch(9)
            >>> start_pitch.interpolate(stop_pitch, 1)
            NumberedPitch(12)

            Interpolates from C5 to C4:

            >>> start_pitch = abjad.NumberedPitch(12)
            >>> stop_pitch = abjad.NumberedPitch(0)

            >>> start_pitch.interpolate(stop_pitch, 0)
            NumberedPitch(12)
            >>> start_pitch.interpolate(stop_pitch, (1, 4))
            NumberedPitch(9)
            >>> start_pitch.interpolate(stop_pitch, (1, 2))
            NumberedPitch(6)
            >>> start_pitch.interpolate(stop_pitch, (3, 4))
            NumberedPitch(3)
            >>> start_pitch.interpolate(stop_pitch, 1)
            NumberedPitch(0)

        """
        try:
            fraction = fractions.Fraction(*fraction)
        except TypeError:
            fraction = fractions.Fraction(fraction)
        assert 0 <= fraction <= 1, repr(fraction)
        stop_pitch = type(self)(stop_pitch)
        distance = stop_pitch - self
        distance = abs(distance.semitones)
        distance = fraction * distance
        distance = int(distance)
        if stop_pitch < self:
            distance *= -1
        pitch_number = self.number
        pitch_number = pitch_number + distance
        pitch = NumberedPitch(pitch_number)
        if self <= stop_pitch:
            triple = (self, pitch, stop_pitch)
            assert self <= pitch <= stop_pitch, triple
        else:
            triple = (self, pitch, stop_pitch)
            assert self >= pitch >= stop_pitch, triple
        return pitch

    def invert(self, axis=None) -> "NumberedPitch":
        """
        Inverts numbered pitch around ``axis``.

        ..  container:: example

            Inverts pitch-class about pitch-class 0 explicitly:

            >>> abjad.NumberedPitch(2).invert(0)
            NumberedPitch(-2)

            >>> abjad.NumberedPitch(-2).invert(0)
            NumberedPitch(2)

            Inverts pitch-class about pitch-class 0 implicitly:

            >>> abjad.NumberedPitch(2).invert()
            NumberedPitch(-2)

            >>> abjad.NumberedPitch(-2).invert()
            NumberedPitch(2)

            Inverts pitch-class about pitch-class -3:

            >>> abjad.NumberedPitch(2).invert(-3)
            NumberedPitch(-8)

        """
        return Pitch.invert(self, axis=axis)

    def multiply(self, n=1) -> "NumberedPitch":
        """
        Multiplies numbered pitch by index ``n``.

        ..  container:: example

            >>> abjad.NumberedPitch(14).multiply(3)
            NumberedPitch(42)

        """
        return super().multiply(n=n)

    def transpose(self, n=0) -> "NumberedPitch":
        """
        Tranposes numbered pitch by ``n`` semitones.

        ..  container:: example

            >>> abjad.NumberedPitch(13).transpose(1)
            NumberedPitch(14)

        """
        interval = NumberedInterval(n)
        return type(self)(float(self) + float(interval))


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class StaffPosition:
    """
    Staff position.

    ..  container:: example

        Middle line of staff:

        >>> abjad.StaffPosition(0)
        StaffPosition(number=0)

        One space below middle line of staff:

        >>> abjad.StaffPosition(-1)
        StaffPosition(number=-1)

        One line below middle line of staff:

        >>> abjad.StaffPosition(-2)
        StaffPosition(number=-2)

    """

    number: int = 0

    def __post_init__(self):
        assert isinstance(self.number, int), repr(self.number)
