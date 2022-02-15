import collections
import copy
import dataclasses
import functools
import importlib
import math
import numbers
import re
import types
import typing

import quicktions

from . import duration as _duration
from . import enumerate as _enumerate
from . import enums as _enums
from . import math as _math
from . import sequence as _sequence
from . import typedcollections as _typedcollections

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

# TODO: possibly remove?
_accidental_abbreviation_to_symbol = {
    "ff": "bb",
    "tqf": "b~",
    "f": "b",
    "qf": "~",
    "": "",
    "qs": "+",
    "s": "#",
    "tqs": "#+",
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

_pitch_class_octave_number_regex_body = (
    "(?P<pitch_class_octave_number>{}{}{})"
).format(
    _diatonic_pc_name_regex_atom,
    _comprehensive_accidental_regex_body,
    _octave_number_regex_atom,
)

_pitch_name_regex_body = ("(?P<pitch_name>{}{}{})").format(
    _diatonic_pc_name_regex_atom,
    _alphabetic_accidental_regex_atom,
    _octave_tick_regex_atom,
)

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

_pitch_class_octave_number_regex = re.compile(
    "^{}$".format(_pitch_class_octave_number_regex_body), re.VERBOSE
)

_pitch_name_regex = re.compile("^{}$".format(_pitch_name_regex_body), re.VERBOSE)

_range_string_regex = re.compile("^{}$".format(_range_string_regex_body), re.VERBOSE)

_interval_name_abbreviation_regex = re.compile(
    "^{}$".format(_interval_name_abbreviation_regex_body), re.VERBOSE
)


@functools.total_ordering
@dataclasses.dataclass(slots=True, unsafe_hash=True)
class Accidental:
    """
    Accidental.

    ..  container:: example

        >>> abjad.Accidental('ff')
        Accidental(name='double flat')

        >>> abjad.Accidental('tqf')
        Accidental(name='three-quarters flat')

        >>> abjad.Accidental('f')
        Accidental(name='flat')

        >>> abjad.Accidental('')
        Accidental(name='natural')

        >>> abjad.Accidental('qs')
        Accidental(name='quarter sharp')

        >>> abjad.Accidental('s')
        Accidental(name='sharp')

        >>> abjad.Accidental('tqs')
        Accidental(name='three-quarters sharp')

        >>> abjad.Accidental('ss')
        Accidental(name='double sharp')

    ..  container:: example

        Generalized accidentals are allowed:

        >>> abjad.Accidental('ssss')
        Accidental(name='ssss')

    ..  container:: example

        Less than is true when ``argument`` is an accidental with semitones greater
        than those of this accidental:

        >>> accidental_1 = abjad.Accidental('f')
        >>> accidental_2 = abjad.Accidental('f')
        >>> accidental_3 = abjad.Accidental('s')

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

        >>> abjad.Accidental('ff').semitones
        -2

        >>> abjad.Accidental('tqf').semitones
        -1.5

        >>> abjad.Accidental('f').semitones
        -1

        >>> abjad.Accidental('').semitones
        0

        >>> abjad.Accidental('qs').semitones
        0.5

        >>> abjad.Accidental('s').semitones
        1

        >>> abjad.Accidental('tqs').semitones
        1.5

        >>> abjad.Accidental('ss').semitones
        2


    ..  container:: example

        >>> abjad.Accidental('ff').name
        'double flat'

        >>> abjad.Accidental('tqf').name
        'three-quarters flat'

        >>> abjad.Accidental('f').name
        'flat'

        >>> abjad.Accidental('').name
        'natural'

        >>> abjad.Accidental('qs').name
        'quarter sharp'

        >>> abjad.Accidental('s').name
        'sharp'

        >>> abjad.Accidental('tqs').name
        'three-quarters sharp'

        >>> abjad.Accidental('ss').name
        'double sharp'

    """

    name: str = "natural"
    arrow: bool | None = dataclasses.field(default=None, repr=False)
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
            self.arrow = _enums.VerticalAlignment.from_expr(self.arrow)
            if self.arrow is _enums.Center:
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

            >>> accidental = abjad.Accidental('qs')

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

        >>> accidental = abjad.Accidental('s')

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

            >>> accidental(abjad.NamedPitchClass('c'))
            NamedPitchClass('cs')

            >>> accidental(abjad.NamedPitchClass('cqs'))
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

            >>> -abjad.Accidental('ff')
            Accidental(name='double sharp')

            >>> -abjad.Accidental('tqf')
            Accidental(name='three-quarters sharp')

            >>> -abjad.Accidental('f')
            Accidental(name='sharp')

            >>> -abjad.Accidental('')
            Accidental(name='natural')

            >>> -abjad.Accidental('qs')
            Accidental(name='quarter flat')

            >>> -abjad.Accidental('s')
            Accidental(name='flat')

            >>> -abjad.Accidental('tqs')
            Accidental(name='three-quarters flat')

            >>> -abjad.Accidental('ss')
            Accidental(name='double flat')

        Returns new accidental.
        """
        return type(self)(-self.semitones)

    def __radd__(self, argument):
        """
        Raises not implemented error on accidental.
        """
        raise NotImplementedError

    def __str__(self):
        """
        Gets string representation of accidental.

        ..  container:: example

            >>> str(abjad.Accidental('ff'))
            'ff'

            >>> str(abjad.Accidental('tqf'))
            'tqf'

            >>> str(abjad.Accidental('f'))
            'f'

            >>> str(abjad.Accidental(''))
            ''

            >>> str(abjad.Accidental('qs'))
            'qs'

            >>> str(abjad.Accidental('s'))
            's'

            >>> str(abjad.Accidental('tqs'))
            'tqs'

            >>> str(abjad.Accidental('ss'))
            'ss'

        Returns string.
        """
        if self.semitones in _accidental_semitones_to_abbreviation:
            return _accidental_semitones_to_abbreviation[self.semitones]
        character = "s"
        if self.semitones < 0:
            character = "f"
        semitones = abs(self.semitones)
        semitones, remainder = divmod(semitones, 1.0)
        abbreviation = character * int(semitones)
        if remainder:
            abbreviation += f"q{character}"
        return abbreviation

    def __sub__(self, argument):
        """
        Subtracts ``argument`` from accidental.

        ..  container:: example

            >>> accidental = abjad.Accidental('qs')

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

            >>> abjad.Accidental('ff').symbol
            'bb'

            >>> abjad.Accidental('tqf').symbol
            'b~'

            >>> abjad.Accidental('f').symbol
            'b'

            >>> abjad.Accidental('').symbol
            ''

            >>> abjad.Accidental('qs').symbol
            '+'

            >>> abjad.Accidental('s').symbol
            '#'

            >>> abjad.Accidental('tqs').symbol
            '#+'

            >>> abjad.Accidental('ss').symbol
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

        Initializes octave from octave-tick string:

        >>> abjad.Octave(",,")
        Octave(number=1)

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
        if isinstance(self.number, str):
            match = _comprehensive_octave_regex.match(self.number)
            group_dict = match.groupdict()
            number = 3
            if group_dict["octave_number"]:
                number = int(group_dict["octave_number"])
            elif group_dict["octave_tick"]:
                if group_dict["octave_tick"].startswith("'"):
                    number += group_dict["octave_tick"].count("'")
                else:
                    number -= group_dict["octave_tick"].count(",")
            self.number = number
        elif isinstance(self.number, (int, float)):
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

    # TODO: remove
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

            >>> abjad.Octave.from_pitch('cs')
            Octave(number=3)

            >>> abjad.Octave.from_pitch("cs'")
            Octave(number=4)

            >>> abjad.Octave.from_pitch(1)
            Octave(number=4)

            >>> abjad.Octave.from_pitch(13)
            Octave(number=5)

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
        elif isinstance(argument, (Interval, IntervalClass)):
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
        return hash(self.__class__.__name__ + str(self))

    def __lt__(self, argument) -> bool:
        """
        Compares ``number``.
        """
        assert isinstance(argument, type(self))
        return self.number < argument.number

    # TODO: remove
    def __str__(self):
        """
        Gets string representation of interval-class.

        Returns string.
        """
        return str(self.number)

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

        >>> abjad.NamedIntervalClass('-M9')
        NamedIntervalClass('-M2')

    """

    __slots__ = ("_number", "_quality")

    def __init__(self, name="P1"):
        super().__init__(name or "P1")

    def __abs__(self):
        """
        Gets absolute value of named interval-class.

        ..  container:: example

            >>> abs(abjad.NamedIntervalClass('-M9'))
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

            >>> interval_class_1 = abjad.NamedIntervalClass('P1')
            >>> interval_class_2 = abjad.NamedIntervalClass('P1')
            >>> interval_class_3 = abjad.NamedIntervalClass('m2')

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

            >>> interval_class_1 = abjad.NamedIntervalClass('P1')
            >>> interval_class_2 = abjad.NamedIntervalClass('P1')
            >>> interval_class_3 = abjad.NamedIntervalClass('m2')

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

    # TODO: remove
    def __str__(self):
        """
        Gets string representation of named interval-class.

        ..  container:: example

            >>> str(abjad.NamedIntervalClass('-M9'))
            '-M2'

        Returns string.
        """
        return self.name

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

            >>> abjad.NamedIntervalClass('P1').direction_number
            0

            >>> abjad.NamedIntervalClass('+M2').direction_number
            1

            >>> abjad.NamedIntervalClass('-M2').direction_number
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

            >>> abjad.NamedIntervalClass('-M9').name
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

        >>> abjad.NamedInversionEquivalentIntervalClass('-m14')
        NamedInversionEquivalentIntervalClass('+M2')

    ..  container:: example

        Initializes from pair:

        >>> abjad.NamedInversionEquivalentIntervalClass(('perfect', 1))
        NamedInversionEquivalentIntervalClass('P1')

        >>> abjad.NamedInversionEquivalentIntervalClass(('perfect', -1))
        NamedInversionEquivalentIntervalClass('P1')

        >>> abjad.NamedInversionEquivalentIntervalClass(('augmented', 4))
        NamedInversionEquivalentIntervalClass('+A4')

        >>> abjad.NamedInversionEquivalentIntervalClass(('augmented', -4))
        NamedInversionEquivalentIntervalClass('+A4')

        >>> abjad.NamedInversionEquivalentIntervalClass(('augmented', 11))
        NamedInversionEquivalentIntervalClass('+A4')

        >>> abjad.NamedInversionEquivalentIntervalClass(('augmented', -11))
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
            >>> interval_class_1 = class_('P1')
            >>> interval_class_2 = class_('P1')
            >>> interval_class_3 = class_('m2')

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
        string = str(named_interval)
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

        >>> abjad.NumberedIntervalClass('-14.5')
        NumberedIntervalClass(-2.5)

        >>> abjad.NumberedIntervalClass('P8')
        NumberedIntervalClass(12)

        >>> abjad.NumberedIntervalClass('-P8')
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

    # TODO: remove
    def __str__(self):
        """
        Gets string representation of numbered interval-class.

        ..  container:: example

            >>> str(abjad.NumberedIntervalClass(-13))
            '-1'

            >>> str(abjad.NumberedIntervalClass(0))
            '0'

            >>> str(abjad.NumberedIntervalClass(13))
            '+1'

        """
        string = super().__str__()
        if 0 < self.number:
            string = "+" + string
        return string

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

        >>> abjad.NumberedInversionEquivalentIntervalClass('1')
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

    # TODO: remove
    def __str__(self):
        """
        Gets string representation of numbered inversion-equivalent
        interval-class.

        ..  container:: example

            >>> str(abjad.NumberedInversionEquivalentIntervalClass(0))
            '0'

            >>> str(abjad.NumberedInversionEquivalentIntervalClass(1.5))
            '1.5'

        Returns string.
        """
        return str(self.number)


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
        Compares string formats.
        """
        if isinstance(argument, type(self)):
            return str(self) == str(argument)
        return False

    def __hash__(self) -> int:
        """
        Hashes interval.
        """
        return hash(self.__class__.__name__ + str(self))

    def __lt__(self, argument):
        """
        Is true when interval is less than ``argument``

        Returns true or false.
        """
        raise NotImplementedError

    # TODO: remove
    def __str__(self):
        """
        Gets string representation of interval.

        Returns string.
        """
        return str(self.number)

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

        >>> abjad.NamedInterval('+M9')
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

        >>> abjad.NamedInterval(('M', 3))
        NamedInterval('+M3')

    """

    __slots__ = ()

    def __init__(self, name="P1"):
        super().__init__(name or "P1")

    def __abs__(self) -> "NamedInterval":
        """
        Gets absolute value of named interval.

        ..  container:: example

            >>> abs(abjad.NamedInterval('+M9'))
            NamedInterval('+M9')

            >>> abs(abjad.NamedInterval('-M9'))
            NamedInterval('+M9')

        """
        return type(self)((self.quality, abs(self.number)))

    def __add__(self, argument) -> "NamedInterval":
        """
        Adds ``argument`` to named interval.

        ..  container:: example

            >>> abjad.NamedInterval('M9') + abjad.NamedInterval('M2')
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

            >>> copy.copy(abjad.NamedInterval('+M9'))
            NamedInterval('+M9')

        """
        return type(self)((self.quality, self.number))

    def __eq__(self, argument) -> bool:
        """
        Compares ``name``.

        ..  container:: example

            >>> interval_1 = abjad.NamedInterval('m2')
            >>> interval_2 = abjad.NamedInterval('m2')
            >>> interval_3 = abjad.NamedInterval('m9')

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

            >>> abjad.NamedInterval('+M9') < abjad.NamedInterval('+M10')
            True

            >>> abjad.NamedInterval('+m9') < abjad.NamedInterval('+M9')
            True

            >>> abjad.NamedInterval('+M9') < abjad.NamedInterval('+M2')
            False

        """
        if isinstance(argument, type(self)):
            return self.semitones < argument.semitones
        return False

    def __mul__(self, argument) -> "NamedInterval":
        """
        Multiplies named interval by ``argument``

        ..  container:: example

            >>> 3 * abjad.NamedInterval('+M9')
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

            >>> -abjad.NamedInterval('+M9')
            NamedInterval('-M9')

            >>> -abjad.NamedInterval('-M9')
            NamedInterval('+M9')

        """
        return type(self)((self.quality, -self.number))

    def __radd__(self, argument) -> "NamedInterval":
        """
        Adds named interval to ``argument``

        ..  container:: example

            >>> abjad.NamedInterval('M9') + abjad.NamedInterval('M2')
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

            >>> abjad.NamedInterval('+M9') * 3
            NamedInterval('+A25')

        """
        return self * argument

    # TODO: remove
    def __str__(self) -> str:
        """
        Gets string representation of named interval.

        ..  container:: example

            >>> str(abjad.NamedInterval('+M9'))
            '+M9'

        """
        return self.name

    def __sub__(self, argument) -> "NamedInterval":
        """
        Subtracts ``argument`` from named interval.

        ..  container:: example

            >>> abjad.NamedInterval('+M9') - abjad.NamedInterval('+M2')
            NamedInterval('+P8')

            >>> abjad.NamedInterval('+M2') - abjad.NamedInterval('+M9')
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

            >>> abjad.NamedInterval('+M9').direction_number
            1

            >>> abjad.NamedInterval('+dim2').direction_number
            1

            >>> abjad.NamedInterval('+A1').direction_number
            1

            >>> abjad.NamedInterval('P1').direction_number
            0

            >>> abjad.NamedInterval('-m3').direction_number
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

            >>> abjad.NamedInterval('+M9').interval_class
            NamedIntervalClass('+M2')

            >>> abjad.NamedInterval('-M9').interval_class
            NamedIntervalClass('-M2')

            >>> abjad.NamedInterval('P1').interval_class
            NamedIntervalClass('P1')

            >>> abjad.NamedInterval('+P8').interval_class
            NamedIntervalClass('+P8')

        """
        return self._interval_class

    @property
    def name(self) -> str:
        """
        Gets name of named interval.

        ..  container:: example

            >>> abjad.NamedInterval('+M9').name
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

            >>> abjad.NamedInterval('+M9').number
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

            >>> abjad.NamedInterval('+M9').semitones
            14

            >>> abjad.NamedInterval('-M9').semitones
            -14

            >>> abjad.NamedInterval('P1').semitones
            0

            >>> abjad.NamedInterval('+P8').semitones
            12

            >>> abjad.NamedInterval('-P8').semitones
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

            >>> abjad.NamedInterval('+M9').staff_spaces
            8

            >>> abjad.NamedInterval('-M9').staff_spaces
            -8

            >>> abjad.NamedInterval('P1').staff_spaces
            0

            >>> abjad.NamedInterval('+P8').staff_spaces
            7

            >>> abjad.NamedInterval('-P8').staff_spaces
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

            >>> abjad.NamedInterval.from_pitch_carriers('c', 'cqs')
            NamedInterval('+P+1')

            >>> abjad.NamedInterval.from_pitch_carriers("cf'", 'bs')
            NamedInterval('-dd2')

            >>> abjad.NamedInterval.from_pitch_carriers("cff'", 'aqs')
            NamedInterval('-ddd+3')

            >>> abjad.NamedInterval.from_pitch_carriers("cff'", 'atqs')
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
        semitones_to_quality: typing.Dict = {
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

            >>> interval = abjad.NamedInterval('+m2')
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

        >>> abjad.NumberedInterval(abjad.NamedInterval('-P4'))
        NumberedInterval(-5)

        Initializes from interval string:

        >>> abjad.NumberedInterval('-P4')
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
        #        if not isinstance(argument, type(self)):
        #            raise TypeError(f"must be numbered interval: {argument!r}.")
        #        if not self.direction_number == argument.direction_number:
        #            raise ValueError("can only compare intervals of same direction.")
        #        return abs(self.number) < abs(argument.number)
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

    # TODO: remove
    def __str__(self):
        """
        Gets string.
        """
        direction_symbol = _direction_number_to_direction_symbol[
            _math.sign(self.number)
        ]
        return f"{direction_symbol}{abs(self.number)}"

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
        elif isinstance(argument, (Pitch, PitchClass)):
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
        Compares string formats.
        """
        if isinstance(argument, type(self)):
            return str(self) == str(argument)
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
        return hash(self.__class__.__name__ + str(self))

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

        >>> abjad.NamedPitchClass('cs')
        NamedPitchClass('cs')

        >>> abjad.NamedPitchClass('cqs')
        NamedPitchClass('cqs')

        Initializes from number of semitones:

        >>> abjad.NamedPitchClass(14)
        NamedPitchClass('d')

        >>> abjad.NamedPitchClass(14.5)
        NamedPitchClass('dqs')

        Initializes from named pitch:

        >>> abjad.NamedPitchClass(abjad.NamedPitch('d'))
        NamedPitchClass('d')

        >>> abjad.NamedPitchClass(abjad.NamedPitch('dqs'))
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

        >>> abjad.NamedPitchClass('C#5')
        NamedPitchClass('cs')

        >>> abjad.NamedPitchClass('Cs5')
        NamedPitchClass('cs')

        Initializes quartertone from pitch-class / octave-number string:

        >>> abjad.NamedPitchClass('C+5')
        NamedPitchClass('cqs')

        >>> abjad.NamedPitchClass('Cqs5')
        NamedPitchClass('cqs')

        Initializes from pitch-class string:

        >>> abjad.NamedPitchClass('C#')
        NamedPitchClass('cs')

        >>> abjad.NamedPitchClass('Cs')
        NamedPitchClass('cs')

        >>> abjad.NamedPitchClass('cs')
        NamedPitchClass('cs')

        Initializes quartertone from pitch-class string

        >>> abjad.NamedPitchClass('C+')
        NamedPitchClass('cqs')

        >>> abjad.NamedPitchClass('Cqs')
        NamedPitchClass('cqs')

        >>> abjad.NamedPitchClass('cqs')
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

            >>> abjad.NamedPitchClass('cs') + abjad.NamedInterval('+M9')
            NamedPitchClass('ds')

            >>> abjad.NamedPitchClass('cs') + abjad.NamedInterval('-M9')
            NamedPitchClass('b')

        """
        dummy_pitch = NamedPitch((self.name, 4))
        pitch = named_interval.transpose(dummy_pitch)
        return type(self)(pitch)

    def __eq__(self, argument) -> bool:
        """
        Compares string formats.

        ..  container:: example

            >>> pitch_class_1 = abjad.NamedPitchClass('cs')
            >>> pitch_class_2 = abjad.NamedPitchClass('cs')
            >>> pitch_class_3 = abjad.NamedPitchClass('df')

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

            >>> abjad.NamedPitchClass('cs') < abjad.NamedPitchClass('d')
            True

            >>> abjad.NamedPitchClass('d') < abjad.NamedPitchClass('cs')
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

    # TODO: remove
    def __str__(self):
        """
        Gets string representation of named pitch-class.

        ..  container:: example

            >>> str(abjad.NamedPitchClass('cs'))
            'cs'

        Returns string.
        """
        return self.name

    def __sub__(self, argument) -> "NamedInversionEquivalentIntervalClass":
        """
        Subtracts ``argument`` from named pitch-class.

        ..  container:: example

            >>> abjad.NamedPitchClass('cs') - abjad.NamedPitchClass('g')
            NamedInversionEquivalentIntervalClass('+A4')

            >>> abjad.NamedPitchClass('c') - abjad.NamedPitchClass('cf')
            NamedInversionEquivalentIntervalClass('+A1')

            >>> abjad.NamedPitchClass('cf') - abjad.NamedPitchClass('c')
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
    def accidental(self) -> Accidental:
        """
        Gets accidental.

        ..  container:: example

            >>> abjad.NamedPitchClass('cs').accidental
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

            >>> abjad.NamedPitchClass('cs').name
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

            >>> abjad.NamedPitchClass('cs').number
            1

        """
        dictionary = _diatonic_pc_number_to_pitch_class_number
        result = dictionary[self._diatonic_pc_number]
        result += self._accidental.semitones
        result %= 12
        return result

    @property
    def pitch_class_label(self) -> str:
        """
        Gets pitch-class label.

        ..  container:: example

            >>> abjad.NamedPitchClass('cs').pitch_class_label
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

            >>> abjad.NamedPitchClass('cs').multiply(3)
            NamedPitchClass('ef')

        """
        return type(self)(n * self.number)

    def transpose(self, n=0) -> "NamedPitchClass":
        """
        Transposes named pitch-class by index named interval ``n``.

        ..  container:: example

            >>> interval = abjad.NamedInterval('-M2')
            >>> abjad.NamedPitchClass('cs').transpose(interval)
            NamedPitchClass('b')

            >>> interval = abjad.NamedInterval('P1')
            >>> abjad.NamedPitchClass('cs').transpose(interval)
            NamedPitchClass('cs')

            >>> interval = abjad.NamedInterval('+M2')
            >>> abjad.NamedPitchClass('cs').transpose(interval)
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

        >>> abjad.NumberedPitchClass('d')
        NumberedPitchClass(2)

        Initializes from named pitch:

        >>> abjad.NumberedPitchClass(abjad.NamedPitch('g,'))
        NumberedPitchClass(7)

        Initializes from numbered pitch:

        >>> abjad.NumberedPitchClass(abjad.NumberedPitch(15))
        NumberedPitchClass(3)

        Initializes from named pitch-class:

        >>> abjad.NumberedPitchClass(abjad.NamedPitchClass('e'))
        NumberedPitchClass(4)

        Initializes from pitch-class / octave string:

        >>> abjad.NumberedPitchClass('C#5')
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
            arrow = _enums.VerticalAlignment.from_expr(arrow)
            if arrow is _enums.Center:
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

    # TODO: remove
    def __str__(self) -> str:
        """
        Gets string.
        """
        return str(self.number)

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
    def accidental(self) -> Accidental:
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
    def pitch_class_label(self) -> str:
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
            _octave = Octave(group_dict.get("comprehensive_octave", "")).number
            self._from_named_parts(_dpc_number, _alteration, _octave)
        elif isinstance(argument, numbers.Number):
            self._from_number(argument)
        elif isinstance(argument, (Pitch, PitchClass)):
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
        return hash(self.__class__.__name__ + str(self))

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


PitchTyping = typing.Union[int, str, Pitch]


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

        >>> abjad.NamedPitch('C#5')
        NamedPitch("cs''")

        Initializes quartertone from pitch-class / octave string:

        >>> abjad.NamedPitch('A+3')
        NamedPitch('aqs')

        >>> abjad.NamedPitch('Aqs3')
        NamedPitch('aqs')

        Initializes arrowed pitch:

        >>> abjad.NamedPitch('C#5', arrow=abjad.Up)
        NamedPitch("cs''", arrow=Up)

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

            >>> abjad.NamedPitch("cs''") + abjad.NamedInterval('-M2')
            NamedPitch("b'")

            >>> abjad.NamedPitch("cs''") + abjad.NamedInterval('P1')
            NamedPitch("cs''")

            >>> abjad.NamedPitch("cs''") + abjad.NamedInterval('+M2')
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

            >>> pitch = abjad.NamedPitch("cs''", arrow=abjad.Up)
            >>> copy.copy(pitch)
            NamedPitch("cs''", arrow=Up)

        """
        return type(self)(self, arrow=self.arrow)

    def __eq__(self, argument) -> bool:
        """
        Is true when ``argument`` is a named pitch equal to this named pitch.

        ..  container:: example

            >>> pitch_1 = abjad.NamedPitch('fs')
            >>> pitch_2 = abjad.NamedPitch('fs')
            >>> pitch_3 = abjad.NamedPitch('gf')

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

            >>> pitch_1 = abjad.NamedPitch('fs')
            >>> pitch_2 = abjad.NamedPitch('fs')
            >>> pitch_3 = abjad.NamedPitch('gf')

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

            >>> pitch_1 = abjad.NamedPitch('fs')
            >>> pitch_2 = abjad.NamedPitch('fs')
            >>> pitch_3 = abjad.NamedPitch('gf')

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

    # TODO: remove
    def __str__(self):
        """
        Gets string representation of named pitch.

        ..  container:: example

            >>> str(abjad.NamedPitch("c''"))
            "c''"

            >>> str(abjad.NamedPitch("cs''"))
            "cs''"

            >>> str(abjad.NamedPitch("df''"))
            "df''"

        """
        return self.name

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
        return str(self)

    def _list_format_contributions(self):
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

            >>> abjad.NamedPitch("cs''", arrow=abjad.Up).arrow
            Up

            >>> abjad.NamedPitch("cs''", arrow=abjad.Down).arrow
            Down

            Displays arrow in interpreter representation:

            >>> abjad.NamedPitch("cs''", arrow=abjad.Down)
            NamedPitch("cs''", arrow=Down)

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
        return f"{self.pitch_class!s}{self.octave!s}"

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

            >>> abjad.NamedPitch("cs''").get_name(locale='us')
            'C#5'

        Set ``locale`` to ``'us'`` or none.
        """
        if locale is None:
            return self.name
        elif locale == "us":
            name = self._get_diatonic_pc_name().upper()
            return f"{name}{self.accidental.symbol}{self.octave.number}"
        else:
            raise ValueError(f"must be 'us' or none: {locale!r}.")

    def invert(self, axis=None) -> "NamedPitch":
        """
        Inverts named pitch around ``axis``.

        ..  container:: example

            Inverts pitch around middle C explicitly:

            >>> abjad.NamedPitch("d'").invert("c'")
            NamedPitch('bf')

            >>> abjad.NamedPitch('bf').invert("c'")
            NamedPitch("d'")

            Inverts pitch around middle C implicitly:

            >>> abjad.NamedPitch("d'").invert()
            NamedPitch('bf')

            >>> abjad.NamedPitch('bf').invert()
            NamedPitch("d'")

            Inverts pitch around A3:

            >>> abjad.NamedPitch("d'").invert('a')
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

            >>> float(abjad.NamedPitch("cfffqf'").simplify()) == float(abjad.NamedPitch('aqf'))
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

            >>> abjad.NamedPitch("c'").transpose(n='m2')
            NamedPitch("df'")

            Transposes C4 down a major second:

            >>> abjad.NamedPitch("c'").transpose(n='-M2')
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
        if isinstance(argument, (int, float)):
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

    # TODO: remove
    def __str__(self):
        """
        Gets string.
        """
        return str(self.number)

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

            >>> abjad.NumberedPitch(13, arrow=abjad.Up).arrow
            Up

            >>> abjad.NumberedPitch(13, arrow=abjad.Down).arrow
            Down

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

    def get_name(self, locale=None) -> str:
        """
        Gets name of numbered pitch name according to ``locale``.

        ..  container:: example

            >>> abjad.NumberedPitch(13).get_name()
            "cs''"

            >>> abjad.NumberedPitch(13).get_name(locale='us')
            'C#5'

        Set ``locale`` to ``'us'`` or none.
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
            fraction = quicktions.Fraction(*fraction)
        except TypeError:
            fraction = quicktions.Fraction(fraction)
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


@functools.total_ordering
class PitchRange:
    r"""
    Pitch range.

    ..  container:: example

        Pitches from C3 to C7, inclusive:

        >>> pitch_range = abjad.PitchRange("[C3, C7]")
        >>> lilypond_file = abjad.illustrate(pitch_range)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            \with
            {
                \override BarLine.stencil = ##f
                \override Glissando.thickness = 2
                \override SpanBar.stencil = ##f
                \override TimeSignature.stencil = ##f
            }
            <<
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        s1 * 1/4
                        s1 * 1/4
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        c1 * 1/4
                        \glissando
                        \change Staff = Treble_Staff
                        c''''1 * 1/4
                    }
                >>
            >>

    ..  container:: example

        Pitches from -39 to 48, inclusive:

        >>> pitch_range = abjad.PitchRange("[-39, 48]")
        >>> lilypond_file = abjad.illustrate(pitch_range)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            \with
            {
                \override BarLine.stencil = ##f
                \override Glissando.thickness = 2
                \override SpanBar.stencil = ##f
                \override TimeSignature.stencil = ##f
            }
            <<
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        s1 * 1/4
                        s1 * 1/4
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        a,,,1 * 1/4
                        \glissando
                        \change Staff = Treble_Staff
                        c'''''1 * 1/4
                    }
                >>
            >>

    ..  container:: example exception

        Errors on mismatched pitch types:

        >>> abjad.PitchRange("[A0, 48]")
        Traceback (most recent call last):
            ...
        Exception: mismatched types: NamedPitch('a,,,') NumberedPitch(48).

    """

    __slots__ = (
        "_close_bracket",
        "_open_bracket",
        "_range_string",
        "_start_pitch",
        "_stop_pitch",
    )

    def __init__(self, range_string="[A0, C8]"):
        if isinstance(range_string, type(self)):
            range_string = range_string.range_string
        assert isinstance(range_string, str), repr(range_string)
        bundle = self._parse_range_string(range_string)
        message = f"mismatched types: {bundle.start_pitch!r} {bundle.stop_pitch!r}."
        if isinstance(bundle.start_pitch, NamedPitch) and isinstance(
            bundle.stop_pitch, NumberedPitch
        ):
            raise Exception(message)
        if isinstance(bundle.stop_pitch, NamedPitch) and isinstance(
            bundle.start_pitch, NumberedPitch
        ):
            raise Exception(message)
        self._close_bracket = bundle.close_bracket
        self._open_bracket = bundle.open_bracket
        self._range_string = bundle.range_string
        self._start_pitch = bundle.start_pitch
        self._stop_pitch = bundle.stop_pitch

    def __contains__(self, argument) -> bool:
        """
        Is true when pitch range contains ``argument``.

        ..  container:: example

            Closed / closed range:

            >>> range_ = abjad.PitchRange("[A0, C8]")

            >>> -99 in range_
            False

            >>> -39 in range_
            True

            >>> 0 in range_
            True

            >>> 48 in range_
            True

            >>> 99 in range_
            False

        ..  container:: example

            Closed / open range:

            >>> range_ = abjad.PitchRange("[A0, C8)")

            >>> -99 in range_
            False

            >>> -39 in range_
            True

            >>> 0 in range_
            True

            >>> 48 in range_
            False

            >>> 99 in range_
            False

        ..  container:: example

            Closed / infinite range:

            >>> range_ = abjad.PitchRange("[-39, +inf]")

            >>> -99 in range_
            False

            >>> -39 in range_
            True

            >>> 0 in range_
            True

            >>> 48 in range_
            True

            >>> 99 in range_
            True

        ..  container:: example

            Open / closed range:

            >>> range_ = abjad.PitchRange("(A0, C8]")

            >>> -99 in range_
            False

            >>> -39 in range_
            False

            >>> 0 in range_
            True

            >>> 48 in range_
            True

            >>> 99 in range_
            False

        ..  container:: example

            Open / open range:

            >>> range_ = abjad.PitchRange("(A0, C8)")

            >>> -99 in range_
            False

            >>> -39 in range_
            False

            >>> 0 in range_
            True

            >>> 48 in range_
            False

            >>> 99 in range_
            False

        ..  container:: example

            Infinite / closed range:

            >>> range_ = abjad.PitchRange("[-inf, C8]")

            >>> -99 in range_
            True

            >>> -39 in range_
            True

            >>> 0 in range_
            True

            >>> 48 in range_
            True

            >>> 99 in range_
            False

        ..  container:: example

            Infinite / open range:

            >>> range_ = abjad.PitchRange("[-inf, C8)")

            >>> -99 in range_
            True

            >>> -39 in range_
            True

            >>> 0 in range_
            True

            >>> 48 in range_
            False

            >>> 99 in range_
            False

        ..  container:: example

            Infinite / infinite range:

            >>> range_ = abjad.PitchRange("[-inf, +inf]")

            >>> -99 in range_
            True

            >>> -39 in range_
            True

            >>> 0 in range_
            True

            >>> 48 in range_
            True

            >>> 99 in range_
            True

        """
        pitch: NamedPitch | NumberedPitch
        start_pitch: NamedPitch | NumberedPitch
        stop_pitch: NamedPitch | NumberedPitch
        if isinstance(argument, (str, NamedPitch)):
            pitch = NamedPitch(argument)
            if self.start_pitch is None:
                start_pitch = NamedPitch(-1000)
            else:
                start_pitch = NamedPitch(self.start_pitch)
            if self.stop_pitch is None:
                stop_pitch = NamedPitch(1000)
            else:
                stop_pitch = NamedPitch(self.stop_pitch)
        elif isinstance(argument, (int, float, NumberedPitch)):
            pitch = NumberedPitch(argument)
            if self.start_pitch is None:
                start_pitch = NumberedPitch(-1000)
            else:
                start_pitch = NumberedPitch(self.start_pitch)
            if self.stop_pitch is None:
                stop_pitch = NumberedPitch(1000)
            else:
                stop_pitch = NumberedPitch(self.stop_pitch)
        else:
            raise Exception(f"must be pitch, number or string: {argument!r}.")
        if self._open_bracket == "[":
            if self._close_bracket == "]":
                return start_pitch <= pitch <= stop_pitch
            else:
                return start_pitch <= pitch < stop_pitch
        else:
            if self._close_bracket == "]":
                return start_pitch < pitch <= stop_pitch
            else:
                return start_pitch < pitch < stop_pitch

    def __eq__(self, argument) -> bool:
        """
        Is true when ``argument`` is a pitch range with ``range_string`` equal to this
        pitch range.

        ..  container:: example

            >>> range_1 = abjad.PitchRange("[-39, 0]")
            >>> range_2 = abjad.PitchRange("[-39, 0]")
            >>> range_3 = abjad.PitchRange("[-39, 48]")

            >>> range_1 == range_1
            True
            >>> range_1 == range_2
            True
            >>> range_1 == range_3
            False

            >>> range_2 == range_1
            True
            >>> range_2 == range_2
            True
            >>> range_2 == range_3
            False

            >>> range_3 == range_1
            False
            >>> range_3 == range_2
            False
            >>> range_3 == range_3
            True

        """
        if isinstance(argument, type(self)):
            return self.range_string == argument.range_string
        return False

    def __hash__(self) -> int:
        """
        Hashes pitch range.
        """
        return hash(repr(self))

    def __lt__(self, argument) -> bool:
        """
        Is true when start pitch of this pitch-range is less than start pitch of
        ``argument`` pitch range.

        ..  container:: example

            >>> range_1 = abjad.PitchRange("[-39, 0]")
            >>> range_2 = abjad.PitchRange("[-39, 0]")
            >>> range_3 = abjad.PitchRange("[-39, 48]")

            >>> range_1 < range_1
            False
            >>> range_1 < range_2
            False
            >>> range_1 < range_3
            True

            >>> range_2 < range_1
            False
            >>> range_2 < range_2
            False
            >>> range_2 < range_3
            True

            >>> range_3 < range_1
            False
            >>> range_3 < range_2
            False
            >>> range_3 < range_3
            False

        """
        assert isinstance(argument, type(self)), repr(argument)
        argument_start_pitch: NamedPitch | NumberedPitch
        argument_stop_pitch: NamedPitch | NumberedPitch
        self_start_pitch: NamedPitch | NumberedPitch
        self_stop_pitch: NamedPitch | NumberedPitch
        if self._is_named() and argument._is_named():
            if self.start_pitch is None:
                self_start_pitch = NamedPitch(-1000)
            else:
                self_start_pitch = NamedPitch(self.start_pitch)
            if self.stop_pitch is None:
                self_stop_pitch = NamedPitch(1000)
            else:
                self_stop_pitch = NamedPitch(self.stop_pitch)
            if argument.start_pitch is None:
                argument_start_pitch = NamedPitch(-1000)
            else:
                argument_start_pitch = NamedPitch(argument.start_pitch)
            if argument.stop_pitch is None:
                argument_stop_pitch = NamedPitch(1000)
            else:
                argument_stop_pitch = NamedPitch(argument.stop_pitch)
        elif self._is_numbered() and argument._is_numbered():
            if self.start_pitch is None:
                self_start_pitch = NumberedPitch(-1000)
            else:
                self_start_pitch = NumberedPitch(self.start_pitch)
            if self.stop_pitch is None:
                self_stop_pitch = NumberedPitch(1000)
            else:
                self_stop_pitch = NumberedPitch(self.stop_pitch)
            if argument.start_pitch is None:
                argument_start_pitch = NumberedPitch(-1000)
            else:
                argument_start_pitch = NumberedPitch(argument.start_pitch)
            if argument.stop_pitch is None:
                argument_stop_pitch = NumberedPitch(1000)
            else:
                argument_stop_pitch = NumberedPitch(argument.stop_pitch)
        else:
            raise Exception(f"mismatched types: {self!r} {argument!r}.")
        if self_start_pitch == argument_start_pitch:
            return self_stop_pitch < argument_stop_pitch
        return self_start_pitch < argument_start_pitch

    def __repr__(self) -> str:
        """
        Gets pitch range interpreter representation.
        """
        return f"{type(self).__name__}(range_string={self.range_string!r})"

    def _is_named(self):
        return isinstance(self.start_pitch, (NamedPitch, type(None))) and isinstance(
            self.stop_pitch, (NamedPitch, type(None))
        )

    def _is_numbered(self):
        return isinstance(self.start_pitch, (NumberedPitch, type(None))) and isinstance(
            self.stop_pitch, (NumberedPitch, type(None))
        )

    def _parse_range_string(self, range_string):
        assert isinstance(range_string, str), repr(range_string)
        range_string = range_string.replace("-inf", "-1000")
        range_string = range_string.replace("+inf", "1000")
        match = _range_string_regex.match(range_string)
        if match is None:
            raise ValueError(f"can not parse range string: {range_string!r}")
        group_dict = match.groupdict()
        open_bracket = group_dict["open_bracket"]
        start_pitch_string = group_dict["start_pitch"]
        stop_pitch_string = group_dict["stop_pitch"]
        close_bracket = group_dict["close_bracket"]
        if start_pitch_string == "-1000":
            start_pitch = None
            start_pitch_repr = "-inf"
        elif start_pitch_string.isnumeric() or start_pitch_string.startswith("-"):
            start_pitch = NumberedPitch(int(start_pitch_string))
            start_pitch_repr = str(start_pitch)
        else:
            start_pitch = NamedPitch(start_pitch_string)
            start_pitch_repr = start_pitch.get_name(locale="us")

        if stop_pitch_string == "1000":
            stop_pitch = None
            stop_pitch_repr = "+inf"
        elif stop_pitch_string.isnumeric() or stop_pitch_string.startswith("-"):
            stop_pitch = NumberedPitch(int(stop_pitch_string))
            stop_pitch_repr = str(stop_pitch)
        else:
            stop_pitch = NamedPitch(stop_pitch_string)
            stop_pitch_repr = stop_pitch.get_name(locale="us")
        start, stop = open_bracket, close_bracket
        normalized_range_string = f"{start}{start_pitch_repr}, {stop_pitch_repr}{stop}"
        return types.SimpleNamespace(
            close_bracket=close_bracket,
            open_bracket=open_bracket,
            range_string=normalized_range_string,
            start_pitch=start_pitch,
            stop_pitch=stop_pitch,
        )

    @property
    def range_string(self) -> str:
        """
        Gets range string of pitch range.

        ..  container:: example

            >>> abjad.PitchRange("[C3, C7]").range_string
            '[C3, C7]'

            >>> abjad.PitchRange("[-inf, C7]").range_string
            '[-inf, C7]'

            >>> abjad.PitchRange("[C3, +inf]").range_string
            '[C3, +inf]'

            >>> abjad.PitchRange("[-inf, +inf]").range_string
            '[-inf, +inf]'

        """
        return self._range_string

    @property
    def start_pitch(self) -> NamedPitch | NumberedPitch | None:
        """
        Start pitch of pitch range.

        ..  container:: example

            >>> abjad.PitchRange("[C3, C7]").start_pitch
            NamedPitch('c')

            >>> abjad.PitchRange("[-inf, C7]").start_pitch is None
            True

        """
        return self._start_pitch

    @property
    def stop_pitch(self) -> NamedPitch | NumberedPitch | None:
        """
        Stop pitch of pitch range.

        ..  container:: example

            >>> abjad.PitchRange("[C3, C7]").stop_pitch
            NamedPitch("c''''")

            >>> abjad.PitchRange("[C8, +inf]").stop_pitch is None
            True

        """
        return self._stop_pitch

    @staticmethod
    def from_octave(octave) -> "PitchRange":
        """
        Initializes pitch range from octave.

        ..  container:: example

            >>> abjad.PitchRange.from_octave(5)
            PitchRange(range_string='[C5, C6)')

        """
        octave = Octave(octave)
        return PitchRange(f"[C{octave.number}, C{octave.number + 1})")

    def voice_pitch_class(self, pitch_class):
        """
        Voices ``pitch_class``.

        ..  container:: example

            Voices C three times:

            >>> pitch_range = abjad.PitchRange("[C4, C6]")
            >>> pitch_range.voice_pitch_class("c")
            (NamedPitch("c'"), NamedPitch("c''"), NamedPitch("c'''"))

            Voices B two times:

            >>> pitch_range = abjad.PitchRange("[C4, C6]")
            >>> pitch_range.voice_pitch_class("b")
            (NamedPitch("b'"), NamedPitch("b''"))

            Returns empty because B can not voice:

            >>> pitch_range = abjad.PitchRange("[C4, A4)")
            >>> pitch_range.voice_pitch_class('b')
            ()

        """
        named_pitch_class = NamedPitchClass(pitch_class)
        pair = (named_pitch_class.name, self.start_pitch.octave.number)
        named_pitch = NamedPitch(pair)
        result = []
        while named_pitch <= self.stop_pitch:
            if named_pitch in self:
                result.append(named_pitch)
            named_pitch += 12
        return tuple(result)


@dataclasses.dataclass(slots=True)
class Segment(_typedcollections.TypedTuple):
    """
    Abstract segment.
    """

    def __post_init__(self):
        prototype = (collections.abc.Iterator, types.GeneratorType)
        if isinstance(self.items, str):
            self.items = self.items.split()
        elif isinstance(self.items, prototype):
            self.items = [_ for _ in self.items]
        if self.item_class is None:
            self.item_class = self._named_item_class
            if self.items is not None:
                if isinstance(
                    self.items, _typedcollections.TypedCollection
                ) and issubclass(self.items.item_class, self._parent_item_class):
                    self.item_class = self.items.item_class
                elif len(self.items):
                    if isinstance(self.items, collections.abc.Set):
                        self.items = tuple(self.items)
                    if isinstance(self.items[0], str):
                        self.item_class = self._named_item_class
                    elif isinstance(self.items[0], (int, float)):
                        self.item_class = self._numbered_item_class
                    elif isinstance(self.items[0], self._parent_item_class):
                        self.item_class = type(self.items[0])
        if isinstance(self.item_class, str):
            abjad = importlib.import_module("abjad")
            globals_ = {"abjad": abjad}
            globals_.update(abjad.__dict__.copy())
            self.item_class = eval(self.item_class, globals_)
        assert issubclass(self.item_class, self._parent_item_class)
        # _typedcollections.TypedTuple.__init__(self, items=items, item_class=item_class)
        _typedcollections.TypedTuple.__post_init__(self)

    def __repr__(self):
        """
        Gets repr.
        """
        item_strings = [str(_) for _ in self.items]
        return f"{type(self).__name__}(items={item_strings}, item_class=abjad.{self.item_class.__name__})"

    def __str__(self) -> str:
        """
        Gets string representation of segment.
        """
        items = [str(_) for _ in self]
        string = ", ".join(items)
        return f"<{string}>"

    def _coerce_item(self, item):
        return self.item_class(item)

    def _get_padded_string(self, width=2):
        strings = []
        for item in self:
            string = f"{item!s:>{width}}"
            strings.append(string)
        string = ", ".join(strings)
        return f"<{string}>"


@dataclasses.dataclass(slots=True)
class IntervalClassSegment(Segment):
    """
    Interval-class segment.

    ..  container:: example

        >>> intervals = 'm2 M10 -aug4 P5'
        >>> abjad.IntervalClassSegment(intervals)
        IntervalClassSegment(items=(NamedIntervalClass('+m2'), NamedIntervalClass('+M3'), NamedIntervalClass('-A4'), NamedIntervalClass('+P5')), item_class=<class 'abjad.pitch.NamedIntervalClass'>)

        >>> intervals = 'P4 P5 P11 P12'
        >>> abjad.IntervalClassSegment(intervals)
        IntervalClassSegment(items=(NamedIntervalClass('+P4'), NamedIntervalClass('+P5'), NamedIntervalClass('+P4'), NamedIntervalClass('+P5')), item_class=<class 'abjad.pitch.NamedIntervalClass'>)

    """

    @property
    def _named_item_class(self):
        return NamedIntervalClass

    @property
    def _numbered_item_class(self):
        return NumberedIntervalClass

    @property
    def _parent_item_class(self):
        return IntervalClass

    @property
    def is_tertian(self) -> bool:
        """
        Is true when all named interval-classes in segment are tertian.

        ..  container:: example

            >>> interval_class_segment = abjad.IntervalClassSegment(
            ...     items=[('major', 3), ('minor', 6), ('major', 6)],
            ...     item_class=abjad.NamedIntervalClass,
            ...     )
            >>> interval_class_segment.is_tertian
            True

        """
        inversion_equivalent_interval_class_segment = dataclasses.replace(
            self, item_class=NamedInversionEquivalentIntervalClass
        )
        for interval in inversion_equivalent_interval_class_segment:
            if not interval.number == 3:
                return False
        return True

    @classmethod
    def from_selection(class_, selection, item_class=None) -> "IntervalClassSegment":
        """
        Initializes interval-class segment from component selection.

        ..  container:: example

            >>> staff_1 = abjad.Staff("c'4 <d' fs' a'>4 b2")
            >>> staff_2 = abjad.Staff("c4. r8 g2")
            >>> selection = abjad.select((staff_1, staff_2))
            >>> abjad.IntervalClassSegment.from_selection(selection)
            IntervalClassSegment(items=(NamedIntervalClass('-M2'), NamedIntervalClass('-M3'), NamedIntervalClass('-m3'), NamedIntervalClass('+m7'), NamedIntervalClass('+M7'), NamedIntervalClass('-P5')), item_class=<class 'abjad.pitch.NamedIntervalClass'>)

        """
        pitch_segment = PitchSegment.from_selection(selection)
        pitches = [_ for _ in pitch_segment]
        intervals = _math.difference_series(pitches)
        return class_(items=intervals, item_class=item_class)

    def has_duplicates(self) -> bool:
        """
        Is true when segment contains duplicates.

        ..  container:: example

            >>> intervals = 'm2 M3 -aug4 m2 P5'
            >>> segment = abjad.IntervalClassSegment(intervals)
            >>> segment.has_duplicates()
            True

            >>> intervals = 'M3 -aug4 m2 P5'
            >>> segment = abjad.IntervalClassSegment(intervals)
            >>> segment.has_duplicates()
            False

        """
        return len(set(self)) < len(self)


@dataclasses.dataclass(slots=True)
class IntervalSegment(Segment):
    """
    Interval segment.

    ..  container:: example

        >>> intervals = 'm2 M10 -aug4 P5'
        >>> abjad.IntervalSegment(intervals)
        IntervalSegment(items=(NamedInterval('+m2'), NamedInterval('+M10'), NamedInterval('-A4'), NamedInterval('+P5')), item_class=<class 'abjad.pitch.NamedInterval'>)

        >>> pitch_segment = abjad.PitchSegment("c d e f g a b c'")
        >>> abjad.IntervalSegment(pitch_segment)
        IntervalSegment(items=(NamedInterval('+M2'), NamedInterval('+M2'), NamedInterval('+m2'), NamedInterval('+M2'), NamedInterval('+M2'), NamedInterval('+M2'), NamedInterval('+m2')), item_class=<class 'abjad.pitch.NamedInterval'>)

    """

    def __post_init__(self):
        if isinstance(self.items, PitchSegment):
            intervals = []
            for one, two in _sequence.Sequence(self.items).nwise():
                intervals.append(one - two)
            self.items = intervals
        Segment.__post_init__(self)

    @property
    def _named_item_class(self):
        return NamedInterval

    @property
    def _numbered_item_class(self):
        return NumberedInterval

    @property
    def _parent_item_class(self):
        return Interval

    @property
    def slope(self):
        """
        Gets slope of interval segment.

        ..  container:: example

            The slope of a interval segment is the sum of its
            intervals divided by its length:

            >>> abjad.IntervalSegment([1, 2]).slope
            Multiplier(3, 2)

        Returns multiplier.
        """
        result = sum([x.number for x in self]) / len(self)
        return _duration.Multiplier.from_float(result)

    @property
    def spread(self):
        """
        Gets spread of interval segment.

        ..  container:: example

            The maximum interval spanned by any combination of
            the intervals within a numbered interval segment.

            >>> abjad.IntervalSegment([1, 2, -3, 1, -2, 1]).spread
            NumberedInterval(4)

            >>> abjad.IntervalSegment([1, 1, 1, 2, -3, -2]).spread
            NumberedInterval(5)

        Returns numbered interval.
        """
        current = maximum = minimum = 0
        for x in self:
            current += float(x.number)
            if maximum < current:
                maximum = current
            if current < minimum:
                minimum = current
        return NumberedInterval(maximum - minimum)

    @classmethod
    def from_selection(class_, selection, item_class=None) -> "IntervalSegment":
        """
        Makes interval segment from component ``selection``.

        ..  container:: example

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
            >>> abjad.IntervalSegment.from_selection(
            ...     abjad.select(staff),
            ...     item_class=abjad.NumberedInterval,
            ... )
            IntervalSegment(items=(NumberedInterval(2), NumberedInterval(2), NumberedInterval(1), NumberedInterval(2), NumberedInterval(2), NumberedInterval(2), NumberedInterval(1)), item_class=<class 'abjad.pitch.NumberedInterval'>)

        """
        pitch_segment = PitchSegment.from_selection(selection)
        pitches = [_ for _ in pitch_segment]
        intervals = (-x for x in _math.difference_series(pitches))
        return class_(items=intervals, item_class=item_class)

    def has_duplicates(self) -> bool:
        """
        Is true if segment has duplicate items.

        ..  container:: example

            >>> intervals = 'm2 M3 -aug4 m2 P5'
            >>> segment = abjad.IntervalSegment(intervals)
            >>> segment.has_duplicates()
            True

            >>> intervals = 'M3 -aug4 m2 P5'
            >>> segment = abjad.IntervalSegment(intervals)
            >>> segment.has_duplicates()
            False

        """
        return len(set(self)) < len(self)

    def rotate(self, n=0):
        """
        Rotates interval segment by index ``n``.

        Returns new interval segment.
        """
        return dataclasses.replace(self, self[-n:] + self[:-n])


@dataclasses.dataclass(slots=True)
class PitchClassSegment(Segment):
    r"""
    Pitch-class segment.

    ..  container:: example

        Initializes segment with numbered pitch-classes:

        >>> items = [-2, -1.5, 6, 7, -1.5, 7]
        >>> segment = abjad.PitchClassSegment(items=items)
        >>> lilypond_file = abjad.illustrate(segment)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> voice = lilypond_file["Voice"]
            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \context Voice = "Voice"
            {
                bf'8
                bqf'8
                fs'8
                g'8
                bqf'8
                g'8
                \bar "|."
                \override Score.BarLine.transparent = ##f
            }

    ..  container:: example

        Initializes segment with named pitch-classes:

        >>> items = ['c', 'ef', 'bqs,', 'd']
        >>> segment = abjad.PitchClassSegment(
        ...     items=items,
        ...     item_class=abjad.NamedPitchClass,
        ...     )
        >>> lilypond_file = abjad.illustrate(segment)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> voice = lilypond_file["Voice"]
            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \context Voice = "Voice"
            {
                c'8
                ef'8
                bqs'8
                d'8
                \bar "|."
                \override Score.BarLine.transparent = ##f
            }

    """

    def __post_init__(self):
        if not self.items and not self.item_class:
            self.item_class = self._named_item_class
        Segment.__post_init__(self)

    def __add__(self, argument) -> "PitchClassSegment":
        r"""
        Adds ``argument`` to segment.

        ..  container:: example

            Example segments:

            >>> pitch_numbers = [-2, -1.5, 6, 7, -1.5, 7]
            >>> abjad.PitchClassSegment(items=pitch_numbers)
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitchClass)

            >>> J = abjad.PitchClassSegment(items=pitch_numbers)
            >>> lilypond_file = abjad.illustrate(J)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> pitch_names = ['c', 'ef', 'bqs,', 'd']
            >>> abjad.PitchClassSegment(items=pitch_names)
            PitchClassSegment(items="c ef bqs d", item_class=NamedPitchClass)

            >>> K = abjad.PitchClassSegment(items=pitch_names)
            >>> lilypond_file = abjad.illustrate(K)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Adds J and K:

            >>> J + K
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7, 0, 3, 11.5, 2], item_class=NumberedPitchClass)

            >>> segment = J + K
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    c'8
                    ef'8
                    bqs'8
                    d'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Adds J repeatedly:

            >>> J + J + J
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7, 10, 10.5, 6, 7, 10.5, 7, 10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitchClass)

            >>> segment = J + J + J
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Adds transformed segments:

            >>> J.rotate(n=1) + K.rotate(n=2)
            PitchClassSegment(items=[7, 10, 10.5, 6, 7, 10.5, 11.5, 2, 0, 3], item_class=NumberedPitchClass)

            >>> segment = J.rotate(n=1) + K.rotate(n=2)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    g'8
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    bqs'8
                    d'8
                    c'8
                    ef'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Reverses result:

            >>> segment = J.rotate(n=1) + K.rotate(n=2)
            >>> segment.retrograde()
            PitchClassSegment(items=[3, 0, 2, 11.5, 10.5, 7, 6, 10.5, 10, 7], item_class=NumberedPitchClass)

            >>> segment = segment.retrograde()
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    ef'8
                    c'8
                    d'8
                    bqs'8
                    bqf'8
                    g'8
                    fs'8
                    bqf'8
                    bf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        """
        argument = type(self)(items=argument)
        items = self.items + argument.items
        return type(self)(items=items)

    def __contains__(self, argument) -> bool:
        r"""
        Is true when pitch-class segment contains ``argument``.

        ..  container:: example

            Example segments:

            >>> pitch_numbers = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(items=pitch_numbers)
            >>> segment
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitchClass)

            >>> abjad.NamedPitch('bf') in segment
            True

            >>> abjad.NamedPitch('cs') in segment
            False

            >>> 'bf' in segment
            True

            >>> 'cs' in segment
            False

            >>> 10 in segment
            True

            >>> 13 in segment
            False

        Returns true or false.
        """
        return Segment.__contains__(self, argument)

    def __getitem__(self, argument):
        r"""
        Gets ``argument`` from segment.

        ..  container:: example

            Example segment:

            >>> pitch_numbers = [-2, -1.5, 6, 7, -1.5, 7]
            >>> abjad.PitchClassSegment(items=pitch_numbers)
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitchClass)

            >>> J = abjad.PitchClassSegment(items=pitch_numbers)
            >>> lilypond_file = abjad.illustrate(J)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Gets item at nonnegative index:

            >>> J[0]
            NumberedPitchClass(10)

        ..  container:: example

            Gets item at negative index:

            >>> J[-1]
            NumberedPitchClass(7)

        ..  container:: example

            Gets slice:

            >>> J[:4]
            PitchClassSegment(items=[10, 10.5, 6, 7], item_class=NumberedPitchClass)

            >>> segment = J[:4]
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Gets retrograde of slice:

            >>> J[:4].retrograde()
            PitchClassSegment(items=[7, 6, 10.5, 10], item_class=NumberedPitchClass)

            >>> segment = J[:4].retrograde()
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    g'8
                    fs'8
                    bqf'8
                    bf'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Gets slice of retrograde:

            >>> J.retrograde()[:4]
            PitchClassSegment(items=[7, 10.5, 7, 6], item_class=NumberedPitchClass)

            >>> segment = J.retrograde()[:4]
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    g'8
                    bqf'8
                    g'8
                    fs'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Returns pitch-class or pitch-class segment:

            >>> isinstance(segment, abjad.PitchClassSegment)
            True

        """
        return Segment.__getitem__(self, argument)

    def __mul__(self, n) -> "PitchClassSegment":
        r"""
        Multiplies pitch-class segment by ``n``.

        ..  container:: example

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> 2 * abjad.PitchClassSegment(items=items)
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7, 10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitchClass)

        """
        return Segment.__mul__(self, n)

    def __repr__(self) -> str:
        r"""
        Gets interpreter representation.

        ..  container:: example

            Interpreter representation:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> abjad.PitchClassSegment(items=items)
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitchClass)

        """
        if self.item_class is NamedPitchClass:
            contents = " ".join([str(_) for _ in self])
            contents = '"' + contents + '"'
        else:
            contents = ", ".join([str(_) for _ in self])
            contents = "[" + contents + "]"
        return f"{type(self).__name__}(items={contents}, item_class={self.item_class.__name__})"

    def __rmul__(self, n) -> "PitchClassSegment":
        r"""
        Multiplies ``n`` by pitch-class segment.

        ..  container:: example

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> abjad.PitchClassSegment(items=items) * 2
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7, 10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitchClass)

        """
        return Segment.__rmul__(self, n)

    def __str__(self) -> str:
        r"""
        Gets string representation of pitch-class segment.

        ..  container::

            >>> segment = abjad.PitchClassSegment([-2, -1.5, 6, 7, -1.5, 7])
            >>> str(segment)
            'PC<10, 10.5, 6, 7, 10.5, 7>'

            Gets string represenation of named pitch class:

            >>> segment = abjad.PitchClassSegment(
            ...     items=[-2, -1.5, 6, 7, -1.5, 7],
            ...     item_class=abjad.NamedPitchClass,
            ...     )
            >>> str(segment)
            'PC<bf bqf fs g bqf g>'

        """
        items = [str(_) for _ in self]
        separator = " "
        if self.item_class is NumberedPitchClass:
            separator = ", "
        return f"PC<{separator.join(items)}>"

    @property
    def _named_item_class(self):
        return NamedPitchClass

    @property
    def _numbered_item_class(self):
        return NumberedPitchClass

    @property
    def _parent_item_class(self):
        return PitchClass

    def _get_padded_string(self, width=2):
        string = Segment._get_padded_string(self, width=width)
        return "PC<" + string[1:-1] + ">"

    def _is_equivalent_under_transposition(self, argument):
        if not isinstance(argument, type(self)):
            return False
        if not len(self) == len(argument):
            return False
        difference = -(
            NamedPitch((argument[0].name, 4)) - NamedPitch((self[0].name, 4))
        )
        new_pitch_classes = (x + difference for x in self)
        new_pitch_classes = dataclasses.replace(self, items=new_pitch_classes)
        return argument == new_pitch_classes

    @staticmethod
    def _make_rotate_method_name(n=0):
        return "r"

    def _transpose_to_zero(self):
        numbers = [_.number for _ in self]
        first_number = self[0].number
        numbers = [pc.number - first_number for pc in self]
        pcs = [_ % 12 for _ in numbers]
        return type(self)(items=pcs, item_class=self.item_class)

    def count(self, item) -> int:
        """
        Counts ``item`` in segment.

        ..  container:: example

            Example segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            Counts existing item in segment:

            >>> segment.count(-1.5)
            2

            Counts nonexisting item in segment:

            >>> segment.count('text')
            0

            Returns nonnegative integer:

            >>> isinstance(segment.count('text'), int)
            True

        """
        return Segment.count(self, item)

    @classmethod
    def from_selection(class_, selection, item_class=None) -> "PitchClassSegment":
        """
        Initializes segment from ``selection``.

        ..  container:: example

            Initializes from selection:

            >>> staff_1 = abjad.Staff("c'4 <d' fs' a'>4 b2")
            >>> staff_2 = abjad.Staff("c4. r8 g2")
            >>> staff_group = abjad.StaffGroup([staff_1, staff_2])
            >>> abjad.show(staff_group) # doctest: +SKIP

            >>> selection = abjad.select((staff_1, staff_2))
            >>> segment = abjad.PitchClassSegment.from_selection(selection)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            Returns pitch-class segment:

            >>> segment
            PitchClassSegment(items="c d fs a b c g", item_class=NamedPitchClass)

        """
        pitch_segment = PitchSegment.from_selection(selection)
        return class_(items=pitch_segment, item_class=item_class)

    def has_duplicates(self) -> bool:
        """
        Is true when segment contains duplicate items.

        ..  container:: example

            Has duplicates:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> segment.has_duplicates()
            True

            Has no duplicates:

            >>> items = "c d e f g a b"
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> segment.has_duplicates()
            False

        """
        return len(set(self)) < len(self)

    def index(self, item):
        """
        Gets index of ``item`` in segment.

        ..  container:: example

            Example segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            Gets index of first item in segment:

            >>> segment.index(-2)
            0

            Gets index of second item in segment:

            >>> segment.index(-1.5)
            1

            Returns nonnegative integer:

            >>> isinstance(segment.index(-1.5), int)
            True

        """
        return Segment.index(self, item)

    def invert(self, axis=None) -> "PitchClassSegment":
        r"""
        Inverts segment.

        ..  container:: example

            Example segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> J = abjad.PitchClassSegment(items=items)
            >>> J
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitchClass)

            >>> lilypond_file = abjad.illustrate(J)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            Inverts segment:

            >>> J.invert()
            PitchClassSegment(items=[2, 1.5, 6, 5, 1.5, 5], item_class=NumberedPitchClass)

            >>> segment = J.invert()
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    d'8
                    dqf'8
                    fs'8
                    f'8
                    dqf'8
                    f'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            Inverts inversion of segment:

            >>> J.invert().invert()
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitchClass)

            >>> segment = J.invert().invert()
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment == J
            True

        """
        items = [_.invert(axis=axis) for _ in self]
        return type(self)(items=items)

    def multiply(self, n=1) -> "PitchClassSegment":
        r"""
        Multiplies pitch-classes in segment by ``n``.

        ..  container:: example

            Example segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> J = abjad.PitchClassSegment(items=items)
            >>> J
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitchClass)

            >>> lilypond_file = abjad.illustrate(J)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            Multiplies pitch-classes in segment by 1:

            >>> J.multiply(n=1)
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitchClass)

            >>> segment = J.multiply(n=1)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            Multiplies pitch-classes in segment by 5:

            >>> J.multiply(n=5)
            PitchClassSegment(items=[2, 4.5, 6, 11, 4.5, 11], item_class=NumberedPitchClass)

            >>> segment = J.multiply(n=5)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    d'8
                    eqs'8
                    fs'8
                    b'8
                    eqs'8
                    b'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            Multiplies pitch-classes in segment by 7:

            >>> J.multiply(n=7)
            PitchClassSegment(items=[10, 1.5, 6, 1, 1.5, 1], item_class=NumberedPitchClass)

            >>> segment = J.multiply(n=7)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    dqf'8
                    fs'8
                    cs'8
                    dqf'8
                    cs'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            Multiplies pitch-classes in segment by 11:

            >>> segment = J.multiply(n=11)
            >>> segment
            PitchClassSegment(items=[2, 7.5, 6, 5, 7.5, 5], item_class=NumberedPitchClass)

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    d'8
                    gqs'8
                    fs'8
                    f'8
                    gqs'8
                    f'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        """
        items = [NumberedPitchClass(_) for _ in self]
        items = [_.multiply(n) for _ in items]
        return type(self)(items=items)

    def permute(self, row=None) -> "PitchClassSegment":
        r"""
        Permutes segment by twelve-tone ``row``.

        ..  container:: example

            >>> abjad.PitchClassSegment([-2, -1, 6, 7, -1, 7])
            PitchClassSegment(items=[10, 11, 6, 7, 11, 7], item_class=NumberedPitchClass)

            >>> segment = abjad.PitchClassSegment([-2, -1, 6, 7, -1, 7])
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  doctest:

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    b'8
                    fs'8
                    g'8
                    b'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment.permute([10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11])
            PitchClassSegment(items=[4, 11, 5, 3, 11, 3], item_class=NumberedPitchClass)

            >>> segment = segment.permute([10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11])
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    e'8
                    b'8
                    f'8
                    ef'8
                    b'8
                    ef'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        """
        row = TwelveToneRow(items=row)
        items = row(self)
        return type(self)(items=items)

    def retrograde(self) -> "PitchClassSegment":
        r"""
        Gets retrograde of segment.

        ..  container:: example

            Example segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> J = abjad.PitchClassSegment(items=items)
            >>> J
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitchClass)

            >>> lilypond_file = abjad.illustrate(J)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            Gets retrograde of segment:

            >>> segment = J.retrograde()
            >>> segment
            PitchClassSegment(items=[7, 10.5, 7, 6, 10.5, 10], item_class=NumberedPitchClass)

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    g'8
                    bqf'8
                    g'8
                    fs'8
                    bqf'8
                    bf'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            Gets retrograde of retrograde of segment:

            >>> segment = J.retrograde().retrograde()
            >>> segment
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitchClass)

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment == J
            True

        """
        return type(self)(items=reversed(self.items))

    def rotate(self, n=0) -> "PitchClassSegment":
        r"""
        Rotates segment by index ``n``.

        ..  container:: example

            Example segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> J = abjad.PitchClassSegment(items=items)
            >>> J
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitchClass)

            >>> lilypond_file = abjad.illustrate(J)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            Rotates segment to the right:

            >>> J.rotate(n=1)
            PitchClassSegment(items=[7, 10, 10.5, 6, 7, 10.5], item_class=NumberedPitchClass)

            >>> segment = J.rotate(n=1)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    g'8
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            Rotates segment to the left:

            >>> J.rotate(n=-1)
            PitchClassSegment(items=[10.5, 6, 7, 10.5, 7, 10], item_class=NumberedPitchClass)

            >>> segment = J.rotate(n=-1)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    bf'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            Rotates segment by zero:

            >>> J.rotate(n=0)
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitchClass)

            >>> segment = J.rotate(n=0)
            >>> lilypond_file = abjad.illustrate(J)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment == J
            True

        """
        items = _sequence.Sequence(self.items).rotate(n=n)
        return type(self)(items=items)

    def to_pitch_classes(self) -> "PitchClassSegment":
        r"""
        Changes to pitch-classes.

        ..  container:: example

            To numbered pitch-class segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> segment
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitchClass)

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment = segment.to_pitch_classes()
            >>> segment
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitchClass)

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            To named pitch-class segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(
            ...     items=items,
            ...     item_class=abjad.NamedPitchClass,
            ...     )
            >>> segment
            PitchClassSegment(items="bf bqf fs g bqf g", item_class=NamedPitchClass)

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment = segment.to_pitch_classes()
            >>> segment
            PitchClassSegment(items="bf bqf fs g bqf g", item_class=NamedPitchClass)

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        Returns new segment.
        """
        return type(self)(self)

    def to_pitches(self) -> "PitchSegment":
        r"""
        Changes to pitches.

        ..  container:: example

            To numbered pitch segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> segment
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitchClass)

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment = segment.to_pitches()
            >>> segment
            PitchSegment(items=[10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitch)

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        bf'1 * 1/8
                        bqf'1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        bqf'1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

        ..  container:: example

            To named pitch segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(
            ...     items=items,
            ...     item_class=abjad.NamedPitchClass,
            ...     )
            >>> segment
            PitchClassSegment(items="bf bqf fs g bqf g", item_class=NamedPitchClass)

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment = segment.to_pitches()
            >>> segment
            PitchSegment(items="bf' bqf' fs' g' bqf' g'", item_class=NamedPitch)

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        bf'1 * 1/8
                        bqf'1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        bqf'1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

        """
        class_ = Pitch
        item_class = class_._to_pitch_item_class(self.item_class)
        return PitchSegment(items=self.items, item_class=item_class)

    def transpose(self, n=0) -> "PitchClassSegment":
        r"""
        Transposes segment by index ``n``.

        ..  container:: example

            Example segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> J = abjad.PitchClassSegment(items=items)
            >>> J
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitchClass)

            >>> lilypond_file = abjad.illustrate(J)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Transposes segment by positive index:

            >>> J.transpose(n=13)
            PitchClassSegment(items=[11, 11.5, 7, 8, 11.5, 8], item_class=NumberedPitchClass)

            >>> segment = J.transpose(n=13)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    b'8
                    bqs'8
                    g'8
                    af'8
                    bqs'8
                    af'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Transposes segment by negative index:

            >>> J.transpose(n=-13)
            PitchClassSegment(items=[9, 9.5, 5, 6, 9.5, 6], item_class=NumberedPitchClass)

            >>> segment = J.transpose(n=-13)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    a'8
                    aqs'8
                    f'8
                    fs'8
                    aqs'8
                    fs'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Transposes segment by zero index:

            >>> J.transpose(n=0)
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitchClass)

            >>> segment = J.transpose(n=0)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment == J
            True

        """
        items = [_.transpose(n=n) for _ in self]
        return type(self)(items=items)

    def voice_horizontally(self, initial_octave=4) -> "PitchSegment":
        r"""
        Voices segment with each pitch as close to the previous pitch as possible.

        ..  todo:: Should be implemented somewhere else.

        ..  container:: example

            Voices horizontally:

            >>> items = "c b d e f g e b a c"
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> voiced_segment = segment.voice_horizontally()
            >>> lilypond_file = abjad.illustrate(voiced_segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                \with
                {
                    \override BarLine.stencil = ##f
                    \override Rest.transparent = ##t
                    \override SpanBar.stencil = ##f
                    \override TimeSignature.stencil = ##f
                }
                <<
                    \context PianoStaff = "Piano_Staff"
                    <<
                        \context Staff = "Treble_Staff"
                        {
                            \clef "treble"
                            c'1 * 1/8
                            b1 * 1/8
                            d'1 * 1/8
                            e'1 * 1/8
                            f'1 * 1/8
                            g'1 * 1/8
                            e'1 * 1/8
                            b1 * 1/8
                            r1 * 1/8
                            c'1 * 1/8
                        }
                        \context Staff = "Bass_Staff"
                        {
                            \clef "bass"
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            a1 * 1/8
                            r1 * 1/8
                        }
                    >>
                >>

        """
        initial_octave = Octave(initial_octave)
        pitches = []
        if self:
            pitch_class = NamedPitchClass(self[0])
            # pitch = NamedPitch((pitch_class.name, initial_octave))
            pitch = NamedPitch((pitch_class.name, initial_octave)).number
            pitches.append(pitch)
            for pitch_class in self[1:]:
                pitch_class = NamedPitchClass(pitch_class)
                # pitch = NamedPitch((pitch_class.name, initial_octave))
                pitch = NamedPitch((pitch_class.name, initial_octave)).number
                # semitones = abs((pitch - pitches[-1]).semitones)
                semitones = abs((pitch - pitches[-1]))
                while 6 < semitones:
                    if pitch < pitches[-1]:
                        pitch += 12
                    else:
                        pitch -= 12
                    # semitones = abs((pitch - pitches[-1]).semitones)
                    semitones = abs((pitch - pitches[-1]))
                pitches.append(pitch)
        if self.item_class is NamedPitchClass:
            segment = PitchSegment(items=pitches, item_class=NamedPitch)
        else:
            segment = PitchSegment(items=pitches, item_class=NumberedPitch)
        return segment

    def voice_vertically(self, initial_octave=4) -> "PitchSegment":
        r"""
        Voices segment with each pitch higher than the previous.

        ..  todo:: Should be implemented somewhere else.

        ..  container:: example

            Voices vertically:

            >>> string = "c' ef' g' bf' d'' f'' af''"
            >>> segment = abjad.PitchClassSegment(string)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> voiced_segment = segment.voice_vertically()
            >>> lilypond_file = abjad.illustrate(voiced_segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                \with
                {
                    \override BarLine.stencil = ##f
                    \override Rest.transparent = ##t
                    \override SpanBar.stencil = ##f
                    \override TimeSignature.stencil = ##f
                }
                <<
                    \context PianoStaff = "Piano_Staff"
                    <<
                        \context Staff = "Treble_Staff"
                        {
                            \clef "treble"
                            c'1 * 1/8
                            ef'1 * 1/8
                            g'1 * 1/8
                            bf'1 * 1/8
                            d''1 * 1/8
                            f''1 * 1/8
                            af''1 * 1/8
                        }
                        \context Staff = "Bass_Staff"
                        {
                            \clef "bass"
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                        }
                    >>
                >>

        """
        initial_octave = Octave(initial_octave)
        pitches = []
        if self:
            pitch_class = NamedPitchClass(self[0])
            pitch = NamedPitch((pitch_class.name, initial_octave))
            pitches.append(pitch)
            for pitch_class in self[1:]:
                pitch_class = NamedPitchClass(pitch_class)
                pitch = NamedPitch((pitch_class.name, initial_octave))
                while pitch < pitches[-1]:
                    pitch += 12
                pitches.append(pitch)
        if self.item_class is NamedPitchClass:
            segment = PitchSegment(items=pitches, item_class=NamedPitch)
        else:
            segment = PitchSegment(items=pitches, item_class=NumberedPitch)
        return segment


@dataclasses.dataclass(slots=True)
class PitchSegment(Segment):
    r"""
    Pitch segment.

    ..  container:: example

        Numbered pitch segment:

        >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

        >>> str(segment)
        '<-2, -1.5, 6, 7, -1.5, 7>'

        >>> lilypond_file = abjad.illustrate(segment)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> staff_group = lilypond_file["Piano_Staff"]
            >>> string = abjad.lilypond(staff_group)
            >>> print(string)
            \context PianoStaff = "Piano_Staff"
            <<
                \context Staff = "Treble_Staff"
                {
                    \clef "treble"
                    r1 * 1/8
                    r1 * 1/8
                    fs'1 * 1/8
                    g'1 * 1/8
                    r1 * 1/8
                    g'1 * 1/8
                }
                \context Staff = "Bass_Staff"
                {
                    \clef "bass"
                    bf1 * 1/8
                    bqf1 * 1/8
                    r1 * 1/8
                    r1 * 1/8
                    bqf1 * 1/8
                    r1 * 1/8
                }
            >>

    ..  container:: example

        Named pitch segment:

        >>> segment = abjad.PitchSegment("bf, aqs fs' g' bqf g'")

        >>> str(segment)
        "<bf, aqs fs' g' bqf g'>"

        >>> lilypond_file = abjad.illustrate(segment)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> staff_group = lilypond_file["Piano_Staff"]
            >>> string = abjad.lilypond(staff_group)
            >>> print(string)
            \context PianoStaff = "Piano_Staff"
            <<
                \context Staff = "Treble_Staff"
                {
                    \clef "treble"
                    r1 * 1/8
                    r1 * 1/8
                    fs'1 * 1/8
                    g'1 * 1/8
                    r1 * 1/8
                    g'1 * 1/8
                }
                \context Staff = "Bass_Staff"
                {
                    \clef "bass"
                    bf,1 * 1/8
                    aqs1 * 1/8
                    r1 * 1/8
                    r1 * 1/8
                    bqf1 * 1/8
                    r1 * 1/8
                }
            >>

    ..  container:: example

        Built-in max() works:

        >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])
        >>> max(segment)
        NumberedPitch(7)

        Built-in min() works:

        >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])
        >>> min(segment)
        NumberedPitch(-2)

    """

    def __post_init__(self):
        if not self.items and not self.item_class:
            self.item_class = self._named_item_class
        Segment.__post_init__(self)

    def __contains__(self, argument):
        """
        Is true when pitch segment contains ``argument``.

        ..  container:: example

            Numbered pitch segment:

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> abjad.NamedPitch('fs') in segment
            False

            >>> 6 in segment
            True

            >>> abjad.NamedPitch('f') in segment
            False

            >>> 5 in segment
            False

        Returns true or false.
        """
        return Segment.__contains__(self, argument)

    def __repr__(self) -> str:
        """
        Gets repr.
        """
        if self.item_class is NamedPitch:
            contents = " ".join([str(_) for _ in self])
            contents = '"' + contents + '"'
        else:
            contents = ", ".join([str(_) for _ in self])
            contents = "[" + contents + "]"
        return f"{type(self).__name__}(items={contents}, item_class={self.item_class.__name__})"

    def __str__(self) -> str:
        """
        Gets pitch segment string.

        ..  container:: example

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> str(segment)
            '<-2, -1.5, 6, 7, -1.5, 7>'

        ..  container:: example

            >>> segment = abjad.PitchSegment("bf, aqs fs' g' bqf g'")

            >>> str(segment)
            "<bf, aqs fs' g' bqf g'>"

        """
        items = [str(_) for _ in self]
        separator = " "
        if self.item_class is NumberedPitch:
            separator = ", "
        return f"<{separator.join(items)}>"

    @property
    def _named_item_class(self):
        return NamedPitch

    @property
    def _numbered_item_class(self):
        return NumberedPitch

    @property
    def _parent_item_class(self):
        return Pitch

    def _is_equivalent_under_transposition(self, argument):
        if not isinstance(argument, type(self)):
            return False
        if not len(self) == len(argument):
            return False
        difference = -(NamedPitch(argument[0], 4) - NamedPitch(self[0], 4))
        new_pitches = (x + difference for x in self)
        new_pitches = dataclasses.replace(self, items=new_pitches)
        return argument == new_pitches

    @property
    def hertz(self) -> list[float]:
        """
        Gets Hertz of pitches in segment.

        ..  container:: example

            >>> segment = abjad.PitchSegment('c e g b')
            >>> segment.hertz
            [130.81..., 164.81..., 195.99..., 246.94...]

        """
        return [_.hertz for _ in self]

    @property
    def inflection_point_count(self) -> int:
        r"""
        Gets segment inflection point count.

        ..  container:: example

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment.inflection_point_count
            2

        """
        return len(self.local_minima) + len(self.local_maxima)

    @property
    def local_maxima(self):
        r"""
        Gets segment local maxima.

        ..  container:: example

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment.local_maxima
            [NumberedPitch(7)]

        Returns list.
        """
        result = []
        if 3 <= len(self):
            for i in range(1, len(self) - 1):
                left, middle, right = self[i - 1], self[i], self[i + 1]
                if left < middle and right < middle:
                    result.append(middle)
        return result

    @property
    def local_minima(self):
        r"""
        Gets segment local minima.

        ..  container:: example

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment.local_minima
            [NumberedPitch(-1.5)]

        Returns list.
        """
        result = []
        if 3 <= len(self):
            for i in range(1, len(self) - 1):
                left, middle, right = self[i - 1], self[i], self[i + 1]
                if middle < left and middle < right:
                    result.append(middle)
        return result

    @classmethod
    def from_selection(class_, selection, item_class=None) -> "PitchSegment":
        r"""
        Makes pitch segment from ``selection``.

        ..  container:: example

            >>> staff_1 = abjad.Staff("c'4 <d' fs' a'>4 b2")
            >>> staff_2 = abjad.Staff("c4. r8 g2")
            >>> selection = abjad.select((staff_1, staff_2))
            >>> segment = abjad.PitchSegment.from_selection(selection)

            >>> str(segment)
            "<c' d' fs' a' b c g>"

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        c'1 * 1/8
                        d'1 * 1/8
                        fs'1 * 1/8
                        a'1 * 1/8
                        b1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        c1 * 1/8
                        g1 * 1/8
                    }
                >>

        """
        assert hasattr(selection, "_pitch_segment"), repr(selection)
        pitch_segment = selection._pitch_segment()
        return class_(items=pitch_segment, item_class=item_class)

    def has_duplicates(self) -> bool:
        """
        Is true when segment has duplicates.

        ..  container:: example

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])
            >>> segment.has_duplicates()
            True

        ..  container:: example

            >>> segment = abjad.PitchSegment("c d e f g a b")
            >>> segment.has_duplicates()
            False

        """
        return len(set(self)) < len(self)

    def invert(self, axis=None) -> "PitchSegment":
        r"""
        Inverts pitch segment about ``axis``.

        ..  container:: example

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment = segment.invert(axis=0)

            >>> str(segment)
            '<2, 1.5, -6, -7, 1.5, -7>'

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        d'1 * 1/8
                        dqf'1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        dqf'1 * 1/8
                        r1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        fs1 * 1/8
                        f1 * 1/8
                        r1 * 1/8
                        f1 * 1/8
                    }
                >>

        """
        items = [_.invert(axis=axis) for _ in self]
        return dataclasses.replace(self, items=items)

    def multiply(self, n=1) -> "PitchSegment":
        r"""
        Multiplies pitch segment by index ``n``.

        ..  container:: example

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment = segment.multiply(n=3)

            >>> str(segment)
            '<-6, -4.5, 18, 21, -4.5, 21>'

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs''1 * 1/8
                        a''1 * 1/8
                        r1 * 1/8
                        a''1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        fs1 * 1/8
                        gqs1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        gqs1 * 1/8
                        r1 * 1/8
                    }
                >>

        """
        items = [_.multiply(n=n) for _ in self]
        return dataclasses.replace(self, items=items)

    def retrograde(self) -> "PitchSegment":
        r"""
        Retrograde of pitch segment.

        ..  container:: example

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment = segment.retrograde()

            >>> str(segment)
            '<7, -1.5, 7, 6, -1.5, -2>'

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                        fs'1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        bf1 * 1/8
                    }
                >>

        """
        return dataclasses.replace(self, items=reversed(self))

    def rotate(self, n=0) -> "PitchSegment":
        r"""
        Rotates pitch segment by index ``n``.

        ..  container:: example

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment = segment.rotate(n=1)

            >>> str(segment)
            '<7, -2, -1.5, 6, 7, -1.5>'

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        g'1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                    }
                >>

        """
        rotated_pitches = _sequence.Sequence(self.items).rotate(n=n)
        new_segment = dataclasses.replace(self, items=rotated_pitches)
        return new_segment

    def to_pitch_classes(self) -> "PitchClassSegment":
        r"""
        Changes to pitch-classes.

        ..  container:: example

            To numbered pitch-class segment:

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment = segment.to_pitch_classes()

            >>> str(segment)
            'PC<10, 10.5, 6, 7, 10.5, 7>'

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            To named pitch-class segment:

            >>> segment = abjad.PitchSegment("bf, aqs fs' g' bqf g'")

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf,1 * 1/8
                        aqs1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment = segment.to_pitch_classes()

            >>> str(segment)
            'PC<bf aqs fs g bqf g>'

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    aqs'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        """
        class_ = Pitch
        item_class = class_._to_pitch_class_item_class(self.item_class)
        return PitchClassSegment(items=self.items, item_class=item_class)

    def to_pitches(self) -> "PitchSegment":
        r"""
        Changes to pitches.

        ..  container:: example

            To numbered pitch segment:

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment = segment.to_pitches()

            >>> str(segment)
            '<-2, -1.5, 6, 7, -1.5, 7>'

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

        ..  container:: example

            To named pitch segment:

            >>> segment = abjad.PitchSegment("bf, aqs fs' g' bqf g'")

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf,1 * 1/8
                        aqs1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment = segment.to_pitches()

            >>> str(segment)
            "<bf, aqs fs' g' bqf g'>"

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf,1 * 1/8
                        aqs1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

        """
        return dataclasses.replace(self)

    def transpose(self, n=0) -> "PitchSegment":
        r"""
        Transposes pitch segment by index ``n``.

        ..  container:: example

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment = segment.transpose(n=11)

            >>> str(segment)
            '<9, 9.5, 17, 18, 9.5, 18>'

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        a'1 * 1/8
                        aqs'1 * 1/8
                        f''1 * 1/8
                        fs''1 * 1/8
                        aqs'1 * 1/8
                        fs''1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

        """
        items = [_.transpose(n=n) for _ in self]
        return dataclasses.replace(self, items=items)


@dataclasses.dataclass(slots=True)
class TwelveToneRow(PitchClassSegment):
    """
    Twelve-tone row.

    ..  container:: example

        Initializes from defaults:

        >>> row = abjad.TwelveToneRow()
        >>> lilypond_file = abjad.illustrate(row)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        Initializes from integers:

        >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
        >>> row = abjad.TwelveToneRow(numbers)
        >>> lilypond_file = abjad.illustrate(row)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        Interpreter representation:

        >>> row
        TwelveToneRow(items=(NumberedPitchClass(1), NumberedPitchClass(11), NumberedPitchClass(9), NumberedPitchClass(3), NumberedPitchClass(6), NumberedPitchClass(7), NumberedPitchClass(5), NumberedPitchClass(4), NumberedPitchClass(10), NumberedPitchClass(2), NumberedPitchClass(8), NumberedPitchClass(0)), item_class=<class 'abjad.pitch.NumberedPitchClass'>)

    """

    items: typing.Any = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)

    def __post_init__(self):
        assert self.items is not None
        PitchClassSegment.__post_init__(self)
        self._validate_pitch_classes(self)

    def __call__(self, pitch_classes):
        r"""
        Calls row on ``pitch_classes``.

        ..  container:: example

            Example row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Permutes pitch-classes:

            >>> row([abjad.NumberedPitchClass(2)])
            [NumberedPitchClass(9)]

            >>> row([abjad.NumberedPitchClass(3)])
            [NumberedPitchClass(3)]

            >>> row([abjad.NumberedPitchClass(4)])
            [NumberedPitchClass(6)]

        ..  container:: example

            Permutes pitch-class segment:

            >>> items = [-2, -1, 6, 7, -1, 7]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> segment_ = row(segment)
            >>> lilypond_file = abjad.illustrate(segment_)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    af'8
                    c'8
                    f'8
                    e'8
                    c'8
                    e'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Permutes row:

            >>> numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
            >>> row_2 = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(row_2)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    c'8
                    cs'8
                    d'8
                    ef'8
                    e'8
                    f'8
                    fs'8
                    g'8
                    af'8
                    a'8
                    bf'8
                    b'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> row_3 = row(row_2)
            >>> lilypond_file = abjad.illustrate(row_3)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    cs'8
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Permutes row:

            >>> numbers = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
            >>> row_2 = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(row_2)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    b'8
                    bf'8
                    a'8
                    af'8
                    g'8
                    fs'8
                    f'8
                    e'8
                    ef'8
                    d'8
                    cs'8
                    c'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> row_3 = row(row_2)
            >>> lilypond_file = abjad.illustrate(row_3)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    c'8
                    af'8
                    d'8
                    bf'8
                    e'8
                    f'8
                    g'8
                    fs'8
                    ef'8
                    a'8
                    b'8
                    cs'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Permutes row:

            >>> numbers = [10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11]
            >>> row_2 = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(row_2)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    c'8
                    d'8
                    fs'8
                    af'8
                    g'8
                    f'8
                    ef'8
                    cs'8
                    a'8
                    e'8
                    b'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> row_3 = row(row_2)
            >>> lilypond_file = abjad.illustrate(row_3)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    af'8
                    cs'8
                    a'8
                    f'8
                    bf'8
                    e'8
                    g'8
                    ef'8
                    b'8
                    d'8
                    fs'8
                    c'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        Returns permuted pitch-classes in object of type ``pitch_classes``.
        """
        new_pitch_classes = []
        for pitch_class in pitch_classes:
            pitch_class = NumberedPitchClass(pitch_class)
            i = pitch_class.number
            new_pitch_class = self[i]
            new_pitch_classes.append(new_pitch_class)
        result = type(pitch_classes)(new_pitch_classes)
        return result

    def __getitem__(self, argument):
        r"""
        Gets item or slice identified by ``argument``.

        ..  container:: example

            Example row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Gets first hexachord:

            >>> lilypond_file = abjad.illustrate(row[:6])
            >>> abjad.show(lilypond_file) # doctest: +SKIP
            PitchClassSegment([0, 1, 11, 9, 3, 6])

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    cs'8
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Gets second hexachord:

            >>> lilypond_file = abjad.illustrate(row[-6:])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Gets items in row:

            >>> row = abjad.TwelveToneRow()
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP


            >>> for item in row.items:
            ...     item
            ...
            NumberedPitchClass(0)
            NumberedPitchClass(1)
            NumberedPitchClass(2)
            NumberedPitchClass(3)
            NumberedPitchClass(4)
            NumberedPitchClass(5)
            NumberedPitchClass(6)
            NumberedPitchClass(7)
            NumberedPitchClass(8)
            NumberedPitchClass(9)
            NumberedPitchClass(10)
            NumberedPitchClass(11)

            Gets items in row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> for item in row.items:
            ...     item
            ...
            NumberedPitchClass(1)
            NumberedPitchClass(11)
            NumberedPitchClass(9)
            NumberedPitchClass(3)
            NumberedPitchClass(6)
            NumberedPitchClass(7)
            NumberedPitchClass(5)
            NumberedPitchClass(4)
            NumberedPitchClass(10)
            NumberedPitchClass(2)
            NumberedPitchClass(8)
            NumberedPitchClass(0)

        """
        item = self.items.__getitem__(argument)
        try:
            return PitchClassSegment(items=item, item_class=NumberedPitchClass)
        except TypeError:
            return item

    def __mul__(self, argument) -> "PitchClassSegment":
        r"""
        Multiplies row by ``argument``.

        ..  container:: example

            Multiplies row:

            >>> row = abjad.TwelveToneRow()
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> segment = 2 * row
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    c'8
                    cs'8
                    d'8
                    ef'8
                    e'8
                    f'8
                    fs'8
                    g'8
                    af'8
                    a'8
                    bf'8
                    b'8
                    c'8
                    cs'8
                    d'8
                    ef'8
                    e'8
                    f'8
                    fs'8
                    g'8
                    af'8
                    a'8
                    bf'8
                    b'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Multiplies row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> segment = 2 * row
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP


            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    cs'8
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    cs'8
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        """
        return PitchClassSegment(self) * argument

    def __rmul__(self, argument) -> "PitchClassSegment":
        r"""
        Multiplies ``argument`` by row.

        ..  container:: example

            Multiplies integer by row:

            >>> row = abjad.TwelveToneRow()
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> segment = row * 2
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    c'8
                    cs'8
                    d'8
                    ef'8
                    e'8
                    f'8
                    fs'8
                    g'8
                    af'8
                    a'8
                    bf'8
                    b'8
                    c'8
                    cs'8
                    d'8
                    ef'8
                    e'8
                    f'8
                    fs'8
                    g'8
                    af'8
                    a'8
                    bf'8
                    b'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Multiplies integer by row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> segment = row * 2
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    cs'8
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    cs'8
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        """
        return PitchClassSegment(self) * argument

    @property
    def _contents_string(self):
        return ", ".join([str(abs(pc)) for pc in self])

    @staticmethod
    def _validate_pitch_classes(pitch_classes):
        numbers = [pc.number for pc in pitch_classes]
        numbers.sort()
        if not numbers == list(range(12)):
            message = f"must contain all twelve pitch-classes: {pitch_classes!r}."
            raise ValueError(message)

    def count(self, item) -> int:
        """
        Counts ``item`` in row.

        ..  container:: example

            Example row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Counts pitch-class 11 in row:

            >>> row.count(11)
            1

        ..  container:: example

            Counts pitch-class 9 in row:

            >>> row.count(9)
            1

        ..  container:: example

            Counts string in row:

            >>> row.count('text')
            0

        """
        return PitchClassSegment.count(self, item)

    @classmethod
    def from_selection(class_, selection, item_class=None):
        """
        Makes row from ``selection``.

        Not yet implemented.

        Returns twelve-tone row.
        """
        raise NotImplementedError

    def has_duplicates(self) -> bool:
        """
        Is false for all rows.

        ..  container:: example

            Is false:

            >>> row = abjad.TwelveToneRow()
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> row.has_duplicates()
            False

        ..  container:: example

            Is false:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> row.has_duplicates()
            False

        Twelve-tone rows have no duplicates.
        """
        return PitchClassSegment.has_duplicates(self)

    def index(self, item):
        """
        Gets index of ``item`` in row.

        ..  container:: example

            Example row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Gets index of pitch-class 11:

            >>> row.index(11)
            1

        ..  container:: example

            Gets index of pitch-class 9:

            >>> row.index(9)
            2

        ..  container:: example

            Returns nonnegative integer less than 12:

            >>> isinstance(row.index(9), int)
            True

        """
        return PitchClassSegment.index(self, item)

    def invert(self, axis=None) -> "TwelveToneRow":
        r"""
        Inverts row about optional ``axis``.

        ..  container:: example

            Example row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Inverts row about first pitch-class when ``axis`` is none:

            >>> inversion = row.invert()
            >>> lilypond_file = abjad.illustrate(inversion)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    cs'8
                    ef'8
                    f'8
                    b'8
                    af'8
                    g'8
                    a'8
                    bf'8
                    e'8
                    c'8
                    fs'8
                    d'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            First pitch-classes are equal:

            >>> row[0] == inversion[0]
            True

        ..  container:: example

            Inverts row about pitch-class 1:

            >>> inversion = row.invert(axis=1)
            >>> lilypond_file = abjad.illustrate(inversion)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    cs'8
                    ef'8
                    f'8
                    b'8
                    af'8
                    g'8
                    a'8
                    bf'8
                    e'8
                    c'8
                    fs'8
                    d'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            Same result as above.

        ..  container:: example

            Inverts row about pitch-class 0:

            >>> inversion = row.invert(axis=0)
            >>> lilypond_file = abjad.illustrate(inversion)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    b'8
                    cs'8
                    ef'8
                    a'8
                    fs'8
                    f'8
                    g'8
                    af'8
                    d'8
                    bf'8
                    e'8
                    c'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Inverts row about pitch-class 5:

            >>> inversion = row.invert(axis=5)
            >>> lilypond_file = abjad.illustrate(inversion)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    a'8
                    b'8
                    cs'8
                    g'8
                    e'8
                    ef'8
                    f'8
                    fs'8
                    c'8
                    af'8
                    d'8
                    bf'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        """
        if axis is None:
            axis = self[0]
        items = [pc.invert(axis=axis) for pc in self]
        return dataclasses.replace(self, items=items)

    def multiply(self, n=1) -> "TwelveToneRow":
        r"""
        Multiplies pitch-classes in row by ``n``.

        ..  container:: example

            Example row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Multiplies pitch-classes in row by 5:

            >>> multiplication = row.multiply(n=5)
            >>> lilypond_file = abjad.illustrate(multiplication)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    f'8
                    g'8
                    a'8
                    ef'8
                    fs'8
                    b'8
                    cs'8
                    af'8
                    d'8
                    bf'8
                    e'8
                    c'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Multiplies pitch-classes in row by 7:

            >>> multiplication = row.multiply(n=7)
            >>> lilypond_file = abjad.illustrate(multiplication)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    g'8
                    f'8
                    ef'8
                    a'8
                    fs'8
                    cs'8
                    b'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Multiplies pitch-classes in row by 1:

            >>> multiplication = row.multiply(n=1)
            >>> lilypond_file = abjad.illustrate(multiplication)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    cs'8
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        """
        return type(self)(PitchClassSegment.multiply(self, n=n))

    def retrograde(self) -> "TwelveToneRow":
        r"""
        Gets retrograde of row.

        ..  container:: example

            Example row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Gets retrograde of row:

            >>> retrograde = row.retrograde()
            >>> lilypond_file = abjad.illustrate(retrograde)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    c'8
                    af'8
                    d'8
                    bf'8
                    e'8
                    f'8
                    g'8
                    fs'8
                    ef'8
                    a'8
                    b'8
                    cs'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Gets retrograde of retrograde of row:

            >>> retrograde = row.retrograde().retrograde()
            >>> lilypond_file = abjad.illustrate(retrograde)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    cs'8
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> retrograde == row
            True

        """
        return type(self)(PitchClassSegment.retrograde(self))

    def rotate(self, n=0) -> "TwelveToneRow":
        r"""
        Rotates row by index ``n``.

        ..  container:: example

            Example row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Rotates row to the right:

            >>> rotation = row.rotate(n=1)
            >>> lilypond_file = abjad.illustrate(rotation)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    c'8
                    cs'8
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Rotates row to the left:

            >>> rotation = row.rotate(n=-1)
            >>> lilypond_file = abjad.illustrate(rotation)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    cs'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Rotates row by zero:

            >>> rotation = row.rotate(n=0)
            >>> lilypond_file = abjad.illustrate(rotation)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    cs'8
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> rotation == row
            True

        """
        return type(self)(PitchClassSegment.rotate(self, n=n))

    def transpose(self, n=0) -> "TwelveToneRow":
        r"""
        Transposes row by index ``n``.

        ..  container:: example

            Example row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Transposes row by positive index:

            >>> transposition = row.transpose(n=13)
            >>> lilypond_file = abjad.illustrate(transposition)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    d'8
                    c'8
                    bf'8
                    e'8
                    g'8
                    af'8
                    fs'8
                    f'8
                    b'8
                    ef'8
                    a'8
                    cs'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Transposes row by negative index:

            >>> transposition = row.transpose(n=-13)
            >>> lilypond_file = abjad.illustrate(transposition)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    c'8
                    bf'8
                    af'8
                    d'8
                    f'8
                    fs'8
                    e'8
                    ef'8
                    a'8
                    cs'8
                    g'8
                    b'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Transposes row by zero index:

            >>> transposition = row.transpose(n=0)
            >>> lilypond_file = abjad.illustrate(transposition)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    cs'8
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> transposition == row
            True

        """
        return type(self)(PitchClassSegment.transpose(self, n=n))


@dataclasses.dataclass(slots=True)
class Set(_typedcollections.TypedFrozenset):
    """
    Abstract set.
    """

    def __post_init__(self):
        if isinstance(self.items, str):
            self.items = self.items.split()
        elif isinstance(self.items, (collections.abc.Iterator, types.GeneratorType)):
            self.items = [item for item in self.items]
        if self.item_class is None:
            self.item_class = self._named_item_class
            if self.items is not None:
                if isinstance(
                    self.items, _typedcollections.TypedCollection
                ) and issubclass(self.items.item_class, self._parent_item_class):
                    self.item_class = self.items.item_class
                elif len(self.items):
                    if isinstance(self.items, collections.abc.Set):
                        self.items = tuple(self.items)
                    if isinstance(self.items[0], str):
                        self.item_class = self._named_item_class
                    elif isinstance(self.items[0], (int, float)):
                        self.item_class = self._numbered_item_class
                    elif isinstance(self.items[0], self._parent_item_class):
                        self.item_class = type(self.items[0])
        assert issubclass(self.item_class, self._parent_item_class)
        _typedcollections.TypedFrozenset.__post_init__(self)

    def __repr__(self):
        """
        Gets repr of set.
        """
        return f"{type(self).__name__}(items={self._get_sorted_repr_items()}, item_class=abjad.{self.item_class.__name__})"

    def _sort_self(self):
        return tuple(self)

    @property
    def cardinality(self):
        """
        Gets cardinality of set.

        Defined equal to length of set.

        Returns nonnegative integer.
        """
        return len(self)


@dataclasses.dataclass(slots=True)
class IntervalClassSet(Set):
    """
    Interval-class set.
    """

    def __post_init__(self):
        prototype = (
            PitchClassSegment,
            PitchSegment,
            PitchClassSet,
            PitchSet,
        )
        if isinstance(self.items, prototype):
            self.items = list(self.items)
            pairs = _enumerate.yield_pairs(self.items)
            self.items = [second - first for first, second in pairs]
        Set.__post_init__(self)

    @property
    def _named_item_class(self):
        return NamedIntervalClass

    @property
    def _numbered_item_class(self):
        return NumberedIntervalClass

    @property
    def _parent_item_class(self):
        return IntervalClass

    @classmethod
    def from_selection(class_, selection, item_class=None) -> "IntervalClassSet":
        r"""
        Initialize interval set from component selection:

        ..  container:: example

            ::

                >>> staff_1 = abjad.Staff("c'4 <d' fs' a'>4 b2")
                >>> staff_2 = abjad.Staff("c4. r8 g2")
                >>> staff_group = abjad.StaffGroup([staff_1, staff_2])
                >>> abjad.show(staff_group) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \new StaffGroup
                <<
                    \new Staff
                    {
                        c'4
                        <d' fs' a'>4
                        b2
                    }
                    \new Staff
                    {
                        c4.
                        r8
                        g2
                    }
                >>

            ::

                >>> selection = abjad.select(staff_group)
                >>> interval_classes = abjad.IntervalClassSet.from_selection(selection)
                >>> for interval_class in sorted(interval_classes):
                ...     interval_class
                ...
                NamedIntervalClass('-M6')
                NamedIntervalClass('-P5')
                NamedIntervalClass('-A4')
                NamedIntervalClass('-M3')
                NamedIntervalClass('-m3')
                NamedIntervalClass('-M2')
                NamedIntervalClass('+m2')
                NamedIntervalClass('+M2')
                NamedIntervalClass('+m3')
                NamedIntervalClass('+M3')
                NamedIntervalClass('+P4')
                NamedIntervalClass('+A4')
                NamedIntervalClass('+P5')
                NamedIntervalClass('+M6')
                NamedIntervalClass('+m7')
                NamedIntervalClass('+M7')
                NamedIntervalClass('+P8')

        """
        interval_set = IntervalSet.from_selection(selection)
        return class_(items=interval_set, item_class=item_class)


@dataclasses.dataclass(slots=True)
class IntervalSet(Set):
    """
    Interval set.
    """

    def __post_init__(self):
        prototype = (
            PitchClassSegment,
            PitchClassSet,
            PitchSegment,
            PitchSet,
        )
        if isinstance(self.items, prototype):
            self.items = list(self.items)
            pairs = _enumerate.yield_pairs(self.items)
            self.items = [second - first for first, second in pairs]
        Set.__post_init__(self)

    @property
    def _named_item_class(self):
        return NamedInterval

    @property
    def _numbered_item_class(self):
        return NumberedInterval

    @property
    def _parent_item_class(self):
        return Interval

    @classmethod
    def from_selection(class_, selection, item_class=None) -> "IntervalSet":
        """
        Initializes interval set from component selection.

        ..  container:: example

            >>> staff_1 = abjad.Staff("c'4 <d' fs' a'>4 b2")
            >>> staff_2 = abjad.Staff("c4. r8 g2")
            >>> selection = abjad.select((staff_1, staff_2))
            >>> intervals = abjad.IntervalSet.from_selection(selection)
            >>> for interval in sorted(intervals):
            ...     interval
            ...
            NamedInterval('-M6')
            NamedInterval('-P5')
            NamedInterval('-A4')
            NamedInterval('-M3')
            NamedInterval('-m3')
            NamedInterval('-M2')
            NamedInterval('+m2')
            NamedInterval('+m3')
            NamedInterval('+M3')
            NamedInterval('+P4')
            NamedInterval('+P5')
            NamedInterval('+m7')
            NamedInterval('+M7')
            NamedInterval('+P8')
            NamedInterval('+M9')
            NamedInterval('+A11')
            NamedInterval('+M13')

        """
        pitch_segment = PitchSegment.from_selection(selection)
        pairs = _enumerate.yield_pairs(pitch_segment)
        intervals = [second - first for first, second in pairs]
        return class_(items=intervals, item_class=item_class)


@dataclasses.dataclass(slots=True, unsafe_hash=True)
class PitchClassSet(Set):
    """
    Pitch-class set.

    ..  container:: example

        Initializes numbered pitch-class set:

        >>> numbered_pitch_class_set = abjad.PitchClassSet(
        ...     items=[-2, -1.5, 6, 7, -1.5, 7],
        ...     item_class=abjad.NumberedPitchClass,
        ...     )
        >>> numbered_pitch_class_set
        PitchClassSet(items=[6, 7, 10, 10.5], item_class=abjad.NumberedPitchClass)

    ..  container:: example

        Initializes named pitch-class set:

        >>> named_pitch_class_set = abjad.PitchClassSet(
        ...     items=['c', 'ef', 'bqs,', 'd'],
        ...     item_class=abjad.NamedPitchClass,
        ...     )
        >>> named_pitch_class_set
        PitchClassSet(items=['c', 'd', 'ef', 'bqs'], item_class=abjad.NamedPitchClass)

    """

    def __repr__(self):
        """
        Gets repr of pitch-class set.
        """
        return f"{type(self).__name__}(items={self._get_sorted_repr_items()}, item_class=abjad.{self.item_class.__name__})"

    def __contains__(self, argument):
        """
        Is true when pitch-class set contains ``argument``.

        ..  container:: example

            Initializes numbered pitch-class set:

            >>> set_ = abjad.PitchClassSet(
            ...     items=[-2, -1.5, 6, 7, -1.5, 7],
            ...     item_class=abjad.NumberedPitchClass,
            ...     )
            >>> set_
            PitchClassSet(items=[6, 7, 10, 10.5], item_class=abjad.NumberedPitchClass)

            >>> abjad.NamedPitch('fs') in set_
            True

            >>> abjad.NamedPitch('f') in set_
            False

            >>> 6 in set_
            True

            >>> 5 in set_
            False

        Returns true or false.
        """
        return Set.__contains__(self, argument)

    def __str__(self) -> str:
        """
        Gets string representation of pitch-class set.

        ..  container:: example

            Gets string of set sorted at initialization:

            >>> pc_set = abjad.PitchClassSet([6, 7, 10, 10.5])
            >>> str(pc_set)
            'PC{6, 7, 10, 10.5}'

        ..  container:: example

            Gets string of set not sorted at initialization:

            >>> pc_set = abjad.PitchClassSet([10.5, 10, 7, 6])
            >>> str(pc_set)
            'PC{6, 7, 10, 10.5}'

        """
        items = [str(_) for _ in sorted(self)]
        separator = " "
        if self.item_class is NumberedPitchClass:
            separator = ", "
        return f"PC{{{separator.join(items)}}}"

    @property
    def _named_item_class(self):
        return NamedPitchClass

    @property
    def _numbered_item_class(self):
        return NumberedPitchClass

    @property
    def _parent_item_class(self):
        return PitchClass

    @staticmethod
    def _get_most_compact_ordering(candidates):
        widths = []
        for candidate in candidates:
            if candidate[0] < candidate[-1]:
                width = abs(candidate[-1] - candidate[0])
            else:
                width = abs(candidate[-1] + 12 - candidate[0])
            widths.append(width)
        minimum_width = min(widths)
        candidates_ = []
        for candidate, width in zip(candidates, widths):
            if width == minimum_width:
                candidates_.append(candidate)
        candidates = candidates_
        assert 1 <= len(candidates)
        if len(candidates) == 1:
            segment = candidates[0]
            segment = PitchClassSegment(items=segment, item_class=NumberedPitchClass)
            return segment
        for i in range(len(candidates[0]) - 1):
            widths = []
            for candidate in candidates:
                stop = i + 1
                if candidate[0] < candidate[stop]:
                    width = abs(candidate[stop] - candidate[0])
                else:
                    width = abs(candidate[stop] + 12 - candidate[0])
                widths.append(width)
            minimum_width = min(widths)
            candidates_ = []
            for candidate, width in zip(candidates, widths):
                if width == minimum_width:
                    candidates_.append(candidate)
            candidates = candidates_
            if len(candidates) == 1:
                segment = candidates[0]
                segment = PitchClassSegment(
                    items=segment, item_class=NumberedPitchClass
                )
                return segment
        candidates.sort(key=lambda x: x[0])
        segment = candidates[0]
        segment = PitchClassSegment(items=segment, item_class=NumberedPitchClass)
        return segment

    @classmethod
    def from_selection(class_, selection, item_class=None) -> "PitchClassSet":
        """
        Makes pitch-class set from ``selection``.

        ..  container:: example

            >>> staff_1 = abjad.Staff("c'4 <d' fs' a'>4 b2")
            >>> staff_2 = abjad.Staff("c4. r8 g2")
            >>> selection = abjad.select((staff_1, staff_2))
            >>> abjad.PitchClassSet.from_selection(selection)
            PitchClassSet(items=['c', 'd', 'fs', 'g', 'a', 'b'], item_class=abjad.NamedPitchClass)

        """
        pitch_segment = PitchSegment.from_selection(selection)
        return class_(items=pitch_segment, item_class=item_class)

    def get_normal_order(self) -> "PitchClassSegment":
        """
        Gets normal order.

        ..  container:: example

            Gets normal order of empty pitch-class set:

            >>> pc_set = abjad.PitchClassSet()
            >>> pc_set.get_normal_order()
            PitchClassSegment(items=[], item_class=NumberedPitchClass)

        ..  container:: example

            Gets normal order:

            >>> pc_set = abjad.PitchClassSet([0, 1, 10, 11])
            >>> pc_set.get_normal_order()
            PitchClassSegment(items=[10, 11, 0, 1], item_class=NumberedPitchClass)

        ..  container:: example

            Gets normal order:

            >>> pc_set = abjad.PitchClassSet([2, 8, 9])
            >>> pc_set.get_normal_order()
            PitchClassSegment(items=[8, 9, 2], item_class=NumberedPitchClass)

        ..  container:: example

            Gets normal order of pitch-class set with degree of symmetry equal
            to 2:

            >>> pc_set = abjad.PitchClassSet([1, 2, 7, 8])
            >>> pc_set.get_normal_order()
            PitchClassSegment(items=[1, 2, 7, 8], item_class=NumberedPitchClass)

        ..  container:: example

            Gets normal order of pitch-class set with degree of symmetry equal
            to 4:

            >>> pc_set = abjad.PitchClassSet([0, 3, 6, 9])
            >>> pc_set.get_normal_order()
            PitchClassSegment(items=[0, 3, 6, 9], item_class=NumberedPitchClass)

        """
        if not len(self):
            return PitchClassSegment(items=None, item_class=NumberedPitchClass)
        pitch_classes = list(self)
        pitch_classes.sort()
        candidates = []
        for i in range(self.cardinality):
            candidate_list = [NumberedPitch(_) for _ in pitch_classes]
            candidate = _sequence.Sequence(candidate_list).rotate(n=-i)
            candidates.append(candidate)
        return self._get_most_compact_ordering(candidates)

    def get_prime_form(self, transposition_only=False) -> "PitchClassSet":
        """
        Gets prime form.

        ..  container:: example

            Gets prime form of empty pitch-class set:

            >>> pc_set = abjad.PitchClassSet()
            >>> pc_set.get_prime_form()
            PitchClassSet(items=[], item_class=abjad.NamedPitchClass)

            >>> pc_set = abjad.PitchClassSet()
            >>> pc_set.get_prime_form(transposition_only=True)
            PitchClassSet(items=[], item_class=abjad.NamedPitchClass)

        ..  container:: example

            Gets prime form:

            >>> pc_set = abjad.PitchClassSet([0, 1, 10, 11])
            >>> pc_set.get_prime_form()
            PitchClassSet(items=[0, 1, 2, 3], item_class=abjad.NumberedPitchClass)

            >>> pc_set = abjad.PitchClassSet([0, 1, 10, 11])
            >>> pc_set.get_prime_form(transposition_only=True)
            PitchClassSet(items=[0, 1, 2, 3], item_class=abjad.NumberedPitchClass)

        ..  container:: example

            Gets prime form:

            >>> pc_set = abjad.PitchClassSet([2, 8, 9])
            >>> pc_set.get_prime_form()
            PitchClassSet(items=[0, 1, 6], item_class=abjad.NumberedPitchClass)

            >>> pc_set = abjad.PitchClassSet([2, 8, 9])
            >>> pc_set.get_prime_form(transposition_only=True)
            PitchClassSet(items=[0, 1, 6], item_class=abjad.NumberedPitchClass)

        ..  container:: example

            Gets prime form of pitch-class set with degree of symmetry equal to
            2:

            >>> pc_set = abjad.PitchClassSet([1, 2, 7, 8])
            >>> pc_set.get_prime_form()
            PitchClassSet(items=[0, 1, 6, 7], item_class=abjad.NumberedPitchClass)

            >>> pc_set = abjad.PitchClassSet([1, 2, 7, 8])
            >>> pc_set.get_prime_form(transposition_only=True)
            PitchClassSet(items=[0, 1, 6, 7], item_class=abjad.NumberedPitchClass)

        ..  container:: example

            Gets prime form of pitch-class set with degree of symmetry equal to
            4:

            >>> pc_set = abjad.PitchClassSet([0, 3, 6, 9])
            >>> pc_set.get_prime_form()
            PitchClassSet(items=[0, 3, 6, 9], item_class=abjad.NumberedPitchClass)

            >>> pc_set = abjad.PitchClassSet([0, 3, 6, 9])
            >>> pc_set.get_prime_form(transposition_only=True)
            PitchClassSet(items=[0, 3, 6, 9], item_class=abjad.NumberedPitchClass)

        ..  container:: example

            Gets prime form of pitch-class that is not inversion-equivalent:

            >>> pc_set = abjad.PitchClassSet([0, 4, 6, 7])
            >>> pc_set.get_prime_form()
            PitchClassSet(items=[0, 1, 3, 7], item_class=abjad.NumberedPitchClass)

            >>> pc_set = abjad.PitchClassSet([0, 4, 6, 7])
            >>> pc_set.get_prime_form(transposition_only=True)
            PitchClassSet(items=[0, 4, 6, 7], item_class=abjad.NumberedPitchClass)

        ..  container:: example

            Gets prime form of inversionally nonequivalent pitch-class set:

            >>> pc_set = abjad.PitchClassSet([0, 4, 7])
            >>> pc_set.get_prime_form()
            PitchClassSet(items=[0, 3, 7], item_class=abjad.NumberedPitchClass)

            >>> pc_set = abjad.PitchClassSet([0, 4, 7])
            >>> pc_set.get_prime_form(transposition_only=True)
            PitchClassSet(items=[0, 4, 7], item_class=abjad.NumberedPitchClass)

        ..  container:: example

            REGRESSION:

            >>> pc_set = abjad.PitchClassSet([0, 1, 2, 5, 8, 9])
            >>> pc_set.get_prime_form()
            PitchClassSet(items=[0, 1, 2, 5, 6, 9], item_class=abjad.NumberedPitchClass)

            REGRESSION:

            >>> pc_set = abjad.PitchClassSet([0, 1, 2, 3, 6, 7])
            >>> pc_set.get_prime_form()
            PitchClassSet(items=[0, 1, 2, 3, 6, 7], item_class=abjad.NumberedPitchClass)

        Returns new pitch-class set.
        """
        if not len(self):
            return copy.copy(self)
        normal_order = self.get_normal_order()
        if not transposition_only:
            normal_orders = [normal_order]
            inversion = self.invert()
            normal_order = inversion.get_normal_order()
            normal_orders.append(normal_order)
            normal_orders = [_._transpose_to_zero() for _ in normal_orders]
            assert len(normal_orders) == 2
            for left_pc, right_pc in zip(*normal_orders):
                if left_pc == right_pc:
                    continue
                if left_pc < right_pc:
                    normal_order = normal_orders[0]
                    break
                if right_pc < left_pc:
                    normal_order = normal_orders[-1]
                    break
        pcs = [_.number for _ in normal_order]
        first_pc = pcs[0]
        pcs = [pc - first_pc for pc in pcs]
        prime_form = type(self)(items=pcs, item_class=NumberedPitchClass)
        return prime_form

    def invert(self, axis=None) -> "PitchClassSet":
        """
        Inverts pitch-class set.

        ..  container:: example

            >>> abjad.PitchClassSet(
            ...     [-2, -1.5, 6, 7, -1.5, 7],
            ...     ).invert()
            PitchClassSet(items=[1.5, 2, 5, 6], item_class=abjad.NumberedPitchClass)

        """
        return type(self)([pc.invert(axis=axis) for pc in self.items])

    def is_transposed_subset(self, pcset) -> bool:
        """
        Is true when pitch-class set is transposed subset of ``pcset``.

        ..  container:: example

            >>> pitch_class_set_1 = abjad.PitchClassSet(
            ...     [-2, -1.5, 6, 7, -1.5, 7],
            ...     )
            >>> pitch_class_set_2 = abjad.PitchClassSet(
            ...     [-2, -1.5, 6, 7, -1.5, 7, 7.5, 8],
            ...     )

            >>> pitch_class_set_1.is_transposed_subset(pitch_class_set_2)
            True

        """
        for n in range(12):
            if self.transpose(n).issubset(pcset):
                return True
        return False

    def is_transposed_superset(self, pcset) -> bool:
        """
        Is true when pitch-class set is transposed superset of ``pcset``.

        ..  container:: example

            >>> pitch_class_set_1 = abjad.PitchClassSet(
            ...     [-2, -1.5, 6, 7, -1.5, 7],
            ...     )
            >>> pitch_class_set_2 = abjad.PitchClassSet(
            ...     [-2, -1.5, 6, 7, -1.5, 7, 7.5, 8],
            ...     )

            >>> pitch_class_set_2.is_transposed_superset(pitch_class_set_1)
            True

        """
        for n in range(12):
            if self.transpose(n).issuperset(pcset):
                return True
        return False

    def multiply(self, n) -> "PitchClassSet":
        """
        Multiplies pitch-class set by ``n``.

        ..  container:: example

            >>> abjad.PitchClassSet(
            ...     [-2, -1.5, 6, 7, -1.5, 7],
            ...     ).multiply(5)
            PitchClassSet(items=[2, 4.5, 6, 11], item_class=abjad.NumberedPitchClass)

        """
        items = (pitch_class.multiply(n) for pitch_class in self)
        return dataclasses.replace(self, items=items)

    def order_by(self, segment) -> "PitchClassSegment":
        """
        Orders pitch-class set by pitch-class ``segment``.

        ..  container:: example

            >>> set_ = abjad.PitchClassSet(['c', 'e', 'b'])
            >>> segment = abjad.PitchClassSegment(['e', 'a', 'f'])
            >>> set_.order_by(segment)
            PitchClassSegment(items="b e c", item_class=NamedPitchClass)

        """
        if not len(self) == len(segment):
            raise ValueError("set and segment must be on equal length.")
        for pitch_classes in _enumerate.yield_permutations(self):
            candidate = PitchClassSegment(pitch_classes)
            if candidate._is_equivalent_under_transposition(segment):
                return candidate
        raise ValueError(f"{self!s} can not order by {segment!s}.")

    def transpose(self, n=0) -> "PitchClassSet":
        """
        Transposes all pitch-classes in pitch-class set by index ``n``.

        ..  container:: example

            >>> set_ = abjad.PitchClassSet(
            ...     items=[-2, -1.5, 6, 7, -1.5, 7],
            ...     item_class=abjad.NumberedPitchClass,
            ...     )

            >>> for n in range(12):
            ...     print(n, set_.transpose(n))
            ...
            0 PC{6, 7, 10, 10.5}
            1 PC{7, 8, 11, 11.5}
            2 PC{0, 0.5, 8, 9}
            3 PC{1, 1.5, 9, 10}
            4 PC{2, 2.5, 10, 11}
            5 PC{0, 3, 3.5, 11}
            6 PC{0, 1, 4, 4.5}
            7 PC{1, 2, 5, 5.5}
            8 PC{2, 3, 6, 6.5}
            9 PC{3, 4, 7, 7.5}
            10 PC{4, 5, 8, 8.5}
            11 PC{5, 6, 9, 9.5}

        """
        items = (pitch_class + n for pitch_class in self)
        return dataclasses.replace(self, items=items)


@dataclasses.dataclass(slots=True, unsafe_hash=True)
class PitchSet(Set):
    r"""
    Pitch set.

    ..  container:: example

        Numbered pitch set:

        >>> set_ = abjad.PitchSet(
        ...     items=[-2, -1.5, 6, 7, -1.5, 7],
        ...     item_class=abjad.NumberedPitch,
        ...     )
        >>> set_
        PitchSet(items=[-2, -1.5, 6, 7], item_class=abjad.NumberedPitch)

    ..  container:: example

        Named pitch set:

        >>> set_ = abjad.PitchSet(
        ...     ['bf,', 'aqs', "fs'", "g'", 'bqf', "g'"],
        ...     item_class=abjad.NamedPitch,
        ...     )
        >>> set_
        PitchSet(items=['bf,', 'aqs', 'bqf', "fs'", "g'"], item_class=abjad.NamedPitch)

    ..  container:: example

        >>> set_1 = abjad.PitchSet(
        ...     items=[-2, -1.5, 6, 7, -1.5, 7],
        ...     item_class=abjad.NumberedPitch,
        ...     )
        >>> set_2 = abjad.PitchSet(
        ...     items=[-2, -1.5, 6, 7, -1.5, 7],
        ...     item_class=abjad.NumberedPitch,
        ...     )
        >>> set_3 = abjad.PitchSet(
        ...     items=[11, 12, 12.5],
        ...     item_class=abjad.NumberedPitch,
        ...     )

        >>> set_1 == set_1
        True
        >>> set_1 == set_2
        True
        >>> set_1 == set_3
        False

        >>> set_2 == set_1
        True
        >>> set_2 == set_2
        True
        >>> set_2 == set_3
        False

        >>> set_3 == set_1
        False
        >>> set_3 == set_2
        False
        >>> set_3 == set_3
        True

    """

    def __repr__(self):
        """
        Gets repr of pitch-class set.
        """
        return f"{type(self).__name__}(items={self._get_sorted_repr_items()}, item_class=abjad.{self.item_class.__name__})"

    @property
    def _named_item_class(self):
        return NamedPitch

    @property
    def _numbered_item_class(self):
        return NumberedPitch

    @property
    def _parent_item_class(self):
        return Pitch

    def _is_equivalent_under_transposition(self, argument):
        """
        True if pitch set is equivalent to ``argument`` under transposition.

        Returns true or false.
        """
        if not isinstance(argument, type(self)):
            return False
        if not len(self) == len(argument):
            return False
        difference = -(NamedPitch(argument[0], 4) - NamedPitch(self[0], 4))
        new_pitches = (x + difference for x in self)
        new_pitches = dataclasses.replace(self, items=new_pitches)
        return argument == new_pitches

    def _sort_self(self):
        return sorted(PitchSegment(tuple(self)))

    @property
    def duplicate_pitch_classes(self) -> "PitchClassSet":
        """
        Gets duplicate pitch-classes in pitch set.

        ..  container:: example

            >>> set_ = abjad.PitchSet(
            ...     items=[-2, -1.5, 6, 7, -1.5, 7],
            ...     item_class=abjad.NumberedPitch,
            ...     )
            >>> set_.duplicate_pitch_classes
            PitchClassSet(items=[], item_class=abjad.NumberedPitchClass)

            >>> set_ = abjad.PitchSet(
            ...     items=[-2, -1.5, 6, 7, 10.5, 7],
            ...     item_class=abjad.NumberedPitch,
            ...     )
            >>> set_.duplicate_pitch_classes
            PitchClassSet(items=[10.5], item_class=abjad.NumberedPitchClass)

        """
        pitch_classes = []
        duplicate_pitch_classes = []
        for pitch in self:
            pitch_class = NumberedPitchClass(pitch)
            if pitch_class in pitch_classes:
                duplicate_pitch_classes.append(pitch_class)
            pitch_classes.append(pitch_class)
        return PitchClassSet(duplicate_pitch_classes, item_class=NumberedPitchClass)

    @property
    def hertz(self) -> set[float]:
        """
        Gets hertz of pitches in pitch segment.

        ..  container:: example

            >>> pitch_set = abjad.PitchSet('c e g b')
            >>> sorted(pitch_set.hertz)
            [130.81..., 164.81..., 195.99..., 246.94...]

        """
        return set(_.hertz for _ in self)

    @property
    def is_pitch_class_unique(self) -> bool:
        """
        Is true when pitch set is pitch-class-unique.

        ..  container:: example

            >>> set_ = abjad.PitchSet(
            ...     items=[-2, -1.5, 6, 7, -1.5, 7],
            ...     item_class=abjad.NumberedPitch,
            ...     )

            >>> set_.is_pitch_class_unique
            True

        ..  container:: example

            >>> set_ = abjad.PitchSet(
            ...     items=[-2, -1.5, 6, 7, 10.5, 7],
            ...     item_class=abjad.NumberedPitch,
            ...     )

            >>> set_.is_pitch_class_unique
            False

        """
        numbered_pitch_class_set = PitchClassSet(self, item_class=NumberedPitchClass)
        return len(self) == len(numbered_pitch_class_set)

    @classmethod
    def from_selection(class_, selection, item_class=None) -> "PitchSet":
        """
        Makes pitch set from ``selection``.

        ..  container:: example

            >>> staff_1 = abjad.Staff("c'4 <d' fs' a'>4 b2")
            >>> staff_2 = abjad.Staff("c4. r8 g2")
            >>> selection = abjad.select((staff_1, staff_2))
            >>> abjad.PitchSet.from_selection(selection)
            PitchSet(items=['c', 'g', 'b', "c'", "d'", "fs'", "a'"], item_class=abjad.NamedPitch)

        """
        pitch_segment = PitchSegment.from_selection(selection)
        return class_(items=pitch_segment, item_class=item_class)

    def invert(self, axis) -> "PitchSet":
        """
        Inverts pitch set about ``axis``.
        """
        items = (pitch.invert(axis) for pitch in self)
        return dataclasses.replace(self, items=items)

    def issubset(self, argument) -> bool:
        """
        Is true when pitch set is subset of ``argument``.

        ..  container:: example

            >>> set_1 = abjad.PitchSet(
            ...     items=[-2, -1.5, 6, 7, -1.5, 7],
            ...     item_class=abjad.NumberedPitch,
            ...     )
            >>> set_2 = abjad.PitchSet(
            ...     items=[-1.5, 6],
            ...     item_class=abjad.NumberedPitch,
            ...     )

            >>> set_1.issubset(set_2)
            False

            >>> set_2.issubset(set_1)
            True

        """
        return Set.issubset(self, argument)

    def issuperset(self, argument) -> bool:
        """
        Is true when pitch set is superset of ``argument``.

        ..  container:: example

            >>> set_1 = abjad.PitchSet(
            ...     items=[-2, -1.5, 6, 7, -1.5, 7],
            ...     item_class=abjad.NumberedPitch,
            ...     )
            >>> set_2 = abjad.PitchSet(
            ...     items=[-1.5, 6],
            ...     item_class=abjad.NumberedPitch,
            ...     )

            >>> set_1.issuperset(set_2)
            False

            >>> set_2.issuperset(set_1)
            True

        """
        return Set.issubset(self, argument)

    def register(self, pitch_classes):
        """
        Registers ``pitch_classes`` by pitch set.

        ..  container:: example

            >>> pitch_set = abjad.PitchSet(
            ...     items=[10, 19, 20, 23, 24, 26, 27, 29, 30, 33, 37, 40],
            ...     item_class=abjad.NumberedPitch,
            ...     )
            >>> pitch_classes = [10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11]
            >>> pitches = pitch_set.register(pitch_classes)
            >>> for pitch in pitches:
            ...     pitch
            NumberedPitch(10)
            NumberedPitch(24)
            NumberedPitch(26)
            NumberedPitch(30)
            NumberedPitch(20)
            NumberedPitch(19)
            NumberedPitch(29)
            NumberedPitch(27)
            NumberedPitch(37)
            NumberedPitch(33)
            NumberedPitch(40)
            NumberedPitch(23)

        Returns list of zero or more numbered pitches.
        """
        if isinstance(pitch_classes, collections.abc.Iterable):
            result = [
                [_ for _ in self if _.number % 12 == pc]
                for pc in [x % 12 for x in pitch_classes]
            ]
            result = _sequence.Sequence(result).flatten(depth=-1)
        elif isinstance(pitch_classes, int):
            result = [p for p in pitch_classes if p % 12 == pitch_classes][0]
        else:
            raise TypeError("must be pitch-class or list of pitch-classes.")
        return result

    def transpose(self, n=0) -> "PitchSet":
        """
        Transposes pitch set by index ``n``.
        """
        items = (pitch.transpose(n=n) for pitch in self)
        return dataclasses.replace(self, items=items)


@dataclasses.dataclass(slots=True)
class Vector(_typedcollections.TypedCounter):
    """
    Vector.
    """

    def __post_init__(self):
        if isinstance(self.items, str):
            self.items = self.items.split()
        if self.item_class is None:
            self.item_class = self._named_item_class
            if self.items is not None:
                if isinstance(
                    self.items, _typedcollections.TypedCollection
                ) and issubclass(self.items.item_class, self._parent_item_class):
                    self.item_class = self.items.item_class
                elif len(self.items):
                    if isinstance(self.items, collections.abc.Set):
                        self.items = tuple(self.items)
                    if isinstance(self.items, dict):
                        self.item_class = self._dictionary_to_item_class(self.items)
                    elif isinstance(self.items[0], str):
                        self.item_class = self._named_item_class
                    elif isinstance(self.items[0], (int, float)):
                        self.item_class = self._numbered_item_class
                    elif isinstance(self.items[0], self._parent_item_class):
                        self.item_class = type(self.items[0])
        assert issubclass(self.item_class, self._parent_item_class)
        _typedcollections.TypedCounter.__post_init__(self)
        assert isinstance(self.items, dict), repr(self.items)

    def __str__(self) -> str:
        """
        String representation of vector.
        """
        parts = [f"{key}: {value}" for key, value in self.items()]
        string = ", ".join(parts)
        return f"<{string}>"

    def _dictionary_to_item_class(self, dictionary):
        if not len(dictionary):
            return self._named_item_class
        keys = dictionary.keys()
        first_key = keys[0]
        assert isinstance(first_key, str), repr(first_key)
        try:
            float(first_key)
            item_class = self._numbered_item_class
        except ValueError:
            item_class = self._named_item_class
        return item_class


@dataclasses.dataclass(slots=True)
class IntervalVector(Vector):
    """
    Interval vector.

    ..  container:: example

        Initializes from pitch segment:

        >>> pitch_segment = abjad.PitchSegment(
        ...     items=[0, 11, 7, 4, 2, 9, 3, 8, 10, 1, 5, 6],
        ...     )
        >>> numbered_interval_vector = abjad.IntervalVector(
        ...     items=pitch_segment,
        ...     item_class=abjad.NumberedInterval,
        ...     )
        >>> for interval, count in sorted(numbered_interval_vector.items.items(),
        ...     key=lambda x: (x[0].direction_number, x[0].number)):
        ...     print(interval, count)
        ...
        -11 1
        -10 1
        -9 1
        -8 2
        -7 3
        -6 3
        -5 4
        -4 4
        -3 4
        -2 5
        -1 6
        +1 5
        +2 5
        +3 5
        +4 4
        +5 3
        +6 3
        +7 2
        +8 2
        +9 2
        +10 1

    ..  container:: example

        Gets interpreter representation of interval vector:

        >>> pitch_segment = abjad.PitchSegment(
        ...     items=[0, 11, 7, 4, 2, 9, 3, 8, 10, 1, 5, 6],
        ...     )
        >>> vector = abjad.IntervalVector(
        ...     items=pitch_segment,
        ...     item_class=abjad.NumberedInterval,
        ...     )

        >>> vector
        IntervalVector(items={NumberedInterval(-11): 1, NumberedInterval(-10): 1, NumberedInterval(-9): 1, NumberedInterval(-8): 2, NumberedInterval(-7): 3, NumberedInterval(-6): 3, NumberedInterval(-5): 4, NumberedInterval(-4): 4, NumberedInterval(-3): 4, NumberedInterval(-2): 5, NumberedInterval(-1): 6, NumberedInterval(1): 5, NumberedInterval(2): 5, NumberedInterval(3): 5, NumberedInterval(4): 4, NumberedInterval(5): 3, NumberedInterval(6): 3, NumberedInterval(7): 2, NumberedInterval(8): 2, NumberedInterval(9): 2, NumberedInterval(10): 1}, item_class=<class 'abjad.pitch.NumberedInterval'>)

    """

    def __post_init__(self):
        if isinstance(
            self.items,
            (
                PitchSegment,
                PitchSet,
                PitchClassSegment,
                PitchClassSet,
            ),
        ):
            intervals = []
            pairs = _enumerate.yield_pairs(self.items)
            for first, second in pairs:
                intervals.append(second - first)
            self.items = intervals
        Vector.__post_init__(self)

    @property
    def _named_item_class(self):
        return NamedInterval

    @property
    def _numbered_item_class(self):
        return NumberedInterval

    @property
    def _parent_item_class(self):
        return Interval

    @classmethod
    def from_selection(class_, selection, item_class=None) -> "IntervalVector":
        """
        Makes interval vector from ``selection``.
        """
        pitch_segment = PitchSegment.from_selection(selection)
        return class_(pitch_segment, item_class=item_class)


@dataclasses.dataclass(slots=True)
class IntervalClassVector(Vector):
    """
    Interval-class vector.

    ..  container:: example

        An interval-class vector:

        >>> pitch_segment = abjad.PitchSegment(
        ...     items=[0, 11, 7, 4, 2, 9, 3, 8, 10, 1, 5, 6],
        ... )
        >>> numbered_interval_class_vector = abjad.IntervalClassVector(
        ...     items=pitch_segment,
        ...     item_class=abjad.NumberedInversionEquivalentIntervalClass,
        ... )

        >>> items = sorted(numbered_interval_class_vector.items.items())
        >>> for interval, count in items:
        ...     print(interval, count)
        ...
        1 12
        2 12
        3 12
        4 12
        5 12
        6 6

    ..  container:: example

        Gets interpreter representation of interval-class vector:

        >>> pitch_segment = abjad.PitchSegment(
        ...     items=[0, 11, 7, 4, 2, 9, 3, 8, 10, 1, 5, 6],
        ...     )
        >>> vector = abjad.IntervalClassVector(
        ...     items=pitch_segment,
        ...     item_class=abjad.NumberedInversionEquivalentIntervalClass,
        ...     )

        >>> vector
        IntervalClassVector(items={NumberedInversionEquivalentIntervalClass(1): 12, NumberedInversionEquivalentIntervalClass(2): 12, NumberedInversionEquivalentIntervalClass(3): 12, NumberedInversionEquivalentIntervalClass(4): 12, NumberedInversionEquivalentIntervalClass(5): 12, NumberedInversionEquivalentIntervalClass(6): 6}, item_class=<class 'abjad.pitch.NumberedInversionEquivalentIntervalClass'>)

    """

    def __init__(self, items=None, item_class=None):
        prototype = (
            PitchSegment,
            PitchSet,
            PitchClassSegment,
            PitchClassSet,
        )
        if isinstance(items, prototype):
            intervals = []
            items = tuple(items)
            pairs = _enumerate.yield_pairs(items)
            for first, second in pairs:
                intervals.append(second - first)
            items = intervals
        Vector.__init__(self, items=items, item_class=item_class)

    @property
    def _label(self):
        counts = []
        for i in range(7):
            item = self._coerce_item(i)
            count = self.items.get(item, 0)
            counts.append(count)
        counts = "".join([str(x) for x in counts])
        if len(self) == 13:
            quartertones = []
            for i in range(6):
                item = self._coerce_item(i + 0.5)
                count = self.items.get(item, 0)
                quartertones.append(count)
            quartertones = "".join([str(_) for _ in quartertones])
            return rf'\tiny \column {{ "{counts}" "{quartertones}" }}'
        else:
            return rf"\tiny {counts}"

    @property
    def _named_item_class(self):
        return NamedIntervalClass

    @property
    def _numbered_item_class(self):
        return NumberedIntervalClass

    @property
    def _parent_item_class(self):
        return IntervalClass

    @classmethod
    def from_selection(class_, selection, item_class=None) -> "IntervalClassVector":
        """
        Makes interval-class vector from ``selection``.

        ..  container:: example

            Makes numbered inversion-equivalent interval-class vector from selection:

            >>> chord = abjad.Chord("<c' d' b''>4"),
            >>> vector = abjad.IntervalClassVector.from_selection(
            ...     abjad.select(chord),
            ...     item_class=abjad.NumberedInversionEquivalentIntervalClass,
            ...     )
            >>> vector
            IntervalClassVector(items={NumberedInversionEquivalentIntervalClass(1): 1, NumberedInversionEquivalentIntervalClass(2): 1, NumberedInversionEquivalentIntervalClass(3): 1}, item_class=<class 'abjad.pitch.NumberedInversionEquivalentIntervalClass'>)

            Makes numbered interval-class vector from selection:

            >>> chord = abjad.Chord("<c' d' b''>4")
            >>> vector = abjad.IntervalClassVector.from_selection(
            ...     abjad.select(chord),
            ...     item_class=abjad.NumberedIntervalClass,
            ...     )
            >>> vector
            IntervalClassVector(items={NumberedIntervalClass(-11): 1, NumberedIntervalClass(-9): 1, NumberedIntervalClass(-2): 1}, item_class=<class 'abjad.pitch.NumberedIntervalClass'>)

            TODO. This should probabaly be checked. Resulting values should probabaly be
            positive (or signless) instead of negative.

            Makes named interval-class vector from selection:

            >>> chord = abjad.Chord("<c' d' b''>4")
            >>> vector = abjad.IntervalClassVector.from_selection(
            ...     abjad.select(chord),
            ...     item_class=None,
            ...     )
            >>> vector
            IntervalClassVector(items={NamedIntervalClass('-M7'): 1, NamedIntervalClass('-M6'): 1, NamedIntervalClass('-M2'): 1}, item_class=<class 'abjad.pitch.NamedIntervalClass'>)

            TODO. This should probabaly be checked. Resulting values should probabaly be
            positive (or signless) instead of negative.

        """
        pitch_segment = PitchSegment.from_selection(selection)
        return class_(pitch_segment, item_class=item_class)


@dataclasses.dataclass(slots=True)
class PitchClassVector(Vector):
    """
    Pitch-class vector.

    ..  container:: example

        Pitch-class vector:

        >>> vector = abjad.PitchClassVector(
        ...     items=[7, 6, -2, -3, -3, 0, 1, 14, 15, 16, 16],
        ...     item_class=abjad.NumberedPitchClass,
        ... )
        >>> vector
        PitchClassVector(items={NumberedPitchClass(0): 1, NumberedPitchClass(1): 1, NumberedPitchClass(2): 1, NumberedPitchClass(3): 1, NumberedPitchClass(4): 2, NumberedPitchClass(6): 1, NumberedPitchClass(7): 1, NumberedPitchClass(9): 2, NumberedPitchClass(10): 1}, item_class=<class 'abjad.pitch.NumberedPitchClass'>)

        >>> items = sorted(vector.items.items())
        >>> for pitch_class, count in items:
        ...     print(pitch_class, count)
        0 1
        1 1
        2 1
        3 1
        4 2
        6 1
        7 1
        9 2
        10 1

    """

    @property
    def _named_item_class(self):
        return NamedPitchClass

    @property
    def _numbered_item_class(self):
        return NumberedPitchClass

    @property
    def _parent_item_class(self):
        return PitchClass

    @classmethod
    def from_selection(class_, selection, item_class=None) -> "PitchClassVector":
        """
        Makes pitch-class vector from ``selection``.
        """
        pitch_segment = PitchSegment.from_selection(selection)
        return class_(pitch_segment, item_class=item_class)


class PitchVector(Vector):
    """
    Pitch vector.

    ..  container:: example

        >>> vector = abjad.PitchVector(
        ...     items=[7, 6, -2, -3, -3, 0, 1, 14, 15, 16, 16],
        ...     item_class=abjad.NumberedPitch,
        ... )
        >>> vector
        PitchVector(items={NumberedPitch(-3): 2, NumberedPitch(-2): 1, NumberedPitch(0): 1, NumberedPitch(1): 1, NumberedPitch(6): 1, NumberedPitch(7): 1, NumberedPitch(14): 1, NumberedPitch(15): 1, NumberedPitch(16): 2}, item_class=<class 'abjad.pitch.NumberedPitch'>)

        >>> items = list(vector.items.items())
        >>> items.sort(key=lambda x: x[0].number)
        >>> for pitch_class, count in items:
        ...     print(pitch_class, count)
        -3 2
        -2 1
        0 1
        1 1
        6 1
        7 1
        14 1
        15 1
        16 2

    """

    @property
    def _named_item_class(self):
        return NamedPitch

    @property
    def _numbered_item_class(self):
        return NumberedPitch

    @property
    def _parent_item_class(self):
        return Pitch

    @classmethod
    def from_selection(class_, selection, item_class=None) -> "PitchVector":
        """
        Makes pitch vector from ``selection``.
        """
        pitch_segment = PitchSegment.from_selection(selection)
        return class_(pitch_segment, item_class=item_class)
