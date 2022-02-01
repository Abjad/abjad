import abc
import collections
import copy
import functools
import importlib
import math
import numbers
import re
import types
import typing

import quicktions

from . import cyclictuple as _cyclictuple
from . import duration as _duration
from . import enumerate as _enumerate
from . import enums as _enums
from . import format as _format
from . import math as _math
from . import new as _new
from . import pattern as _pattern
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

# TODO: possibly remove?
_symbolic_accidental_to_abbreviation = {
    "bb": "ff",
    "b~": "tqf",
    "b": "f",
    "~": "qf",
    "": "",
    "!": "!",
    "+": "qs",
    "#": "s",
    "#+": "tqs",
    "##": "ss",
}

# TODO: change to function; accommodate arbitrarily long names
_symbolic_accidental_to_semitones = {
    "bb": -2,
    "b~": -1.5,
    "b": -1,
    "~": -0.5,
    "": 0,
    "+": 0.5,
    "#": 1,
    "#+": 1.5,
    "##": 2,
    "ff": -2,
    "tqf": 1.5,
    "f": -1,
    "qf": -0.5,
    "qs": 0.5,
    "s": 1,
    "tqs": 1.5,
    "ss": 2,
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

_start_punctuation_to_inclusivity_string = {"[": "inclusive", "(": "exclusive"}

_stop_punctuation_to_inclusivity_string = {"]": "inclusive", ")": "exclusive"}

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
class Accidental:
    """
    Accidental.

    ..  container:: example

        >>> abjad.Accidental('ff')
        Accidental('double flat')

        >>> abjad.Accidental('tqf')
        Accidental('three-quarters flat')

        >>> abjad.Accidental('f')
        Accidental('flat')

        >>> abjad.Accidental('')
        Accidental('natural')

        >>> abjad.Accidental('qs')
        Accidental('quarter sharp')

        >>> abjad.Accidental('s')
        Accidental('sharp')

        >>> abjad.Accidental('tqs')
        Accidental('three-quarters sharp')

        >>> abjad.Accidental('ss')
        Accidental('double sharp')

    ..  container:: example

        Generalized accidentals are allowed:

        >>> abjad.Accidental('ssss')
        Accidental('ssss')

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_arrow", "_semitones")

    ### INITIALIZER ##

    def __init__(self, name="", *, arrow=None):
        semitones = 0
        _arrow = None
        if name is None:
            pass
        elif isinstance(name, str):
            if name in _accidental_name_to_abbreviation:
                name = _accidental_name_to_abbreviation[name]
                semitones = _accidental_abbreviation_to_semitones[name]
            else:
                match = _comprehensive_accidental_regex.match(name)
                group_dict = match.groupdict()
                if group_dict["alphabetic_accidental"]:
                    prefix, _, suffix = name.partition("q")
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
                    semitones += name.count("#")
                    semitones -= name.count("b")
                    if name.endswith("+"):
                        semitones += 0.5
                    elif name.endswith("~"):
                        semitones -= 0.5
        elif isinstance(name, numbers.Number):
            semitones = float(name)
            assert (semitones % 1.0) in (0.0, 0.5)
        elif hasattr(name, "accidental"):
            _arrow = name.accidental.arrow
            semitones = name.accidental.semitones
        elif isinstance(name, type(self)):
            _arrow = name.arrow
            semitones = name.semitones
        semitones = _math.integer_equivalent_number_to_integer(semitones)
        self._semitones = semitones
        self._arrow = _arrow
        if arrow is not None:
            arrow = _enums.VerticalAlignment.from_expr(arrow)
            if arrow is _enums.Center:
                arrow = None
            self._arrow = arrow

    ### SPECIAL METHODS ###

    def __add__(self, argument):
        """
        Adds ``argument`` to accidental.

        ..  container:: example

            >>> accidental = abjad.Accidental('qs')

            >>> accidental + accidental
            Accidental('sharp')

            >>> accidental + accidental + accidental
            Accidental('three-quarters sharp')

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

    def __eq__(self, argument) -> bool:
        """
        Delegates to ``abjad.format.compare_objects()``.
        """
        return _format.compare_objects(self, argument)

    def __hash__(self) -> int:
        """
        Hashes accidental.
        """
        return hash(self.__class__.__name__ + str(self))

    def __lt__(self, argument):
        """
        Is true when ``argument`` is an accidental with semitones greater
        than those of this accidental.

        ..  container:: example

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

        Returns true or false.
        """
        return self.semitones < argument.semitones

    def __neg__(self):
        """
        Negates accidental.

        ..  container:: example

            >>> -abjad.Accidental('ff')
            Accidental('double sharp')

            >>> -abjad.Accidental('tqf')
            Accidental('three-quarters sharp')

            >>> -abjad.Accidental('f')
            Accidental('sharp')

            >>> -abjad.Accidental('')
            Accidental('natural')

            >>> -abjad.Accidental('qs')
            Accidental('quarter flat')

            >>> -abjad.Accidental('s')
            Accidental('flat')

            >>> -abjad.Accidental('tqs')
            Accidental('three-quarters flat')

            >>> -abjad.Accidental('ss')
            Accidental('double flat')

        Returns new accidental.
        """
        return type(self)(-self.semitones)

    def __radd__(self, argument):
        """
        Raises not implemented error on accidental.
        """
        raise NotImplementedError

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return _format.get_repr(self)

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
            Accidental('natural')

            >>> accidental - accidental - accidental
            Accidental('quarter flat')

        Returns new accidental.
        """
        if not isinstance(argument, type(self)):
            raise TypeError("can only subtract accidental from other accidental.")
        semitones = self.semitones - argument.semitones
        return type(self)(semitones)

    ### PRIVATE METHODS ###

    @classmethod
    def _get_all_accidental_abbreviations(class_):
        return list(_accidental_abbreviation_to_symbol.keys())

    @classmethod
    def _get_all_accidental_names(class_):
        return list(_accidental_name_to_abbreviation.keys())

    @classmethod
    def _get_all_accidental_semitone_values(class_):
        return list(_accidental_semitones_to_abbreviation.keys())

    def _get_format_specification(self):
        return _format.FormatSpecification(
            storage_format_args_values=[self.name],
            storage_format_is_not_indented=True,
            storage_format_keyword_names=["arrow"],
        )

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

    ### PUBLIC PROPERTIES ###

    @property
    def arrow(self):
        """
        Gets arrow of accidental.

        ..  container:: example

            Most accidentals carry no arrow:

            >>> abjad.Accidental('sharp').arrow is None
            True

        ..  container:: example

            Sharp with up-arrow:

            >>> abjad.Accidental('sharp', arrow=abjad.Up).arrow
            Up

            Sharp with down-arrow:

            >>> abjad.Accidental('sharp', arrow=abjad.Down).arrow
            Down

        Arrow property is currently a stub in the object model. You can set the
        property but accidental math and formatting currently ignore the
        setting.

        Returns up, down or none.
        """
        return self._arrow

    @property
    def name(self):
        """
        Gets name of accidental.

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

        Returns string.
        """
        try:
            abbreviation = _accidental_semitones_to_abbreviation[self.semitones]
            name = _accidental_abbreviation_to_name[abbreviation]
        except KeyError:
            name = str(self)
        return name

    @property
    def semitones(self):
        """
        Gets semitones of accidental.

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

        Returns number.
        """
        return self._semitones

    @property
    def symbol(self):
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

        Returns string.
        """
        abbreviation = _accidental_semitones_to_abbreviation[self.semitones]
        symbol = _accidental_abbreviation_to_symbol[abbreviation]
        return symbol


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
            match = _comprehensive_octave_regex.match(number)
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
        Delegates to ``abjad.format.compare_objects()``.

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
        return _format.compare_objects(self, argument)

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
        return hash(self.__class__.__name__ + str(self))

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
        return _format.get_repr(self)

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
        return _format.FormatSpecification(
            storage_format_is_not_indented=True,
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


class SetClass:
    """
    Set-class.

    ..  container:: example

        Makes SG2 set-class from Forte rank:

        >>> set_class = abjad.SetClass(4, 29)
        >>> print(set_class)
        SC(4-29){0, 1, 3, 7}

        Makes SG2 set-class from lex rank:

        >>> set_class = abjad.SetClass(4, 29, lex_rank=True)
        >>> print(set_class)
        SC(4-29){0, 3, 6, 9}

        Makes SG1 set-class:

        >>> set_class = abjad.SetClass(4, 29, transposition_only=True)
        >>> print(set_class)
        SC(4-29){0, 2, 6, 7}

    ..  container:: example

        Makes aggregate:

        >>> set_class = abjad.SetClass(12, 1, transposition_only=True)
        >>> print(set_class)
        SC(12-1){0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}

    ..  container:: example

        Lists SG2 tetrachords, pentachords, hexachords by Forte rank:

        >>> set_classes = abjad.SetClass.list_set_classes(cardinality=4)
        >>> for set_class in set_classes:
        ...     print(set_class)
        ...
        SC(4-1){0, 1, 2, 3}
        SC(4-2){0, 1, 2, 4}
        SC(4-3){0, 1, 3, 4}
        SC(4-4){0, 1, 2, 5}
        SC(4-5){0, 1, 2, 6}
        SC(4-6){0, 1, 2, 7}
        SC(4-7){0, 1, 4, 5}
        SC(4-8){0, 1, 5, 6}
        SC(4-9){0, 1, 6, 7}
        SC(4-10){0, 2, 3, 5}
        SC(4-11){0, 1, 3, 5}
        SC(4-12){0, 2, 3, 6}
        SC(4-13){0, 1, 3, 6}
        SC(4-14){0, 2, 3, 7}
        SC(4-15){0, 1, 4, 6}
        SC(4-16){0, 1, 5, 7}
        SC(4-17){0, 3, 4, 7}
        SC(4-18){0, 1, 4, 7}
        SC(4-19){0, 1, 4, 8}
        SC(4-20){0, 1, 5, 8}
        SC(4-21){0, 2, 4, 6}
        SC(4-22){0, 2, 4, 7}
        SC(4-23){0, 2, 5, 7}
        SC(4-24){0, 2, 4, 8}
        SC(4-25){0, 2, 6, 8}
        SC(4-26){0, 3, 5, 8}
        SC(4-27){0, 2, 5, 8}
        SC(4-28){0, 3, 6, 9}
        SC(4-29){0, 1, 3, 7}

        >>> set_classes = abjad.SetClass.list_set_classes(cardinality=5)
        >>> for set_class in set_classes:
        ...     print(set_class)
        ...
        SC(5-1){0, 1, 2, 3, 4}
        SC(5-2){0, 1, 2, 3, 5}
        SC(5-3){0, 1, 2, 4, 5}
        SC(5-4){0, 1, 2, 3, 6}
        SC(5-5){0, 1, 2, 3, 7}
        SC(5-6){0, 1, 2, 5, 6}
        SC(5-7){0, 1, 2, 6, 7}
        SC(5-8){0, 2, 3, 4, 6}
        SC(5-9){0, 1, 2, 4, 6}
        SC(5-10){0, 1, 3, 4, 6}
        SC(5-11){0, 2, 3, 4, 7}
        SC(5-12){0, 1, 3, 5, 6}
        SC(5-13){0, 1, 2, 4, 8}
        SC(5-14){0, 1, 2, 5, 7}
        SC(5-15){0, 1, 2, 6, 8}
        SC(5-16){0, 1, 3, 4, 7}
        SC(5-17){0, 1, 3, 4, 8}
        SC(5-18){0, 1, 4, 5, 7}
        SC(5-19){0, 1, 3, 6, 7}
        SC(5-20){0, 1, 3, 7, 8}
        SC(5-21){0, 1, 4, 5, 8}
        SC(5-22){0, 1, 4, 7, 8}
        SC(5-23){0, 2, 3, 5, 7}
        SC(5-24){0, 1, 3, 5, 7}
        SC(5-25){0, 2, 3, 5, 8}
        SC(5-26){0, 2, 4, 5, 8}
        SC(5-27){0, 1, 3, 5, 8}
        SC(5-28){0, 2, 3, 6, 8}
        SC(5-29){0, 1, 3, 6, 8}
        SC(5-30){0, 1, 4, 6, 8}
        SC(5-31){0, 1, 3, 6, 9}
        SC(5-32){0, 1, 4, 6, 9}
        SC(5-33){0, 2, 4, 6, 8}
        SC(5-34){0, 2, 4, 6, 9}
        SC(5-35){0, 2, 4, 7, 9}
        SC(5-36){0, 1, 2, 4, 7}
        SC(5-37){0, 3, 4, 5, 8}
        SC(5-38){0, 1, 2, 5, 8}

        >>> set_classes = abjad.SetClass.list_set_classes(cardinality=6)
        >>> for set_class in set_classes:
        ...     print(set_class)
        ...
        SC(6-1){0, 1, 2, 3, 4, 5}
        SC(6-2){0, 1, 2, 3, 4, 6}
        SC(6-3){0, 1, 2, 3, 5, 6}
        SC(6-4){0, 1, 2, 4, 5, 6}
        SC(6-5){0, 1, 2, 3, 6, 7}
        SC(6-6){0, 1, 2, 5, 6, 7}
        SC(6-7){0, 1, 2, 6, 7, 8}
        SC(6-8){0, 2, 3, 4, 5, 7}
        SC(6-9){0, 1, 2, 3, 5, 7}
        SC(6-10){0, 1, 3, 4, 5, 7}
        SC(6-11){0, 1, 2, 4, 5, 7}
        SC(6-12){0, 1, 2, 4, 6, 7}
        SC(6-13){0, 1, 3, 4, 6, 7}
        SC(6-14){0, 1, 3, 4, 5, 8}
        SC(6-15){0, 1, 2, 4, 5, 8}
        SC(6-16){0, 1, 4, 5, 6, 8}
        SC(6-17){0, 1, 2, 4, 7, 8}
        SC(6-18){0, 1, 2, 5, 7, 8}
        SC(6-19){0, 1, 3, 4, 7, 8}
        SC(6-20){0, 1, 4, 5, 8, 9}
        SC(6-21){0, 2, 3, 4, 6, 8}
        SC(6-22){0, 1, 2, 4, 6, 8}
        SC(6-23){0, 2, 3, 5, 6, 8}
        SC(6-24){0, 1, 3, 4, 6, 8}
        SC(6-25){0, 1, 3, 5, 6, 8}
        SC(6-26){0, 1, 3, 5, 7, 8}
        SC(6-27){0, 1, 3, 4, 6, 9}
        SC(6-28){0, 1, 3, 5, 6, 9}
        SC(6-29){0, 1, 3, 6, 8, 9}
        SC(6-30){0, 1, 3, 6, 7, 9}
        SC(6-31){0, 1, 3, 5, 8, 9}
        SC(6-32){0, 2, 4, 5, 7, 9}
        SC(6-33){0, 2, 3, 5, 7, 9}
        SC(6-34){0, 1, 3, 5, 7, 9}
        SC(6-35){0, 2, 4, 6, 8, 10}
        SC(6-36){0, 1, 2, 3, 4, 7}
        SC(6-37){0, 1, 2, 3, 4, 8}
        SC(6-38){0, 1, 2, 3, 7, 8}
        SC(6-39){0, 2, 3, 4, 5, 8}
        SC(6-40){0, 1, 2, 3, 5, 8}
        SC(6-41){0, 1, 2, 3, 6, 8}
        SC(6-42){0, 1, 2, 3, 6, 9}
        SC(6-43){0, 1, 2, 5, 6, 8}
        SC(6-44){0, 1, 2, 5, 6, 9}
        SC(6-45){0, 2, 3, 4, 6, 9}
        SC(6-46){0, 1, 2, 4, 6, 9}
        SC(6-47){0, 1, 2, 4, 7, 9}
        SC(6-48){0, 1, 2, 5, 7, 9}
        SC(6-49){0, 1, 3, 4, 7, 9}
        SC(6-50){0, 1, 4, 6, 7, 9}

    There are 352 SG1 set-classes and 224 SG2 set-classes.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_cardinality",
        "_lex_rank",
        "_prime_form",
        "_rank",
        "_transposition_only",
    )

    _forte_identifier_to_prime_form = {
        # 0
        (0, 1): (),
        # 1
        (1, 1): (0,),
        # 2
        (2, 1): (0, 1),
        (2, 2): (0, 2),
        (2, 3): (0, 3),
        (2, 4): (0, 4),
        (2, 5): (0, 5),
        (2, 6): (0, 6),
        # 3
        (3, 1): (0, 1, 2),
        (3, 2): (0, 1, 3),
        (3, 3): (0, 1, 4),
        (3, 4): (0, 1, 5),
        (3, 5): (0, 1, 6),
        (3, 6): (0, 2, 4),
        (3, 7): (0, 2, 5),
        (3, 8): (0, 2, 6),
        (3, 9): (0, 2, 7),
        (3, 10): (0, 3, 6),
        (3, 11): (0, 3, 7),
        (3, 12): (0, 4, 8),
        # 4
        (4, 1): (0, 1, 2, 3),
        (4, 2): (0, 1, 2, 4),
        (4, 3): (0, 1, 3, 4),
        (4, 4): (0, 1, 2, 5),
        (4, 5): (0, 1, 2, 6),
        (4, 6): (0, 1, 2, 7),
        (4, 7): (0, 1, 4, 5),
        (4, 8): (0, 1, 5, 6),
        (4, 9): (0, 1, 6, 7),
        (4, 10): (0, 2, 3, 5),
        (4, 11): (0, 1, 3, 5),
        (4, 12): (0, 2, 3, 6),
        (4, 13): (0, 1, 3, 6),
        (4, 14): (0, 2, 3, 7),
        (4, 15): (0, 1, 4, 6),
        (4, 16): (0, 1, 5, 7),
        (4, 17): (0, 3, 4, 7),
        (4, 18): (0, 1, 4, 7),
        (4, 19): (0, 1, 4, 8),
        (4, 20): (0, 1, 5, 8),
        (4, 21): (0, 2, 4, 6),
        (4, 22): (0, 2, 4, 7),
        (4, 23): (0, 2, 5, 7),
        (4, 24): (0, 2, 4, 8),
        (4, 25): (0, 2, 6, 8),
        (4, 26): (0, 3, 5, 8),
        (4, 27): (0, 2, 5, 8),
        (4, 28): (0, 3, 6, 9),
        (4, 29): (0, 1, 3, 7),
        # 5
        (5, 1): (0, 1, 2, 3, 4),
        (5, 2): (0, 1, 2, 3, 5),
        (5, 3): (0, 1, 2, 4, 5),
        (5, 4): (0, 1, 2, 3, 6),
        (5, 5): (0, 1, 2, 3, 7),
        (5, 6): (0, 1, 2, 5, 6),
        (5, 7): (0, 1, 2, 6, 7),
        (5, 8): (0, 2, 3, 4, 6),
        (5, 9): (0, 1, 2, 4, 6),
        (5, 10): (0, 1, 3, 4, 6),
        (5, 11): (0, 2, 3, 4, 7),
        (5, 12): (0, 1, 3, 5, 6),
        (5, 13): (0, 1, 2, 4, 8),
        (5, 14): (0, 1, 2, 5, 7),
        (5, 15): (0, 1, 2, 6, 8),
        (5, 16): (0, 1, 3, 4, 7),
        (5, 17): (0, 1, 3, 4, 8),
        (5, 18): (0, 1, 4, 5, 7),
        (5, 19): (0, 1, 3, 6, 7),
        (5, 20): (0, 1, 3, 7, 8),
        (5, 21): (0, 1, 4, 5, 8),
        (5, 22): (0, 1, 4, 7, 8),
        (5, 23): (0, 2, 3, 5, 7),
        (5, 24): (0, 1, 3, 5, 7),
        (5, 25): (0, 2, 3, 5, 8),
        (5, 26): (0, 2, 4, 5, 8),
        (5, 27): (0, 1, 3, 5, 8),
        (5, 28): (0, 2, 3, 6, 8),
        (5, 29): (0, 1, 3, 6, 8),
        (5, 30): (0, 1, 4, 6, 8),
        (5, 31): (0, 1, 3, 6, 9),
        (5, 32): (0, 1, 4, 6, 9),
        (5, 33): (0, 2, 4, 6, 8),
        (5, 34): (0, 2, 4, 6, 9),
        (5, 35): (0, 2, 4, 7, 9),
        (5, 36): (0, 1, 2, 4, 7),
        (5, 37): (0, 3, 4, 5, 8),
        (5, 38): (0, 1, 2, 5, 8),
        # 6
        (6, 1): (0, 1, 2, 3, 4, 5),
        (6, 2): (0, 1, 2, 3, 4, 6),
        (6, 3): (0, 1, 2, 3, 5, 6),
        (6, 4): (0, 1, 2, 4, 5, 6),
        (6, 5): (0, 1, 2, 3, 6, 7),
        (6, 6): (0, 1, 2, 5, 6, 7),
        (6, 7): (0, 1, 2, 6, 7, 8),
        (6, 8): (0, 2, 3, 4, 5, 7),
        (6, 9): (0, 1, 2, 3, 5, 7),
        (6, 10): (0, 1, 3, 4, 5, 7),
        (6, 11): (0, 1, 2, 4, 5, 7),
        (6, 12): (0, 1, 2, 4, 6, 7),
        (6, 13): (0, 1, 3, 4, 6, 7),
        (6, 14): (0, 1, 3, 4, 5, 8),
        (6, 15): (0, 1, 2, 4, 5, 8),
        (6, 16): (0, 1, 4, 5, 6, 8),
        (6, 17): (0, 1, 2, 4, 7, 8),
        (6, 18): (0, 1, 2, 5, 7, 8),
        (6, 19): (0, 1, 3, 4, 7, 8),
        (6, 20): (0, 1, 4, 5, 8, 9),
        (6, 21): (0, 2, 3, 4, 6, 8),
        (6, 22): (0, 1, 2, 4, 6, 8),
        (6, 23): (0, 2, 3, 5, 6, 8),
        (6, 24): (0, 1, 3, 4, 6, 8),
        (6, 25): (0, 1, 3, 5, 6, 8),
        (6, 26): (0, 1, 3, 5, 7, 8),
        (6, 27): (0, 1, 3, 4, 6, 9),
        (6, 28): (0, 1, 3, 5, 6, 9),
        (6, 29): (0, 1, 3, 6, 8, 9),
        (6, 30): (0, 1, 3, 6, 7, 9),
        (6, 31): (0, 1, 3, 5, 8, 9),
        (6, 32): (0, 2, 4, 5, 7, 9),
        (6, 33): (0, 2, 3, 5, 7, 9),
        (6, 34): (0, 1, 3, 5, 7, 9),
        (6, 35): (0, 2, 4, 6, 8, 10),
        (6, 36): (0, 1, 2, 3, 4, 7),
        (6, 37): (0, 1, 2, 3, 4, 8),
        (6, 38): (0, 1, 2, 3, 7, 8),
        (6, 39): (0, 2, 3, 4, 5, 8),
        (6, 40): (0, 1, 2, 3, 5, 8),
        (6, 41): (0, 1, 2, 3, 6, 8),
        (6, 42): (0, 1, 2, 3, 6, 9),
        (6, 43): (0, 1, 2, 5, 6, 8),
        (6, 44): (0, 1, 2, 5, 6, 9),
        (6, 45): (0, 2, 3, 4, 6, 9),
        (6, 46): (0, 1, 2, 4, 6, 9),
        (6, 47): (0, 1, 2, 4, 7, 9),
        (6, 48): (0, 1, 2, 5, 7, 9),
        (6, 49): (0, 1, 3, 4, 7, 9),
        (6, 50): (0, 1, 4, 6, 7, 9),
    }

    assert len(_forte_identifier_to_prime_form) == 137

    _lex_identifier_to_prime_form = {
        # 0
        (0, 1): (),
        # 1
        (1, 1): (0,),
        # 2
        (2, 1): (0, 1),
        (2, 2): (0, 2),
        (2, 3): (0, 3),
        (2, 4): (0, 4),
        (2, 5): (0, 5),
        (2, 6): (0, 6),
        # 3
        (3, 1): (0, 1, 2),
        (3, 2): (0, 1, 3),
        (3, 3): (0, 1, 4),
        (3, 4): (0, 1, 5),
        (3, 5): (0, 1, 6),
        (3, 6): (0, 2, 4),
        (3, 7): (0, 2, 5),
        (3, 8): (0, 2, 6),
        (3, 9): (0, 2, 7),
        (3, 10): (0, 3, 6),
        (3, 11): (0, 3, 7),
        (3, 12): (0, 4, 8),
        # 4
        (4, 1): (0, 1, 2, 3),
        (4, 2): (0, 1, 2, 4),
        (4, 3): (0, 1, 2, 5),
        (4, 4): (0, 1, 2, 6),
        (4, 5): (0, 1, 2, 7),
        (4, 6): (0, 1, 3, 4),
        (4, 7): (0, 1, 3, 5),
        (4, 8): (0, 1, 3, 6),
        (4, 9): (0, 1, 3, 7),
        (4, 10): (0, 1, 4, 5),
        (4, 11): (0, 1, 4, 6),
        (4, 12): (0, 1, 4, 7),
        (4, 13): (0, 1, 4, 8),
        (4, 14): (0, 1, 5, 6),
        (4, 15): (0, 1, 5, 7),
        (4, 16): (0, 1, 5, 8),
        (4, 17): (0, 1, 6, 7),
        (4, 18): (0, 2, 3, 5),
        (4, 19): (0, 2, 3, 6),
        (4, 20): (0, 2, 3, 7),
        (4, 21): (0, 2, 4, 6),
        (4, 22): (0, 2, 4, 7),
        (4, 23): (0, 2, 4, 8),
        (4, 24): (0, 2, 5, 7),
        (4, 25): (0, 2, 5, 8),
        (4, 26): (0, 2, 6, 8),
        (4, 27): (0, 3, 4, 7),
        (4, 28): (0, 3, 5, 8),
        (4, 29): (0, 3, 6, 9),
        # 5
        (5, 1): (0, 1, 2, 3, 4),
        (5, 2): (0, 1, 2, 3, 5),
        (5, 3): (0, 1, 2, 3, 6),
        (5, 4): (0, 1, 2, 3, 7),
        (5, 5): (0, 1, 2, 4, 5),
        (5, 6): (0, 1, 2, 4, 6),
        (5, 7): (0, 1, 2, 4, 7),
        (5, 8): (0, 1, 2, 4, 8),
        (5, 9): (0, 1, 2, 5, 6),
        (5, 10): (0, 1, 2, 5, 7),
        (5, 11): (0, 1, 2, 5, 8),
        (5, 12): (0, 1, 2, 6, 7),
        (5, 13): (0, 1, 2, 6, 8),
        (5, 14): (0, 1, 3, 4, 6),
        (5, 15): (0, 1, 3, 4, 7),
        (5, 16): (0, 1, 3, 4, 8),
        (5, 17): (0, 1, 3, 5, 6),
        (5, 18): (0, 1, 3, 5, 7),
        (5, 19): (0, 1, 3, 5, 8),
        (5, 20): (0, 1, 3, 6, 7),
        (5, 21): (0, 1, 3, 6, 8),
        (5, 22): (0, 1, 3, 6, 9),
        (5, 23): (0, 1, 3, 7, 8),
        (5, 24): (0, 1, 4, 5, 7),
        (5, 25): (0, 1, 4, 5, 8),
        (5, 26): (0, 1, 4, 6, 8),
        (5, 27): (0, 1, 4, 7, 8),
        (5, 28): (0, 1, 4, 7, 9),
        (5, 29): (0, 2, 3, 4, 6),
        (5, 30): (0, 2, 3, 4, 7),
        (5, 31): (0, 2, 3, 5, 7),
        (5, 32): (0, 2, 3, 5, 8),
        (5, 33): (0, 2, 3, 6, 8),
        (5, 34): (0, 2, 4, 5, 8),
        (5, 35): (0, 2, 4, 6, 8),
        (5, 36): (0, 2, 4, 6, 9),
        (5, 37): (0, 2, 4, 7, 9),
        (5, 38): (0, 3, 4, 5, 8),
        # 6
        (6, 1): (0, 1, 2, 3, 4, 5),
        (6, 2): (0, 1, 2, 3, 4, 6),
        (6, 3): (0, 1, 2, 3, 4, 7),
        (6, 4): (0, 1, 2, 3, 4, 8),
        (6, 5): (0, 1, 2, 3, 5, 6),
        (6, 6): (0, 1, 2, 3, 5, 7),
        (6, 7): (0, 1, 2, 3, 5, 8),
        (6, 8): (0, 1, 2, 3, 6, 7),
        (6, 9): (0, 1, 2, 3, 6, 8),
        (6, 10): (0, 1, 2, 3, 6, 9),
        (6, 11): (0, 1, 2, 3, 7, 8),
        (6, 12): (0, 1, 2, 4, 5, 6),
        (6, 13): (0, 1, 2, 4, 5, 7),
        (6, 14): (0, 1, 2, 4, 5, 8),
        (6, 15): (0, 1, 2, 4, 6, 7),
        (6, 16): (0, 1, 2, 4, 6, 8),
        (6, 17): (0, 1, 2, 4, 6, 9),
        (6, 18): (0, 1, 2, 4, 7, 8),
        (6, 19): (0, 1, 2, 4, 7, 9),
        (6, 20): (0, 1, 2, 5, 6, 7),
        (6, 21): (0, 1, 2, 5, 6, 8),
        (6, 22): (0, 1, 2, 5, 7, 8),
        (6, 23): (0, 1, 2, 5, 7, 9),
        (6, 24): (0, 1, 2, 5, 8, 9),
        (6, 25): (0, 1, 2, 6, 7, 8),
        (6, 26): (0, 1, 3, 4, 5, 7),
        (6, 27): (0, 1, 3, 4, 5, 8),
        (6, 28): (0, 1, 3, 4, 6, 7),
        (6, 29): (0, 1, 3, 4, 6, 8),
        (6, 30): (0, 1, 3, 4, 6, 9),
        (6, 31): (0, 1, 3, 4, 7, 8),
        (6, 32): (0, 1, 3, 4, 7, 9),
        (6, 33): (0, 1, 3, 5, 6, 8),
        (6, 34): (0, 1, 3, 5, 6, 9),
        (6, 35): (0, 1, 3, 5, 7, 8),
        (6, 36): (0, 1, 3, 5, 7, 9),
        (6, 37): (0, 1, 3, 5, 8, 9),
        (6, 38): (0, 1, 3, 6, 7, 9),
        (6, 39): (0, 1, 3, 6, 8, 9),
        (6, 40): (0, 1, 4, 5, 6, 8),
        (6, 41): (0, 1, 4, 5, 8, 9),
        (6, 42): (0, 1, 4, 6, 7, 9),
        (6, 43): (0, 2, 3, 4, 5, 7),
        (6, 44): (0, 2, 3, 4, 5, 8),
        (6, 45): (0, 2, 3, 4, 6, 8),
        (6, 46): (0, 2, 3, 4, 6, 9),
        (6, 47): (0, 2, 3, 5, 6, 8),
        (6, 48): (0, 2, 3, 5, 7, 9),
        (6, 49): (0, 2, 4, 5, 7, 9),
        (6, 50): (0, 2, 4, 6, 8, 10),
        # 7
        (7, 1): (0, 1, 2, 3, 4, 5, 6),
        (7, 2): (0, 1, 2, 3, 4, 5, 7),
        (7, 3): (0, 1, 2, 3, 4, 5, 8),
        (7, 4): (0, 1, 2, 3, 4, 6, 7),
        (7, 5): (0, 1, 2, 3, 4, 6, 8),
        (7, 6): (0, 1, 2, 3, 4, 6, 9),
        (7, 7): (0, 1, 2, 3, 4, 7, 8),
        (7, 8): (0, 1, 2, 3, 4, 7, 9),
        (7, 9): (0, 1, 2, 3, 5, 6, 7),
        (7, 10): (0, 1, 2, 3, 5, 6, 8),
        (7, 11): (0, 1, 2, 3, 5, 6, 9),
        (7, 12): (0, 1, 2, 3, 5, 7, 8),
        (7, 13): (0, 1, 2, 3, 5, 7, 9),
        (7, 14): (0, 1, 2, 3, 5, 8, 9),
        (7, 15): (0, 1, 2, 3, 6, 7, 8),
        (7, 16): (0, 1, 2, 3, 6, 8, 9),
        (7, 17): (0, 1, 2, 4, 5, 6, 8),
        (7, 18): (0, 1, 2, 4, 5, 6, 9),
        (7, 19): (0, 1, 2, 4, 5, 7, 8),
        (7, 20): (0, 1, 2, 4, 5, 7, 9),
        (7, 21): (0, 1, 2, 4, 5, 8, 9),
        (7, 22): (0, 1, 2, 4, 6, 7, 8),
        (7, 23): (0, 1, 2, 4, 6, 7, 9),
        (7, 24): (0, 1, 2, 4, 6, 8, 10),
        (7, 25): (0, 1, 2, 4, 6, 8, 9),
        (7, 26): (0, 1, 2, 4, 7, 8, 9),
        (7, 27): (0, 1, 2, 5, 6, 8, 9),
        (7, 28): (0, 1, 3, 4, 5, 6, 8),
        (7, 29): (0, 1, 3, 4, 5, 7, 8),
        (7, 30): (0, 1, 3, 4, 5, 7, 9),
        (7, 31): (0, 1, 3, 4, 6, 7, 9),
        (7, 32): (0, 1, 3, 4, 6, 8, 10),
        (7, 33): (0, 1, 3, 4, 6, 8, 9),
        (7, 34): (0, 1, 3, 5, 6, 7, 9),
        (7, 35): (0, 1, 3, 5, 6, 8, 10),
        (7, 36): (0, 2, 3, 4, 5, 6, 8),
        (7, 37): (0, 2, 3, 4, 5, 7, 9),
        (7, 38): (0, 2, 3, 4, 6, 7, 9),
        # 8
        (8, 1): (0, 1, 2, 3, 4, 5, 6, 7),
        (8, 2): (0, 1, 2, 3, 4, 5, 6, 8),
        (8, 3): (0, 1, 2, 3, 4, 5, 6, 9),
        (8, 4): (0, 1, 2, 3, 4, 5, 7, 8),
        (8, 5): (0, 1, 2, 3, 4, 5, 7, 9),
        (8, 6): (0, 1, 2, 3, 4, 5, 8, 9),
        (8, 7): (0, 1, 2, 3, 4, 6, 7, 8),
        (8, 8): (0, 1, 2, 3, 4, 6, 7, 9),
        (8, 9): (0, 1, 2, 3, 4, 6, 8, 10),
        (8, 10): (0, 1, 2, 3, 4, 6, 8, 9),
        (8, 11): (0, 1, 2, 3, 4, 7, 8, 9),
        (8, 12): (0, 1, 2, 3, 5, 6, 7, 8),
        (8, 13): (0, 1, 2, 3, 5, 6, 7, 9),
        (8, 14): (0, 1, 2, 3, 5, 6, 8, 9),
        (8, 15): (0, 1, 2, 3, 5, 7, 8, 10),
        (8, 16): (0, 1, 2, 3, 5, 7, 8, 9),
        (8, 17): (0, 1, 2, 3, 5, 7, 9, 10),
        (8, 18): (0, 1, 2, 3, 6, 7, 8, 9),
        (8, 19): (0, 1, 2, 4, 5, 6, 7, 9),
        (8, 20): (0, 1, 2, 4, 5, 6, 8, 10),
        (8, 21): (0, 1, 2, 4, 5, 6, 8, 9),
        (8, 22): (0, 1, 2, 4, 5, 7, 8, 10),
        (8, 23): (0, 1, 2, 4, 5, 7, 8, 9),
        (8, 24): (0, 1, 2, 4, 5, 7, 9, 10),
        (8, 25): (0, 1, 2, 4, 6, 7, 8, 10),
        (8, 26): (0, 1, 3, 4, 5, 6, 7, 9),
        (8, 27): (0, 1, 3, 4, 5, 6, 8, 9),
        (8, 28): (0, 1, 3, 4, 6, 7, 9, 10),
        (8, 29): (0, 2, 3, 4, 5, 6, 7, 9),
        # 9
        (9, 1): (0, 1, 2, 3, 4, 5, 6, 7, 8),
        (9, 2): (0, 1, 2, 3, 4, 5, 6, 7, 9),
        (9, 3): (0, 1, 2, 3, 4, 5, 6, 8, 10),
        (9, 4): (0, 1, 2, 3, 4, 5, 6, 8, 9),
        (9, 5): (0, 1, 2, 3, 4, 5, 7, 8, 9),
        (9, 6): (0, 1, 2, 3, 4, 5, 7, 9, 10),
        (9, 7): (0, 1, 2, 3, 4, 6, 7, 8, 9),
        (9, 8): (0, 1, 2, 3, 4, 6, 7, 9, 10),
        (9, 9): (0, 1, 2, 3, 4, 6, 8, 9, 10),
        (9, 10): (0, 1, 2, 3, 5, 6, 7, 8, 10),
        (9, 11): (0, 1, 2, 3, 5, 6, 8, 9, 10),
        (9, 12): (0, 1, 2, 4, 5, 6, 8, 9, 10),
        # 10
        (10, 1): (0, 1, 2, 3, 4, 5, 6, 7, 8, 10),
        (10, 2): (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
        (10, 3): (0, 1, 2, 3, 4, 5, 6, 7, 9, 10),
        (10, 4): (0, 1, 2, 3, 4, 5, 6, 8, 9, 10),
        (10, 5): (0, 1, 2, 3, 4, 5, 7, 8, 9, 10),
        (10, 6): (0, 1, 2, 3, 4, 6, 7, 8, 9, 10),
        # 11
        (11, 1): (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
        # 12
        (12, 1): (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11),
    }

    assert len(_lex_identifier_to_prime_form) == 224

    _transposition_only_identifier_to_prime_form = {
        # 0
        (0, 1): (),
        # 1
        (1, 1): (0),
        # 2
        (2, 1): (0, 1),
        (2, 2): (0, 2),
        (2, 3): (0, 3),
        (2, 4): (0, 4),
        (2, 5): (0, 5),
        (2, 6): (0, 6),
        # 3
        (3, 1): (0, 1, 2),
        (3, 2): (0, 1, 3),
        (3, 3): (0, 1, 4),
        (3, 4): (0, 1, 5),
        (3, 5): (0, 1, 6),
        (3, 6): (0, 2, 3),
        (3, 7): (0, 2, 4),
        (3, 8): (0, 2, 5),
        (3, 9): (0, 2, 6),
        (3, 10): (0, 2, 7),
        (3, 11): (0, 3, 4),
        (3, 12): (0, 3, 5),
        (3, 13): (0, 3, 6),
        (3, 14): (0, 3, 7),
        (3, 15): (0, 4, 5),
        (3, 16): (0, 4, 6),
        (3, 17): (0, 4, 7),
        (3, 18): (0, 4, 8),
        (3, 19): (0, 5, 6),
        # 4
        (4, 1): (0, 1, 2, 3),
        (4, 2): (0, 1, 2, 4),
        (4, 3): (0, 1, 2, 5),
        (4, 4): (0, 1, 2, 6),
        (4, 5): (0, 1, 2, 7),
        (4, 6): (0, 1, 3, 4),
        (4, 7): (0, 1, 3, 5),
        (4, 8): (0, 1, 3, 6),
        (4, 9): (0, 1, 3, 7),
        (4, 10): (0, 1, 4, 5),
        (4, 11): (0, 1, 4, 6),
        (4, 12): (0, 1, 4, 7),
        (4, 13): (0, 1, 4, 8),
        (4, 14): (0, 1, 5, 6),
        (4, 15): (0, 1, 5, 7),
        (4, 16): (0, 1, 5, 8),
        (4, 17): (0, 1, 6, 7),
        (4, 18): (0, 2, 3, 4),
        (4, 19): (0, 2, 3, 5),
        (4, 20): (0, 2, 3, 6),
        (4, 21): (0, 2, 3, 7),
        (4, 22): (0, 2, 4, 5),
        (4, 23): (0, 2, 4, 6),
        (4, 24): (0, 2, 4, 7),
        (4, 25): (0, 2, 4, 8),
        (4, 26): (0, 2, 5, 6),
        (4, 27): (0, 2, 5, 7),
        (4, 28): (0, 2, 5, 8),
        (4, 29): (0, 2, 6, 7),
        (4, 30): (0, 2, 6, 8),
        (4, 31): (0, 3, 4, 5),
        (4, 32): (0, 3, 4, 6),
        (4, 33): (0, 3, 4, 7),
        (4, 34): (0, 3, 4, 8),
        (4, 35): (0, 3, 5, 6),
        (4, 36): (0, 3, 5, 7),
        (4, 37): (0, 3, 5, 8),
        (4, 38): (0, 3, 6, 7),
        (4, 39): (0, 3, 6, 8),
        (4, 40): (0, 3, 6, 9),
        (4, 41): (0, 4, 5, 6),
        (4, 42): (0, 4, 5, 7),
        (4, 43): (0, 4, 6, 7),
        # 5
        (5, 1): (0, 1, 2, 3, 4),
        (5, 2): (0, 1, 2, 3, 5),
        (5, 3): (0, 1, 2, 3, 6),
        (5, 4): (0, 1, 2, 3, 7),
        (5, 5): (0, 1, 2, 4, 5),
        (5, 6): (0, 1, 2, 4, 6),
        (5, 7): (0, 1, 2, 4, 7),
        (5, 8): (0, 1, 2, 4, 8),
        (5, 9): (0, 1, 2, 5, 6),
        (5, 10): (0, 1, 2, 5, 7),
        (5, 11): (0, 1, 2, 5, 8),
        (5, 12): (0, 1, 2, 6, 7),
        (5, 13): (0, 1, 2, 6, 8),
        (5, 14): (0, 1, 3, 4, 5),
        (5, 15): (0, 1, 3, 4, 6),
        (5, 16): (0, 1, 3, 4, 7),
        (5, 17): (0, 1, 3, 4, 8),
        (5, 18): (0, 1, 3, 5, 6),
        (5, 19): (0, 1, 3, 5, 7),
        (5, 20): (0, 1, 3, 5, 8),
        (5, 21): (0, 1, 3, 6, 7),
        (5, 22): (0, 1, 3, 6, 8),
        (5, 23): (0, 1, 3, 6, 9),
        (5, 24): (0, 1, 3, 7, 8),
        (5, 25): (0, 1, 4, 5, 6),
        (5, 26): (0, 1, 4, 5, 7),
        (5, 27): (0, 1, 4, 5, 8),
        (5, 28): (0, 1, 4, 6, 7),
        (5, 29): (0, 1, 4, 6, 8),
        (5, 30): (0, 1, 4, 6, 9),
        (5, 31): (0, 1, 4, 7, 8),
        (5, 32): (0, 1, 4, 7, 9),
        (5, 33): (0, 1, 5, 6, 7),
        (5, 34): (0, 1, 5, 7, 8),
        (5, 35): (0, 2, 3, 4, 5),
        (5, 36): (0, 2, 3, 4, 6),
        (5, 37): (0, 2, 3, 4, 7),
        (5, 38): (0, 2, 3, 4, 8),
        (5, 39): (0, 2, 3, 5, 6),
        (5, 40): (0, 2, 3, 5, 7),
        (5, 41): (0, 2, 3, 5, 8),
        (5, 42): (0, 2, 3, 6, 7),
        (5, 43): (0, 2, 3, 6, 8),
        (5, 44): (0, 2, 3, 6, 9),
        (5, 45): (0, 2, 4, 5, 6),
        (5, 46): (0, 2, 4, 5, 7),
        (5, 47): (0, 2, 4, 5, 8),
        (5, 48): (0, 2, 4, 6, 7),
        (5, 49): (0, 2, 4, 6, 8),
        (5, 50): (0, 2, 4, 6, 9),
        (5, 51): (0, 2, 4, 7, 8),
        (5, 52): (0, 2, 4, 7, 9),
        (5, 53): (0, 2, 5, 6, 7),
        (5, 54): (0, 2, 5, 6, 8),
        (5, 55): (0, 2, 5, 7, 8),
        (5, 56): (0, 3, 4, 5, 6),
        (5, 57): (0, 3, 4, 5, 7),
        (5, 58): (0, 3, 4, 5, 8),
        (5, 59): (0, 3, 4, 6, 7),
        (5, 60): (0, 3, 4, 6, 8),
        (5, 61): (0, 3, 4, 7, 8),
        (5, 62): (0, 3, 5, 6, 7),
        (5, 63): (0, 3, 5, 6, 8),
        (5, 64): (0, 3, 5, 7, 8),
        (5, 65): (0, 3, 6, 7, 8),
        (5, 66): (0, 4, 5, 6, 7),
        # 6
        (6, 1): (0, 1, 2, 3, 4, 5),
        (6, 2): (0, 1, 2, 3, 4, 6),
        (6, 3): (0, 1, 2, 3, 4, 7),
        (6, 4): (0, 1, 2, 3, 4, 8),
        (6, 5): (0, 1, 2, 3, 5, 6),
        (6, 6): (0, 1, 2, 3, 5, 7),
        (6, 7): (0, 1, 2, 3, 5, 8),
        (6, 8): (0, 1, 2, 3, 6, 7),
        (6, 9): (0, 1, 2, 3, 6, 8),
        (6, 10): (0, 1, 2, 3, 6, 9),
        (6, 11): (0, 1, 2, 3, 7, 8),
        (6, 12): (0, 1, 2, 4, 5, 6),
        (6, 13): (0, 1, 2, 4, 5, 7),
        (6, 14): (0, 1, 2, 4, 5, 8),
        (6, 15): (0, 1, 2, 4, 6, 7),
        (6, 16): (0, 1, 2, 4, 6, 8),
        (6, 17): (0, 1, 2, 4, 6, 9),
        (6, 18): (0, 1, 2, 4, 7, 8),
        (6, 19): (0, 1, 2, 4, 7, 9),
        (6, 20): (0, 1, 2, 5, 6, 7),
        (6, 21): (0, 1, 2, 5, 6, 8),
        (6, 22): (0, 1, 2, 5, 6, 9),
        (6, 23): (0, 1, 2, 5, 7, 8),
        (6, 24): (0, 1, 2, 5, 7, 9),
        (6, 25): (0, 1, 2, 5, 8, 9),
        (6, 26): (0, 1, 2, 6, 7, 8),
        (6, 27): (0, 1, 3, 4, 5, 6),
        (6, 28): (0, 1, 3, 4, 5, 7),
        (6, 29): (0, 1, 3, 4, 5, 8),
        (6, 30): (0, 1, 3, 4, 6, 7),
        (6, 31): (0, 1, 3, 4, 6, 8),
        (6, 32): (0, 1, 3, 4, 6, 9),
        (6, 33): (0, 1, 3, 4, 7, 8),
        (6, 34): (0, 1, 3, 4, 7, 9),
        (6, 35): (0, 1, 3, 5, 6, 7),
        (6, 36): (0, 1, 3, 5, 6, 8),
        (6, 37): (0, 1, 3, 5, 6, 9),
        (6, 38): (0, 1, 3, 5, 7, 8),
        (6, 39): (0, 1, 3, 5, 7, 9),
        (6, 40): (0, 1, 3, 5, 8, 9),
        (6, 41): (0, 1, 3, 6, 7, 8),
        (6, 42): (0, 1, 3, 6, 7, 9),
        (6, 43): (0, 1, 3, 6, 8, 9),
        (6, 44): (0, 1, 4, 5, 6, 7),
        (6, 45): (0, 1, 4, 5, 6, 8),
        (6, 46): (0, 1, 4, 5, 7, 8),
        (6, 47): (0, 1, 4, 5, 8, 9),
        (6, 48): (0, 1, 4, 6, 7, 8),
        (6, 49): (0, 1, 4, 6, 7, 9),
        (6, 50): (0, 1, 4, 6, 8, 9),
        (6, 51): (0, 2, 3, 4, 5, 6),
        (6, 52): (0, 2, 3, 4, 5, 7),
        (6, 53): (0, 2, 3, 4, 5, 8),
        (6, 54): (0, 2, 3, 4, 6, 7),
        (6, 55): (0, 2, 3, 4, 6, 8),
        (6, 56): (0, 2, 3, 4, 6, 9),
        (6, 57): (0, 2, 3, 4, 7, 8),
        (6, 58): (0, 2, 3, 4, 7, 9),
        (6, 59): (0, 2, 3, 5, 6, 7),
        (6, 60): (0, 2, 3, 5, 6, 8),
        (6, 61): (0, 2, 3, 5, 6, 9),
        (6, 62): (0, 2, 3, 5, 7, 8),
        (6, 63): (0, 2, 3, 5, 7, 9),
        (6, 64): (0, 2, 3, 6, 7, 8),
        (6, 65): (0, 2, 3, 6, 8, 9),
        (6, 66): (0, 2, 4, 5, 6, 7),
        (6, 67): (0, 2, 4, 5, 6, 8),
        (6, 68): (0, 2, 4, 5, 6, 9),
        (6, 69): (0, 2, 4, 5, 7, 8),
        (6, 70): (0, 2, 4, 5, 7, 9),
        (6, 71): (0, 2, 4, 6, 7, 8),
        (6, 72): (0, 2, 4, 6, 7, 9),
        (6, 73): (0, 2, 4, 6, 8, 10),
        (6, 74): (0, 2, 4, 6, 8, 9),
        (6, 75): (0, 2, 5, 6, 7, 8),
        (6, 76): (0, 3, 4, 5, 6, 7),
        (6, 77): (0, 3, 4, 5, 6, 8),
        (6, 78): (0, 3, 4, 5, 7, 8),
        (6, 79): (0, 3, 4, 6, 7, 8),
        (6, 80): (0, 3, 5, 6, 7, 8),
        # 7
        (7, 1): (0, 1, 2, 3, 4, 5, 6),
        (7, 2): (0, 1, 2, 3, 4, 5, 7),
        (7, 3): (0, 1, 2, 3, 4, 5, 8),
        (7, 4): (0, 1, 2, 3, 4, 6, 7),
        (7, 5): (0, 1, 2, 3, 4, 6, 8),
        (7, 6): (0, 1, 2, 3, 4, 6, 9),
        (7, 7): (0, 1, 2, 3, 4, 7, 8),
        (7, 8): (0, 1, 2, 3, 4, 7, 9),
        (7, 9): (0, 1, 2, 3, 5, 6, 7),
        (7, 10): (0, 1, 2, 3, 5, 6, 8),
        (7, 11): (0, 1, 2, 3, 5, 6, 9),
        (7, 12): (0, 1, 2, 3, 5, 7, 8),
        (7, 13): (0, 1, 2, 3, 5, 7, 9),
        (7, 14): (0, 1, 2, 3, 5, 8, 9),
        (7, 15): (0, 1, 2, 3, 6, 7, 8),
        (7, 16): (0, 1, 2, 3, 6, 7, 9),
        (7, 17): (0, 1, 2, 3, 6, 8, 9),
        (7, 18): (0, 1, 2, 4, 5, 6, 7),
        (7, 19): (0, 1, 2, 4, 5, 6, 8),
        (7, 20): (0, 1, 2, 4, 5, 6, 9),
        (7, 21): (0, 1, 2, 4, 5, 7, 8),
        (7, 22): (0, 1, 2, 4, 5, 7, 9),
        (7, 23): (0, 1, 2, 4, 5, 8, 9),
        (7, 24): (0, 1, 2, 4, 6, 7, 8),
        (7, 25): (0, 1, 2, 4, 6, 7, 9),
        (7, 26): (0, 1, 2, 4, 6, 8, 10),
        (7, 27): (0, 1, 2, 4, 6, 8, 9),
        (7, 28): (0, 1, 2, 4, 7, 8, 9),
        (7, 29): (0, 1, 2, 5, 6, 7, 8),
        (7, 30): (0, 1, 2, 5, 6, 8, 9),
        (7, 31): (0, 1, 2, 5, 7, 8, 9),
        (7, 32): (0, 1, 3, 4, 5, 6, 7),
        (7, 33): (0, 1, 3, 4, 5, 6, 8),
        (7, 34): (0, 1, 3, 4, 5, 6, 9),
        (7, 35): (0, 1, 3, 4, 5, 7, 8),
        (7, 36): (0, 1, 3, 4, 5, 7, 9),
        (7, 37): (0, 1, 3, 4, 5, 8, 9),
        (7, 38): (0, 1, 3, 4, 6, 7, 8),
        (7, 39): (0, 1, 3, 4, 6, 7, 9),
        (7, 40): (0, 1, 3, 4, 6, 8, 10),
        (7, 41): (0, 1, 3, 4, 6, 8, 9),
        (7, 42): (0, 1, 3, 5, 6, 7, 8),
        (7, 43): (0, 1, 3, 5, 6, 7, 9),
        (7, 44): (0, 1, 3, 5, 6, 8, 10),
        (7, 45): (0, 1, 3, 5, 6, 8, 9),
        (7, 46): (0, 1, 3, 5, 7, 8, 9),
        (7, 47): (0, 1, 4, 5, 6, 7, 8),
        (7, 48): (0, 1, 4, 6, 7, 8, 9),
        (7, 49): (0, 2, 3, 4, 5, 6, 7),
        (7, 50): (0, 2, 3, 4, 5, 6, 8),
        (7, 51): (0, 2, 3, 4, 5, 6, 9),
        (7, 52): (0, 2, 3, 4, 5, 7, 8),
        (7, 53): (0, 2, 3, 4, 5, 7, 9),
        (7, 54): (0, 2, 3, 4, 6, 7, 8),
        (7, 55): (0, 2, 3, 4, 6, 7, 9),
        (7, 56): (0, 2, 3, 4, 6, 8, 9),
        (7, 57): (0, 2, 3, 5, 6, 7, 8),
        (7, 58): (0, 2, 3, 5, 6, 7, 9),
        (7, 59): (0, 2, 3, 5, 6, 8, 9),
        (7, 60): (0, 2, 3, 5, 7, 8, 9),
        (7, 61): (0, 2, 4, 5, 6, 7, 8),
        (7, 62): (0, 2, 4, 5, 6, 7, 9),
        (7, 63): (0, 2, 4, 5, 6, 8, 9),
        (7, 64): (0, 2, 4, 5, 7, 8, 9),
        (7, 65): (0, 2, 4, 6, 7, 8, 9),
        (7, 66): (0, 3, 4, 5, 6, 7, 8),
        # 8
        (8, 1): (0, 1, 2, 3, 4, 5, 6, 7),
        (8, 2): (0, 1, 2, 3, 4, 5, 6, 8),
        (8, 3): (0, 1, 2, 3, 4, 5, 6, 9),
        (8, 4): (0, 1, 2, 3, 4, 5, 7, 8),
        (8, 5): (0, 1, 2, 3, 4, 5, 7, 9),
        (8, 6): (0, 1, 2, 3, 4, 5, 8, 9),
        (8, 7): (0, 1, 2, 3, 4, 6, 7, 8),
        (8, 8): (0, 1, 2, 3, 4, 6, 7, 9),
        (8, 9): (0, 1, 2, 3, 4, 6, 8, 10),
        (8, 10): (0, 1, 2, 3, 4, 6, 8, 9),
        (8, 11): (0, 1, 2, 3, 4, 7, 8, 9),
        (8, 12): (0, 1, 2, 3, 5, 6, 7, 8),
        (8, 13): (0, 1, 2, 3, 5, 6, 7, 9),
        (8, 14): (0, 1, 2, 3, 5, 6, 8, 10),
        (8, 15): (0, 1, 2, 3, 5, 6, 8, 9),
        (8, 16): (0, 1, 2, 3, 5, 7, 8, 10),
        (8, 17): (0, 1, 2, 3, 5, 7, 8, 9),
        (8, 18): (0, 1, 2, 3, 5, 7, 9, 10),
        (8, 19): (0, 1, 2, 3, 6, 7, 8, 9),
        (8, 20): (0, 1, 2, 4, 5, 6, 7, 8),
        (8, 21): (0, 1, 2, 4, 5, 6, 7, 9),
        (8, 22): (0, 1, 2, 4, 5, 6, 8, 10),
        (8, 23): (0, 1, 2, 4, 5, 6, 8, 9),
        (8, 24): (0, 1, 2, 4, 5, 7, 8, 10),
        (8, 25): (0, 1, 2, 4, 5, 7, 8, 9),
        (8, 26): (0, 1, 2, 4, 5, 7, 9, 10),
        (8, 27): (0, 1, 2, 4, 6, 7, 8, 10),
        (8, 28): (0, 1, 2, 4, 6, 7, 8, 9),
        (8, 29): (0, 1, 2, 4, 6, 7, 9, 10),
        (8, 30): (0, 1, 3, 4, 5, 6, 7, 8),
        (8, 31): (0, 1, 3, 4, 5, 6, 7, 9),
        (8, 32): (0, 1, 3, 4, 5, 6, 8, 9),
        (8, 33): (0, 1, 3, 4, 5, 7, 8, 9),
        (8, 34): (0, 1, 3, 4, 6, 7, 8, 9),
        (8, 35): (0, 1, 3, 4, 6, 7, 9, 10),
        (8, 36): (0, 1, 3, 5, 6, 7, 8, 9),
        (8, 37): (0, 2, 3, 4, 5, 6, 7, 8),
        (8, 38): (0, 2, 3, 4, 5, 6, 7, 9),
        (8, 39): (0, 2, 3, 4, 5, 6, 8, 9),
        (8, 40): (0, 2, 3, 4, 5, 7, 8, 9),
        (8, 41): (0, 2, 3, 4, 6, 7, 8, 9),
        (8, 42): (0, 2, 3, 5, 6, 7, 8, 9),
        (8, 43): (0, 2, 4, 5, 6, 7, 8, 9),
        # 9
        (9, 1): (0, 1, 2, 3, 4, 5, 6, 7, 8),
        (9, 2): (0, 1, 2, 3, 4, 5, 6, 7, 9),
        (9, 3): (0, 1, 2, 3, 4, 5, 6, 8, 10),
        (9, 4): (0, 1, 2, 3, 4, 5, 6, 8, 9),
        (9, 5): (0, 1, 2, 3, 4, 5, 7, 8, 10),
        (9, 6): (0, 1, 2, 3, 4, 5, 7, 8, 9),
        (9, 7): (0, 1, 2, 3, 4, 5, 7, 9, 10),
        (9, 8): (0, 1, 2, 3, 4, 6, 7, 8, 10),
        (9, 9): (0, 1, 2, 3, 4, 6, 7, 8, 9),
        (9, 10): (0, 1, 2, 3, 4, 6, 7, 9, 10),
        (9, 11): (0, 1, 2, 3, 4, 6, 8, 9, 10),
        (9, 12): (0, 1, 2, 3, 5, 6, 7, 8, 10),
        (9, 13): (0, 1, 2, 3, 5, 6, 7, 8, 9),
        (9, 14): (0, 1, 2, 3, 5, 6, 7, 9, 10),
        (9, 15): (0, 1, 2, 3, 5, 6, 8, 9, 10),
        (9, 16): (0, 1, 2, 4, 5, 6, 7, 8, 9),
        (9, 17): (0, 1, 2, 4, 5, 6, 8, 9, 10),
        (9, 18): (0, 1, 3, 4, 5, 6, 7, 8, 9),
        (9, 19): (0, 2, 3, 4, 5, 6, 7, 8, 9),
        # 10
        (10, 1): (0, 1, 2, 3, 4, 5, 6, 7, 8, 10),
        (10, 2): (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
        (10, 3): (0, 1, 2, 3, 4, 5, 6, 7, 9, 10),
        (10, 4): (0, 1, 2, 3, 4, 5, 6, 8, 9, 10),
        (10, 5): (0, 1, 2, 3, 4, 5, 7, 8, 9, 10),
        (10, 6): (0, 1, 2, 3, 4, 6, 7, 8, 9, 10),
        # 11
        (11, 1): (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
        # 12
        (12, 1): (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11),
    }

    assert len(_transposition_only_identifier_to_prime_form) == 352

    _prime_form_to_forte_identifier = {
        v: k for k, v in _forte_identifier_to_prime_form.items()
    }

    _prime_form_to_lex_identifier = {
        v: k for k, v in _lex_identifier_to_prime_form.items()
    }

    _prime_form_to_transposition_only_identifier = {
        v: k for k, v in _transposition_only_identifier_to_prime_form.items()
    }

    ### INITIALIZER ###

    def __init__(
        self, cardinality=1, rank=1, *, lex_rank=None, transposition_only=None
    ):
        if bool(transposition_only) and lex_rank is False:
            raise Exception("SG1 set-classes are always lex-rank.")
        cardinality = int(cardinality)
        assert 0 <= cardinality <= 12, repr(cardinality)
        self._cardinality = cardinality
        rank = int(rank)
        assert 1 <= rank, repr(rank)
        self._rank = rank
        assert isinstance(lex_rank, (type(None), type(True)))
        self._lex_rank = lex_rank
        assert isinstance(transposition_only, (type(None), type(True)))
        self._transposition_only = transposition_only
        prime_form = self._unrank(
            self.cardinality,
            self.rank,
            transposition_only=self.transposition_only,
        )
        self._prime_form = prime_form

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Delegates to ``abjad.format.compare_objects()``.
        """
        return _format.compare_objects(self, argument)

    def __hash__(self) -> int:
        """
        Hashes set-class.
        """
        return hash(self.__class__.__name__ + str(self))

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return _format.get_repr(self)

    def __str__(self):
        """
        Gets string representation.

        ..  container:: example

            Gets string of SG2 set-class with Forte rank:

            >>> set_class = abjad.SetClass(4, 29)
            >>> print(set_class)
            SC(4-29){0, 1, 3, 7}

        ..  container:: example

            Gets string of SG2 set-class with lex rank:

            >>> set_class = abjad.SetClass(
            ...     4, 29,
            ...     lex_rank=True,
            ... )
            >>> print(set_class)
            SC(4-29){0, 3, 6, 9}

        ..  container:: example

            Gets string of SG1 set-class:

            >>> set_class = abjad.SetClass(
            ...     4, 29,
            ...     transposition_only=True,
            ... )
            >>> print(set_class)
            SC(4-29){0, 2, 6, 7}

        Returns string.
        """
        string = f"SC({self.cardinality}-{self.rank}){self.prime_form!s}"
        string = string.replace("PC", "")
        return string

    ### PRIVATE METHODS ###

    def _unrank(self, cardinality, rank, transposition_only=None):
        pair = (cardinality, rank)
        if self.transposition_only:
            prime_form = self._transposition_only_identifier_to_prime_form[pair]
        elif self.lex_rank:
            prime_form = self._lex_identifier_to_prime_form[pair]
        else:
            prime_form = self._forte_identifier_to_prime_form[pair]
        prime_form = PitchClassSet(items=prime_form, item_class=NumberedPitchClass)
        return prime_form

    ### PUBLIC PROPERTIES ###

    @property
    def cardinality(self):
        """
        Gets cardinality.

        ..  container:: example

            Gets cardinality of SG2 set-class with Forte rank:

            >>> set_class = abjad.SetClass(4, 29)
            >>> print(set_class)
            SC(4-29){0, 1, 3, 7}

            >>> set_class.cardinality
            4

        ..  container:: example

            Gets cardinality of SG2 set-class with lex rank:

            >>> set_class = abjad.SetClass(
            ...     4, 29,
            ...     lex_rank=True,
            ... )
            >>> print(set_class)
            SC(4-29){0, 3, 6, 9}

            >>> set_class.cardinality
            4

        ..  container:: example

            Gets cardinality of SG1 set-class:

            >>> set_class = abjad.SetClass(
            ...     4, 29,
            ...     transposition_only=True,
            ... )
            >>> print(set_class)
            SC(4-29){0, 2, 6, 7}

            >>> set_class.cardinality
            4

        Set to integer between 0 and 12, inclusive.

        Returns integer between 0 and 12, inclusive.
        """
        return self._cardinality

    @property
    def is_inversion_equivalent(self):
        """
        Is true when set-class is inversion-equivalent.

        ..  container:: example

            Is inversion-equivalent:

            >>> set_class = abjad.SetClass(4, 29)
            >>> print(set_class)
            SC(4-29){0, 1, 3, 7}

            >>> pitch_class_set = set_class.prime_form
            >>> inverted_pitch_class_set = pitch_class_set.invert()
            >>> inverted_set_class = abjad.SetClass.from_pitch_class_set(
            ...     inverted_pitch_class_set
            ... )
            >>> print(inverted_set_class)
            SC(4-29){0, 1, 3, 7}

            >>> set_class.is_inversion_equivalent
            True

        ..  container:: example

            Is inversion-equivalent:

            >>> set_class = abjad.SetClass(
            ...     4, 29,
            ...     lex_rank=True,
            ... )
            >>> print(set_class)
            SC(4-29){0, 3, 6, 9}

            >>> pitch_class_set = set_class.prime_form
            >>> inverted_pitch_class_set = pitch_class_set.invert()
            >>> inverted_set_class = abjad.SetClass.from_pitch_class_set(
            ...     inverted_pitch_class_set,
            ...     lex_rank=True,
            ... )
            >>> print(inverted_set_class)
            SC(4-29){0, 3, 6, 9}

            >>> set_class.is_inversion_equivalent
            True

        ..  container:: example

            Is not inversion-equivalent:

            >>> set_class = abjad.SetClass(
            ...     4, 29,
            ...     transposition_only=True,
            ... )
            >>> print(set_class)
            SC(4-29){0, 2, 6, 7}

            >>> pitch_class_set = set_class.prime_form
            >>> inverted_pitch_class_set = pitch_class_set.invert()
            >>> inverted_set_class = abjad.SetClass.from_pitch_class_set(
            ...     inverted_pitch_class_set,
            ...     transposition_only=True,
            ... )
            >>> print(inverted_set_class)
            SC(4-15){0, 1, 5, 7}

            >>> set_class.is_inversion_equivalent
            False

        Returns true or false.
        """
        prime_form = self.prime_form
        inverted_pitch_class_set = prime_form.invert()
        inverted_set_class = type(self).from_pitch_class_set(
            inverted_pitch_class_set,
            lex_rank=self.lex_rank,
            transposition_only=self.transposition_only,
        )
        return self == inverted_set_class

    @property
    def lex_rank(self):
        """
        Is true when set-class uses lex rank.

        ..  container:: example

            Uses Forte rank:

            >>> set_class = abjad.SetClass(4, 29)
            >>> set_class
            SetClass(cardinality=4, rank=29)

            >>> print(set_class)
            SC(4-29){0, 1, 3, 7}

        ..  container:: example

            Uses lex rank:

            >>> set_class = abjad.SetClass(
            ...     4, 29,
            ...     lex_rank=True,
            ... )
            >>> set_class
            SetClass(cardinality=4, rank=29, lex_rank=True)

            >>> print(set_class)
            SC(4-29){0, 3, 6, 9}

        ..  container:: example

            SG1 set-classes always use lex rank:

            >>> set_class = abjad.SetClass(
            ...     4, 29,
            ...     transposition_only=True,
            ... )
            >>> set_class
            SetClass(cardinality=4, rank=29, transposition_only=True)

            >>> print(set_class)
            SC(4-29){0, 2, 6, 7}

        Set to true, false or none.

        Defaults to none.

        Returns true, false or none.
        """
        return self._lex_rank

    @property
    def prime_form(self):
        """
        Gets prime form.

        ..  container:: example

            Gets prime form of SG2 set-class with Forte rank:

            >>> set_class = abjad.SetClass(4, 29)
            >>> print(set_class)
            SC(4-29){0, 1, 3, 7}

            >>> set_class.prime_form
            PitchClassSet([0, 1, 3, 7])

        ..  container:: example

            Gets prime form of SG2 set-class with lex rank:

            >>> set_class = abjad.SetClass(
            ...     4, 29,
            ...     lex_rank=True,
            ... )
            >>> print(set_class)
            SC(4-29){0, 3, 6, 9}

            >>> set_class.prime_form
            PitchClassSet([0, 3, 6, 9])

        ..  container:: example

            Gets prime form of SG1 set-class:

            >>> set_class = abjad.SetClass(
            ...     4, 29,
            ...     transposition_only=True,
            ... )
            >>> print(set_class)
            SC(4-29){0, 2, 6, 7}

            >>> set_class.prime_form
            PitchClassSet([0, 2, 6, 7])

        Returns numbered pitch-class set.
        """
        return self._prime_form

    @property
    def rank(self):
        """
        Gets rank.

        ..  container:: example

            Gets rank of SG2 set-class with Forte rank:

            >>> set_class = abjad.SetClass(4, 29)
            >>> print(set_class)
            SC(4-29){0, 1, 3, 7}

            >>> set_class.rank
            29

        ..  container:: example

            Gets rank of SG2 set-class with lex rank:

            >>> set_class = abjad.SetClass(
            ...     4, 29,
            ...     lex_rank=True,
            ... )
            >>> print(set_class)
            SC(4-29){0, 3, 6, 9}

            >>> set_class.rank
            29

        ..  container:: example

            Gets rank of SG1 set-class:

            >>> set_class = abjad.SetClass(
            ...     4, 29,
            ...     transposition_only=True,
            ... )
            >>> print(set_class)
            SC(4-29){0, 2, 6, 7}

            >>> set_class.rank
            29

        Set to positive integer.

        Returns positive integer.
        """
        return self._rank

    @property
    def transposition_only(self):
        """
        Is true when set-class collects pitch-class sets related only by
        transposition.

        ..  container:: example

            Initializes SG2 set-class with Forte rank:

            >>> set_class = abjad.SetClass(4, 29)
            >>> print(set_class)
            SC(4-29){0, 1, 3, 7}

        ..  container:: example

            Initializes SG2 set-class with lex rank:

            >>> set_class = abjad.SetClass(
            ...     4, 29,
            ...     lex_rank=True,
            ... )
            >>> print(set_class)
            SC(4-29){0, 3, 6, 9}

        ..  container:: example

            Initializes SG1 set-class:

            >>> set_class = abjad.SetClass(
            ...     4, 29,
            ...     transposition_only=True,
            ... )
            >>> print(set_class)
            SC(4-29){0, 2, 6, 7}

        Set to true, false or none.

        Defaults to none.

        Returns true, false or none.
        """
        return self._transposition_only

    ### PUBLIC METHODS ###

    # TODO: change to from_selection()
    @staticmethod
    def from_pitch_class_set(pitch_class_set, lex_rank=None, transposition_only=None):
        """
        Makes set-class from ``pitch_class_set``.

        ..  container:: example

            >>> pc_set = abjad.PitchClassSet([9, 0, 3, 5, 6])
            >>> set_class = abjad.SetClass.from_pitch_class_set(pc_set)
            >>> print(set_class)
            SC(5-31){0, 1, 3, 6, 9}

            >>> pc_set = abjad.PitchClassSet([9, 0, 3, 5, 6])
            >>> set_class = abjad.SetClass.from_pitch_class_set(
            ...     pc_set,
            ...     lex_rank=True,
            ... )
            >>> print(set_class)
            SC(5-22){0, 1, 3, 6, 9}

            >>> pc_set = abjad.PitchClassSet([9, 0, 3, 5, 6])
            >>> set_class = abjad.SetClass.from_pitch_class_set(
            ...     pc_set,
            ...     transposition_only=True,
            ... )
            >>> print(set_class)
            SC(5-44){0, 2, 3, 6, 9}

        ..  container:: example

            >>> pc_set = abjad.PitchClassSet([9, 11, 1, 2, 4, 6])
            >>> set_class = abjad.SetClass.from_pitch_class_set(pc_set)
            >>> print(set_class)
            SC(6-32){0, 2, 4, 5, 7, 9}

            >>> pc_set = abjad.PitchClassSet([9, 11, 1, 2, 4, 6])
            >>> set_class = abjad.SetClass.from_pitch_class_set(
            ...     pc_set,
            ...     lex_rank=True,
            ... )
            >>> print(set_class)
            SC(6-49){0, 2, 4, 5, 7, 9}

            >>> pc_set = abjad.PitchClassSet([9, 11, 1, 2, 4, 6])
            >>> set_class = abjad.SetClass.from_pitch_class_set(
            ...     pc_set,
            ...     transposition_only=True,
            ... )
            >>> print(set_class)
            SC(6-70){0, 2, 4, 5, 7, 9}

        ..  container:: example

            >>> pc_set = abjad.PitchClassSet([11, 0, 5, 6])
            >>> set_class = abjad.SetClass.from_pitch_class_set(pc_set)
            >>> print(set_class)
            SC(4-9){0, 1, 6, 7}

            >>> pc_set = abjad.PitchClassSet([11, 0, 5, 6])
            >>> set_class = abjad.SetClass.from_pitch_class_set(
            ...     pc_set,
            ...     lex_rank=True,
            ... )
            >>> print(set_class)
            SC(4-17){0, 1, 6, 7}

            >>> pc_set = abjad.PitchClassSet([11, 0, 5, 6])
            >>> set_class = abjad.SetClass.from_pitch_class_set(
            ...     pc_set,
            ...     transposition_only=True,
            ... )
            >>> print(set_class)
            SC(4-17){0, 1, 6, 7}

        ..  container:: example

            >>> pc_set = abjad.PitchClassSet([0, 4, 7])
            >>> set_class = abjad.SetClass.from_pitch_class_set(pc_set)
            >>> print(set_class)
            SC(3-11){0, 3, 7}

            >>> pc_set = abjad.PitchClassSet([0, 4, 7])
            >>> set_class = abjad.SetClass.from_pitch_class_set(
            ...     pc_set,
            ...     lex_rank=True,
            ... )
            >>> print(set_class)
            SC(3-11){0, 3, 7}

            >>> pc_set = abjad.PitchClassSet([0, 4, 7])
            >>> set_class = abjad.SetClass.from_pitch_class_set(
            ...     pc_set,
            ...     transposition_only=True,
            ... )
            >>> print(set_class)
            SC(3-17){0, 4, 7}

        Returns set-class.
        """
        pitch_class_set = PitchClassSet(
            items=pitch_class_set, item_class=NumberedPitchClass
        )
        prime_form = pitch_class_set.get_prime_form(
            transposition_only=transposition_only
        )
        prime_form = tuple([_.number for _ in sorted(prime_form)])
        if transposition_only:
            pair = SetClass._prime_form_to_transposition_only_identifier[prime_form]
        elif lex_rank:
            pair = SetClass._prime_form_to_lex_identifier[prime_form]
        else:
            pair = SetClass._prime_form_to_forte_identifier[prime_form]
        cardinality, rank = pair
        set_class = SetClass(
            cardinality=cardinality,
            rank=rank,
            lex_rank=lex_rank,
            transposition_only=transposition_only,
        )
        return set_class

    @staticmethod
    def list_set_classes(cardinality=None, lex_rank=None, transposition_only=None):
        """
        List set-classes.

        ..  container:: example

            Lists SG2 set-classes of cardinality 4 with Forte rank:

            >>> set_classes = abjad.SetClass.list_set_classes(
            ...     cardinality=4,
            ... )
            >>> for set_class in set_classes:
            ...     print(set_class)
            SC(4-1){0, 1, 2, 3}
            SC(4-2){0, 1, 2, 4}
            SC(4-3){0, 1, 3, 4}
            SC(4-4){0, 1, 2, 5}
            SC(4-5){0, 1, 2, 6}
            SC(4-6){0, 1, 2, 7}
            SC(4-7){0, 1, 4, 5}
            SC(4-8){0, 1, 5, 6}
            SC(4-9){0, 1, 6, 7}
            SC(4-10){0, 2, 3, 5}
            SC(4-11){0, 1, 3, 5}
            SC(4-12){0, 2, 3, 6}
            SC(4-13){0, 1, 3, 6}
            SC(4-14){0, 2, 3, 7}
            SC(4-15){0, 1, 4, 6}
            SC(4-16){0, 1, 5, 7}
            SC(4-17){0, 3, 4, 7}
            SC(4-18){0, 1, 4, 7}
            SC(4-19){0, 1, 4, 8}
            SC(4-20){0, 1, 5, 8}
            SC(4-21){0, 2, 4, 6}
            SC(4-22){0, 2, 4, 7}
            SC(4-23){0, 2, 5, 7}
            SC(4-24){0, 2, 4, 8}
            SC(4-25){0, 2, 6, 8}
            SC(4-26){0, 3, 5, 8}
            SC(4-27){0, 2, 5, 8}
            SC(4-28){0, 3, 6, 9}
            SC(4-29){0, 1, 3, 7}

        ..  container:: example

            Lists SG2 set-classes of cardinality 4 with lex rank:

            >>> set_classes = abjad.SetClass.list_set_classes(
            ...     cardinality=4,
            ...     lex_rank=True,
            ... )
            >>> for set_class in set_classes:
            ...     print(set_class)
            SC(4-1){0, 1, 2, 3}
            SC(4-2){0, 1, 2, 4}
            SC(4-3){0, 1, 2, 5}
            SC(4-4){0, 1, 2, 6}
            SC(4-5){0, 1, 2, 7}
            SC(4-6){0, 1, 3, 4}
            SC(4-7){0, 1, 3, 5}
            SC(4-8){0, 1, 3, 6}
            SC(4-9){0, 1, 3, 7}
            SC(4-10){0, 1, 4, 5}
            SC(4-11){0, 1, 4, 6}
            SC(4-12){0, 1, 4, 7}
            SC(4-13){0, 1, 4, 8}
            SC(4-14){0, 1, 5, 6}
            SC(4-15){0, 1, 5, 7}
            SC(4-16){0, 1, 5, 8}
            SC(4-17){0, 1, 6, 7}
            SC(4-18){0, 2, 3, 5}
            SC(4-19){0, 2, 3, 6}
            SC(4-20){0, 2, 3, 7}
            SC(4-21){0, 2, 4, 6}
            SC(4-22){0, 2, 4, 7}
            SC(4-23){0, 2, 4, 8}
            SC(4-24){0, 2, 5, 7}
            SC(4-25){0, 2, 5, 8}
            SC(4-26){0, 2, 6, 8}
            SC(4-27){0, 3, 4, 7}
            SC(4-28){0, 3, 5, 8}
            SC(4-29){0, 3, 6, 9}

        ..  container:: example

            Lists SG1 set-classes of cardinality 4:

            >>> set_classes = abjad.SetClass.list_set_classes(
            ...     cardinality=4,
            ...     transposition_only=True,
            ... )
            >>> for set_class in set_classes:
            ...     print(set_class)
            SC(4-1){0, 1, 2, 3}
            SC(4-2){0, 1, 2, 4}
            SC(4-3){0, 1, 2, 5}
            SC(4-4){0, 1, 2, 6}
            SC(4-5){0, 1, 2, 7}
            SC(4-6){0, 1, 3, 4}
            SC(4-7){0, 1, 3, 5}
            SC(4-8){0, 1, 3, 6}
            SC(4-9){0, 1, 3, 7}
            SC(4-10){0, 1, 4, 5}
            SC(4-11){0, 1, 4, 6}
            SC(4-12){0, 1, 4, 7}
            SC(4-13){0, 1, 4, 8}
            SC(4-14){0, 1, 5, 6}
            SC(4-15){0, 1, 5, 7}
            SC(4-16){0, 1, 5, 8}
            SC(4-17){0, 1, 6, 7}
            SC(4-18){0, 2, 3, 4}
            SC(4-19){0, 2, 3, 5}
            SC(4-20){0, 2, 3, 6}
            SC(4-21){0, 2, 3, 7}
            SC(4-22){0, 2, 4, 5}
            SC(4-23){0, 2, 4, 6}
            SC(4-24){0, 2, 4, 7}
            SC(4-25){0, 2, 4, 8}
            SC(4-26){0, 2, 5, 6}
            SC(4-27){0, 2, 5, 7}
            SC(4-28){0, 2, 5, 8}
            SC(4-29){0, 2, 6, 7}
            SC(4-30){0, 2, 6, 8}
            SC(4-31){0, 3, 4, 5}
            SC(4-32){0, 3, 4, 6}
            SC(4-33){0, 3, 4, 7}
            SC(4-34){0, 3, 4, 8}
            SC(4-35){0, 3, 5, 6}
            SC(4-36){0, 3, 5, 7}
            SC(4-37){0, 3, 5, 8}
            SC(4-38){0, 3, 6, 7}
            SC(4-39){0, 3, 6, 8}
            SC(4-40){0, 3, 6, 9}
            SC(4-41){0, 4, 5, 6}
            SC(4-42){0, 4, 5, 7}
            SC(4-43){0, 4, 6, 7}

        Returns list of set-classes.
        """
        if transposition_only:
            identifiers = SetClass._transposition_only_identifier_to_prime_form
        elif lex_rank:
            identifiers = SetClass._lex_identifier_to_prime_form
        else:
            identifiers = SetClass._forte_identifier_to_prime_form
        identifiers = list(identifiers)
        if cardinality is not None:
            identifiers = [_ for _ in identifiers if _[0] == cardinality]
        set_classes = []
        for identifier in sorted(identifiers):
            cardinality, rank = identifier
            set_class = SetClass(
                cardinality,
                rank,
                lex_rank=lex_rank,
                transposition_only=transposition_only,
            )
            set_classes.append(set_class)
        return set_classes


def _classify_set_classes(transposition_only=False):
    """
    Was only necessary to run during implementation of SetClass.

    Generated the ...

        _forte_identifier_to_prime_form
        _lex_identifier_to_prime_form
        _transposition_only_identifier_to_prime_form

    ... dictionaries attached as class attributes.

    Archived here in case other identifier systems are needed in future.
    """
    all_prime_forms = {}
    for cardinality in range(12 + 1):
        all_prime_forms[cardinality] = set()
    for pc_set in _yield_all_pitch_class_sets():
        if NumberedPitchClass(0) not in pc_set:
            if 0 < len(pc_set):
                continue
        prime_form = pc_set.get_prime_form(transposition_only=transposition_only)
        all_prime_forms[prime_form.cardinality].add(prime_form)
    total = 0
    for cardinality in range(12 + 1):
        count = len(all_prime_forms[cardinality])
        total += count
    for cardinality in range(12 + 1):
        prime_forms = list(all_prime_forms[cardinality])
        prime_forms.sort(key=lambda x: str(x))
        for index, prime_form in enumerate(prime_forms):
            rank = index + 1
            prime_form = str(prime_form)
            prime_form = prime_form.replace("{", "(")
            prime_form = prime_form.replace("}", ")")
            message = f"({cardinality}, {rank}): {prime_form},"
            print(message)
        print()
    message = f"total set-classes: {total}"
    print(message)
    print()


def _yield_all_pitch_class_sets():
    def _helper(binary_string):
        result = zip(binary_string, range(len(binary_string)))
        result = [string[1] for string in result if string[0] == "1"]
        return result

    for i in range(4096):
        string = _math.integer_to_binary_string(i).zfill(12)
        subset = "".join(list(reversed(string)))
        subset = _helper(subset)
        subset = PitchClassSet(subset, item_class=NumberedPitchClass)
        yield subset


@functools.total_ordering
class IntervalClass:
    """
    Abstract interval-class.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    _is_abstract = True

    ### INITIALIZER ###

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

    ### SPECIAL METHODS ###

    def __abs__(self):
        """
        Gets absolute value of interval-class.

        Returns new interval-class.
        """
        return type(self)(abs(self._number))

    def __add__(self, argument):
        """
        Adds ``argument`` to interval-class.

        Returns new interval-class.
        """
        raise NotImplementedError

    def __eq__(self, argument) -> bool:
        """
        Delegates to ``abjad.format.compare_objects()``.
        """
        return _format.compare_objects(self, argument)

    def __float__(self):
        """
        Coerce to semitones as float.

        Returns float.
        """
        raise NotImplementedError

    def __hash__(self) -> int:
        """
        Hashes interval-class.
        """
        return hash(self.__class__.__name__ + str(self))

    def __lt__(self, argument):
        """
        Is true when interval-class is less than ``argument``

        Returns true or false.
        """
        raise NotImplementedError

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return _format.get_repr(self)

    def __str__(self):
        """
        Gets string representation of interval-class.

        Returns string.
        """
        return str(self.number)

    def __sub__(self, argument):
        """
        Subtracts ``argument`` from interval-class.

        Returns new interval-class.
        """
        raise NotImplementedError

    ### PRIVATE METHODS ###

    @classmethod
    def _named_to_numbered(cls, direction, quality, diatonic_number):
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

    ### PUBLIC PROPERTIES ###

    @property
    def number(self):
        """
        Gets number of interval-class.

        Returns number.
        """
        return self._number

    ### PUBLIC METHODS ###

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

    ### CLASS VARIABLES ###

    __slots__ = ("_number", "_quality")

    ### INITIALIZER ###

    def __init__(self, name="P1"):
        super().__init__(name or "P1")

    ### SPECIAL METHODS ###

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

    def __lt__(self, argument):
        """
        Is true when ``argument`` is a named interval class with a number
        greater than that of this named interval.

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

        Returns true or false.
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

    ### PRIVATE PROPERTIES ###

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

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        values = [self.name]
        return _format.FormatSpecification(
            coerce_for_equality=True,
            storage_format_is_not_indented=True,
            storage_format_args_values=values,
        )

    ### PUBLIC PROPERTIES ###

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

    ### PUBLIC METHODS ###

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

        >>> interval_class = abjad.NamedInversionEquivalentIntervalClass(
        ...     'P1',
        ...     )
        >>> abjad.NamedInversionEquivalentIntervalClass(interval_class)
        NamedInversionEquivalentIntervalClass('P1')

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, name="P1"):
        super().__init__(name or "P1")
        self._quality, self._number = self._process_quality_and_number(
            self._quality, self._number
        )

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        """
        Is true when ``argument`` is a named inversion-equivalent
        interval-class with name equal to that of this named
        inversion-equivalent interval-class.

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

    ### PRIVATE METHODS ###

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

    ### PUBLIC METHODS ###

    @classmethod
    def from_pitch_carriers(class_, pitch_carrier_1, pitch_carrier_2):
        """
        Makes named inversion-equivalent interval-class from
        ``pitch_carrier_1`` and ``pitch_carrier_2``

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

    ### CLASS VARIABLES ###

    __slots__ = ("_number",)

    ### INITIALIZER ###

    def __init__(self, number=0):
        super().__init__(number or 0)

    ### SPECIAL METHODS ###

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

    def __eq__(self, argument):
        """
        Is true when ``argument`` is a numbered interval-class with number
        equal to that of this numbered interval-class.

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

        Returns true or false.
        """
        return super().__eq__(argument)

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
        Is true when numbered interval-class is less than ``argument``

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

    ### PRIVATE METHODS ###

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

    def _get_format_specification(self):
        return _format.FormatSpecification(
            coerce_for_equality=True,
            storage_format_is_not_indented=True,
            storage_format_args_values=[self.number],
        )

    ### PUBLIC PROPERTIES ###

    @property
    def direction_number(self):
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

    ### PUBLIC METHODS ###

    @classmethod
    def from_pitch_carriers(class_, pitch_carrier_1, pitch_carrier_2):
        """Makes numbered interval-class from ``pitch_carrier_1`` and
        ``pitch_carrier_2``

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

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, number=0):
        super().__init__(number or 0)
        self._number %= 12
        if 6 < self._number:
            self._number = 12 - self._number

    ### SPECIAL METHODS ###

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
        Is true when ``argument`` is a numbered inversion-equivalent
        interval-class with a number less than this numbered
        inversion-equivalent interval-class.
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


# NOTE: mypy 0.770 errors on functools combined with abstract class
@functools.total_ordering
class Interval:
    """
    Abstract interval.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_interval_class", "_octaves")

    _is_abstract = True

    ### INITIALIZER ###

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

    ### SPECIAL METHODS ###

    def __abs__(self):
        """
        Gets absolute value of interval.

        Returns new interval.
        """
        raise NotImplementedError

    def __eq__(self, argument) -> bool:
        """
        Delegates to ``abjad.format.compare_objects()``.
        """
        return _format.compare_objects(self, argument)

    def __float__(self):
        """
        Coerce to semitones as float.

        Returns float.
        """
        raise NotImplementedError

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

    def __neg__(self):
        """
        Negates interval.

        Returns interval.
        """
        raise NotImplementedError

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return _format.get_repr(self)

    def __str__(self):
        """
        Gets string representation of interval.

        Returns string.
        """
        return str(self.number)

    ### PRIVATE METHODS ###

    def _from_interval_or_interval_class(self, argument):
        raise NotImplementedError

    def _from_named_parts(self, direction, quality, diatonic_number):
        raise NotImplementedError

    def _from_number(self, argument):
        raise NotImplementedError

    @classmethod
    def _named_to_numbered(cls, direction, quality, diatonic_number):
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

    ### PUBLIC PROPERTIES ###

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

    ### PUBLIC METHODS ###

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

    ### CLASS VARIABLES ##

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, name="P1"):
        super().__init__(name or "P1")

    ### SPECIAL METHODS ###

    def __abs__(self):
        """
        Gets absolute value of named interval.

        ..  container:: example

            >>> abs(abjad.NamedInterval('+M9'))
            NamedInterval('+M9')

            >>> abs(abjad.NamedInterval('-M9'))
            NamedInterval('+M9')

        Returns named interval.
        """
        return type(self)((self.quality, abs(self.number)))

    def __add__(self, argument):
        """
        Adds ``argument`` to named interval.

        ..  container:: example

            >>> abjad.NamedInterval('M9') + abjad.NamedInterval('M2')
            NamedInterval('+M10')

        Returns new named interval.
        """
        try:
            argument = type(self)(argument)
        except Exception:
            return NotImplemented
        dummy_pitch = NamedPitch(0)
        new_pitch = dummy_pitch + self + argument
        return NamedInterval.from_pitch_carriers(dummy_pitch, new_pitch)

    def __copy__(self, *arguments):
        """
        Copies named interval.

        >>> import copy

        ..  container:: example

            >>> copy.copy(abjad.NamedInterval('+M9'))
            NamedInterval('+M9')

        Returns new named interval.
        """
        return type(self)((self.quality, self.number))

    def __eq__(self, argument):
        """
        Is true when named interval equal ``argument``

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
        return super().__eq__(argument)

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

    def __lt__(self, argument):
        """
        Is true when ``argument`` is a named interval with a number greater
        than that of this named interval.

        ..  container:: example

            >>> abjad.NamedInterval('+M9') < abjad.NamedInterval('+M10')
            True

        ..  container:: example

            Also true when ``argument`` is a named interval with a
            number equal to this named interval and with semitones greater than
            this named interval:

            >>> abjad.NamedInterval('+m9') < abjad.NamedInterval('+M9')
            True

        ..  container:: example

            Otherwise false:

            >>> abjad.NamedInterval('+M9') < abjad.NamedInterval('+M2')
            False

        Returns true or false.
        """
        if isinstance(argument, type(self)):
            if self.number == argument.number:
                return self.semitones < argument.semitones
            return self.number < argument.number
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

    def __neg__(self):
        """
        Negates named interval.

        ..  container:: example

            >>> -abjad.NamedInterval('+M9')
            NamedInterval('-M9')

        ..  container:: example

            >>> -abjad.NamedInterval('-M9')
            NamedInterval('+M9')

        Returns new named interval.
        """
        return type(self)((self.quality, -self.number))

    def __radd__(self, argument):
        """
        Adds named interval to ``argument``

        ..  container:: example

            >>> abjad.NamedInterval('M9') + abjad.NamedInterval('M2')
            NamedInterval('+M10')

        Returns new named interval.
        """
        try:
            argument = type(self)(argument)
        except Exception:
            return NotImplemented
        return argument.__add__(self)

    def __rmul__(self, argument):
        """
        Multiplies ``argument`` by named interval.

        ..  container:: example

            >>> abjad.NamedInterval('+M9') * 3
            NamedInterval('+A25')

        Returns new named interval.
        """
        return self * argument

    def __str__(self):
        """
        Gets string representation of named interval.

        ..  container:: example

            >>> str(abjad.NamedInterval('+M9'))
            '+M9'

        Returns string.
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

    ### PRIVATE METHODS ###

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

    def _get_format_specification(self):
        values = [self.name]
        return _format.FormatSpecification(
            coerce_for_equality=True,
            storage_format_is_not_indented=True,
            storage_format_args_values=values,
        )

    ### PUBLIC PROPERTIES ###

    @property
    def direction_number(self):
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

        Returns ``-1``, ``0`` or ``1``.
        """
        if self.quality == "P" and abs(self.number) == 1:
            return 0
        return _math.sign(self.number)

    @property
    def interval_class(self):
        """
        Gets interval class of named interval.

        ..  container:: example

            >>> abjad.NamedInterval('+M9').interval_class
            NamedIntervalClass('+M2')

            >>> abjad.NamedInterval('-M9').interval_class
            NamedIntervalClass('-M2')

            >>> abjad.NamedInterval('P1').interval_class
            NamedIntervalClass('P1')

            >>> abjad.NamedInterval('+P8').interval_class
            NamedIntervalClass('+P8')

        Returns named interval-class.
        """
        return self._interval_class

    @property
    def name(self):
        """
        Gets name of named interval.

        ..  container:: example

            >>> abjad.NamedInterval('+M9').name
            '+M9'

        Returns string.
        """
        direction_symbol = _direction_number_to_direction_symbol[self.direction_number]
        return "{}{}{}".format(
            direction_symbol, self._interval_class.quality, abs(self.number)
        )

    @property
    def number(self):
        """
        Gets number of named interval.

        ..  container:: example

            >>> abjad.NamedInterval('+M9').number
            9

        Returns nonnegative number.
        """
        number = self._interval_class._number
        direction = _math.sign(number)
        number = abs(number) + (7 * self.octaves)
        return number * direction

    @property
    def octaves(self):
        """
        Gets octaves of interval.

        Returns nonnegative number.
        """
        return self._octaves

    @property
    def quality(self):
        """
        Gets quality of named interval.

        Returns string.
        """
        return self._interval_class.quality

    @property
    def semitones(self):
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

        Returns number.
        """
        direction = self.direction_number
        diatonic_number = abs(self._interval_class._number)
        quality = self._validate_quality_and_diatonic_number(
            self.quality, diatonic_number
        )
        diatonic_number += 7 * self._octaves
        return self._named_to_numbered(direction, quality, diatonic_number)

    @property
    def staff_spaces(self):
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

        Returns nonnegative integer.
        """
        if self.direction_number == -1:
            return self.number + 1
        elif not self.direction_number:
            return 0
        elif self.direction_number == 1:
            return self.number - 1

    ### PUBLIC METHODS ###

    @classmethod
    def from_pitch_carriers(
        class_, pitch_carrier_1, pitch_carrier_2
    ) -> "NamedInterval":
        """
        Makes named interval calculated from ``pitch_carrier_1`` to
        ``pitch_carrier_2``

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

    ..  container:: example

        Initializes from other numbered interval

        >>> abjad.NumberedInterval(abjad.NumberedInterval(-14))
        NumberedInterval(-14)

    ..  container:: example

        Initializes from named interval:

        >>> abjad.NumberedInterval(abjad.NamedInterval('-P4'))
        NumberedInterval(-5)

    ..  container:: example

        Initializes from interval string:

        >>> abjad.NumberedInterval('-P4')
        NumberedInterval(-5)

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, number=0):
        super().__init__(number or 0)

    ### SPECIAL METHODS ###

    def __abs__(self):
        """
        Absolute value of numbered interval.

        ..  container:: example

            >>> abs(abjad.NumberedInterval(-14))
            NumberedInterval(14)

        Returns new numbered interval.
        """
        return type(self)(abs(self.number))

    def __add__(self, argument):
        """
        Adds ``argument`` to numbered interval.

        ..  container:: example

            >>> abjad.NumberedInterval(3) + abjad.NumberedInterval(14)
            NumberedInterval(17)

            >>> abjad.NumberedInterval(3) + abjad.NumberedInterval(-14)
            NumberedInterval(-11)

        Returns new numbered interval.
        """
        try:
            argument = type(self)(argument)
        except Exception:
            return NotImplemented
        return type(self)(float(self) + float(argument))

    def __copy__(self):
        """
        Copies numbered interval.

        >>> import copy

        ..  container:: example

            >>> copy.copy(abjad.NumberedInterval(-14))
            NumberedInterval(-14)

        Returns new numbered interval.
        """
        return type(self)(self.number)

    def __eq__(self, argument):
        """
        Is true when ``argument`` is a numbered interval with number equal to that of
        this numbered interval.

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

        Returns true or false.
        """
        return super().__eq__(argument)

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

    def __lt__(self, argument):
        """
        Is true when ``argument`` is a numbered interval with same direction
        number as this numbered interval and with number greater than that of
        this numbered interval.

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
        if not isinstance(argument, type(self)):
            raise TypeError(f"must be numbered interval: {argument!r}.")
        if not self.direction_number == argument.direction_number:
            raise ValueError("can only compare intervals of same direction.")
        return abs(self.number) < abs(argument.number)

    def __neg__(self):
        """
        Negates numbered interval.

        ..  container:: example

            >>> -abjad.NumberedInterval(-14)
            NumberedInterval(14)

        Returns new numbered interval.
        """
        return type(self)(-self.number)

    def __radd__(self, argument):
        """
        Adds numbered interval to ``argument``

        ..  container:: example

            >>> interval = abjad.NumberedInterval(14)
            >>> abjad.NumberedInterval(3).__radd__(interval)
            NumberedInterval(17)

            >>> interval = abjad.NumberedInterval(-14)
            >>> abjad.NumberedInterval(3).__radd__(interval)
            NumberedInterval(-11)

        Returns new numbered interval.
        """
        try:
            argument = type(self)(argument)
        except Exception:
            return NotImplemented
        return type(self)(float(self) + float(argument))

    def __str__(self):
        """
        String representation of numbered interval.

        Returns string.
        """
        direction_symbol = _direction_number_to_direction_symbol[
            _math.sign(self.number)
        ]
        return f"{direction_symbol}{abs(self.number)}"

    def __sub__(self, argument):
        """
        Subtracts ``argument`` from numbered interval.

        Returns new numbered interval.
        """
        try:
            argument = type(self)(argument)
        except Exception:
            return NotImplemented
        return type(self)(float(self) - float(argument))

    ### PRIVATE METHODS ###

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

    def _get_format_specification(self):
        values = [self.number]
        return _format.FormatSpecification(
            coerce_for_equality=True,
            storage_format_is_not_indented=True,
            storage_format_args_values=values,
        )

    ### PUBLIC PROPERTIES ###

    @property
    def direction_number(self):
        """
        Gets direction number of numbered interval.

        ..  container:: example

            >>> abjad.NumberedInterval(-14).direction_number
            -1

            >>> abjad.NumberedInterval(0).direction_number
            0

            >>> abjad.NumberedInterval(6).direction_number
            1

        Returns integer.
        """ ""
        return _math.sign(self.number)

    @property
    def interval_class(self):
        """
        Gets interval class of numbered interval.

        Returns numbered interval-class.
        """
        return self._interval_class

    @property
    def number(self):
        """
        Gets number of numbered interval.

        ..  container:: example

            >>> abjad.NumberedInterval(-14).number
            -14

            >>> abjad.NumberedInterval(-2).number
            -2

            >>> abjad.NumberedInterval(0).number
            0

        Returns number.
        """
        number = self._interval_class._number
        direction = _math.sign(number)
        number = abs(number) + (12 * self.octaves)
        return number * direction

    @property
    def octaves(self):
        """
        Gets octaves of interval.

        Returns nonnegative number.
        """
        return self._octaves

    @property
    def semitones(self):
        """
        Gets semitones corresponding to numbered interval.

        ..  container:: example

            >>> abjad.NumberedInterval(-14).semitones
            -14

        Returns nonnegative number.
        """
        return self.number

    ### PUBLIC METHODS ###

    @classmethod
    def from_pitch_carriers(
        class_, pitch_carrier_1, pitch_carrier_2
    ) -> "NumberedInterval":
        """Makes numbered interval from ``pitch_carrier_1`` and
        ``pitch_carrier_2``

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


class CompoundOperator:
    """
    Compound operator.

    ..  container:: example

        Rotation followed by transposition:

        >>> operator = abjad.CompoundOperator()
        >>> operator = operator.rotate(n=1)
        >>> operator = operator.transpose(n=2)

        >>> str(operator)
        'T2r1'

        >>> pitch_classes = abjad.PitchClassSegment([0, 1, 4, 7])
        >>> operator(pitch_classes)
        PitchClassSegment([9, 2, 3, 6])

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_operators", "_show_identity_operators")

    ### INITIALIZER ###

    def __init__(self, operators=None, *, show_identity_operators=None):
        if operators is not None:
            if not isinstance(operators, collections.abc.Sequence):
                operators = (operators,)
            assert len(operators)
            operators = tuple(operators)
        self._operators = operators
        assert isinstance(show_identity_operators, (bool, type(None)))
        self._show_identity_operators = show_identity_operators

    ### SPECIAL METHODS ###

    def __add__(self, operator):
        """
        Composes compound operator and ``operator``.

        ..  container:: example

            >>> operator = abjad.CompoundOperator()
            >>> operator = operator.transpose(n=1)
            >>> operator = operator.multiply(n=5)
            >>> str(operator)
            'M5T1'

        ..  container:: example

            >>> inversion = abjad.Inversion()
            >>> retrograde = abjad.Retrograde()
            >>> transposition = abjad.Transposition(n=1)

            >>> operator_1 = inversion + retrograde
            >>> str(operator_1)
            'IR'

            >>> operator_2 = inversion + transposition
            >>> str(operator_2)
            'IT1'

            >>> operator_3 = operator_1 + operator_2
            >>> str(operator_3)
            'IRIT1'

            >>> string = abjad.storage(operator_3)
            >>> print(string)
            abjad.CompoundOperator(
                operators=[
                    Transposition(n=1),
                    Inversion(),
                    Retrograde(),
                    Inversion(),
                    ],
                )

        Returns new compound operator.
        """
        operators = list(self.operators)
        if isinstance(operator, type(self)):
            operators[0:0] = operator.operators
        else:
            operators.insert(0, operator)
        result = type(self)()
        for operator in operators:
            result = result._with_operator(operator)
        return result

    def __call__(self, argument):
        """
        Calls compound operator on ``argument``.

        ..  container:: example

            >>> operator = abjad.CompoundOperator()
            >>> operator = operator.rotate(n=1)
            >>> operator = operator.transpose(n=2)
            >>> str(operator)
            'T2r1'

            >>> segment = abjad.PitchClassSegment([0, 1, 4, 7])
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> transform = operator(segment)
            >>> lilypond_file = abjad.illustrate(transform)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> transform
            PitchClassSegment([9, 2, 3, 6])

        Returns new object with type equal to that of ``argument``.
        """
        if self.operators is None:
            return argument
        for transform in self.operators:
            argument = transform(argument)
        return argument

    def __eq__(self, argument) -> bool:
        """
        Delegates to ``abjad.format.compare_objects()``.
        """
        return _format.compare_objects(self, argument)

    def __hash__(self) -> int:
        """
        Hashes compound operator.
        """
        return hash(self.__class__.__name__ + str(self))

    def __radd__(self, operator):
        """
        Composes ``operator`` and compound operator.

        ..  container

            >>> operator = abjad.CompoundOperator()
            >>> operator = operator.transpose(n=1)
            >>> operator = operator.multiply(n=5)
            >>> str(operator)
            'M5T1'

            >>> retrograde = abjad.Retrograde()
            >>> new_operator = retrograde + operator
            >>> str(new_operator)
            'RM5T1'

            >>> new_operator = operator + retrograde
            >>> str(new_operator)
            'M5T1R'

        Returns new compound operator.
        """
        operators = list(self.operators)
        if isinstance(operator, type(self)):
            operators.extend(operator.operators)
        else:
            operators.append(operator)
        result = type(self)()
        for operator in operators:
            result = result._with_operator(operator)
        return result

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return _format.get_repr(self)

    def __str__(self):
        """
        Gets string representation of compound operator.

        ..  container:: example

            Gets string:

            >>> operator = abjad.CompoundOperator()
            >>> operator = operator.rotate(n=1)
            >>> operator = operator.transpose(n=2)

            >>> str(operator)
            'T2r1'

        ..  container:: example

            Gets string of empty operator:

            >>> operator = abjad.CompoundOperator()

            >>> str(operator)
            ''

        Returns string.
        """
        result = []
        operators = self.operators or []
        for operator in reversed(operators):
            if operator._is_identity_operator():
                if self.show_identity_operators:
                    result.append(str(operator))
            else:
                result.append(str(operator))
        result = "".join(result)
        return result

    ### PRIVATE METHODS ###

    @staticmethod
    def _compose_operators(operator_1, operator_2):
        if isinstance(operator_1, CompoundOperator):
            result = operator_1.__add__(operator_2)
        elif isinstance(operator_2, CompoundOperator):
            result = operator_2.__radd__(operator_1)
        else:
            result = CompoundOperator()
            result = result._with_operator(operator_2)
            result = result._with_operator(operator_1)
        return result

    def _with_operator(self, operator):
        operators = self.operators or []
        operators = operators + [operator]
        return type(self)(
            operators, show_identity_operators=self.show_identity_operators
        )

    ### PUBLIC PROPERTIES ###

    @property
    def operators(self):
        """
        Gets operators.

        ..  container:: example

            Gets operators:

            >>> operator = abjad.CompoundOperator()
            >>> operator = operator.rotate(n=1)
            >>> operator = operator.transpose(n=2)

            >>> for operator_ in operator.operators:
            ...     operator_
            ...
            Rotation(n=1)
            Transposition(n=2)

        Returns list of operators.
        """
        if self._operators is not None:
            return list(self._operators)

    @property
    def show_identity_operators(self):
        """
        Is true when string representation of operator should show identity
        operators.

        ..  container:: example

            Does not show identity operators:

            >>> operator = abjad.CompoundOperator()
            >>> operator = operator.transpose(n=0)
            >>> operator = operator.multiply(n=5)

            >>> str(operator)
            'M5'

        ..  container:: example

            Shows identity operators:

            >>> operator = abjad.CompoundOperator(
            ...     show_identity_operators=True,
            ...     )
            >>> operator = operator.transpose(n=0)
            >>> operator = operator.multiply(n=5)

            >>> str(operator)
            'M5T0'

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        """
        return self._show_identity_operators

    ### PUBLIC METHODS ###

    def duplicate(self, counts=None, indices=None, period=None):
        """
        Configures compound operator to duplicate pitches by ``counts``, with
        optional ``indices`` and ``period``.

        ..  container:: example

            >>> operator = abjad.CompoundOperator()
            >>> operator = operator.duplicate(counts=1)
            >>> string = abjad.storage(operator)
            >>> print(string)
            abjad.CompoundOperator(
                operators=[
                    Duplication(counts=1),
                    ],
                )

        Returns new compound operator.
        """
        operator = Duplication(counts=counts, indices=indices, period=period)
        return self._with_operator(operator)

    def invert(self, axis=None):
        """
        Configures compound operator to invert pitches about ``axis``.

        ..  container:: example

            >>> operator = abjad.CompoundOperator()
            >>> operator = operator.invert(axis=2)
            >>> string = abjad.storage(operator)
            >>> print(string)
            abjad.CompoundOperator(
                operators=[
                    Inversion(axis=NamedPitch("d'")),
                    ],
                )

        Returns new compound operator.
        """
        operator = Inversion(axis=axis)
        return self._with_operator(operator)

    def multiply(self, n=1):
        """
        Configures compound operator to multiply pitch-classes by index ``n``.

        ..  container:: example

            >>> operator = abjad.CompoundOperator()
            >>> operator = operator.multiply(n=3)
            >>> string = abjad.storage(operator)
            >>> print(string)
            abjad.CompoundOperator(
                operators=[
                    Multiplication(n=3),
                    ],
                )

        Returns new compound operator.
        """
        operator = Multiplication(n=n)
        return self._with_operator(operator)

    def retrograde(self, period=None):
        """
        Configures compound operator to retrograde pitches.

        ..  container:: example

            >>> operator = abjad.CompoundOperator()
            >>> operator = operator.retrograde()
            >>> string = abjad.storage(operator)
            >>> print(string)
            abjad.CompoundOperator(
                operators=[
                    Retrograde(),
                    ],
                )

        Returns new compound operator.
        """
        operator = Retrograde(period=period)
        return self._with_operator(operator)

    def rotate(self, n=0, period=None):
        """
        Configures compound operator to rotate pitches by index ``n``.

        ..  container:: example

            >>> operator = abjad.CompoundOperator()
            >>> operator = operator.rotate(n=-1)
            >>> string = abjad.storage(operator)
            >>> print(string)
            abjad.CompoundOperator(
                operators=[
                    Rotation(n=-1),
                    ],
                )

        Returns new compound operator.
        """
        operator = Rotation(n=n, period=period)
        return self._with_operator(operator)

    def transpose(self, n=0):
        """
        Configures compound operator to transpose pitches by index ``n``.

        ..  container:: example

            >>> operator = abjad.CompoundOperator()
            >>> operator = operator.transpose(n=1)

            >>> string = abjad.storage(operator)
            >>> print(string)
            abjad.CompoundOperator(
                operators=[
                    Transposition(n=1),
                    ],
                )

        Returns new compound operator.
        """
        operator = Transposition(n=n)
        return self._with_operator(operator)


class Duplication:
    """
    Duplication.

    ..  container:: example:

        >>> operator_ = abjad.Duplication(counts=2, period=4)

        >>> string = abjad.storage(operator_)
        >>> print(string)
        abjad.Duplication(
            counts=2,
            period=4,
            )

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_counts", "_indices", "_period")

    ### INITIALIZER ###

    def __init__(self, *, counts=None, indices=None, period=None):
        if counts is not None:
            if isinstance(counts, collections.abc.Sequence):
                assert len(counts)
                counts = tuple(int(_) for _ in counts)
                assert all(0 <= _ for _ in counts)
            else:
                counts = int(counts)
                assert 0 <= counts
        self._counts = counts
        if indices is not None:
            assert all(isinstance(_, int) for _ in indices), repr(indices)
            indices = tuple(indices)
        self._indices = indices
        if period is not None:
            period = int(period)
            assert 0 < period
        self._period = period

    ### SPECIAL METHODS ###

    def __call__(self, argument):
        """
        Calls rotation on ``argument``.

        ..  container:: example

            Duplicates once without period:

            >>> operator_ = abjad.Duplication(counts=1)
            >>> numbers = [1, 2, 3, 4]
            >>> operator_(numbers)
            [1, 2, 3, 4, 1, 2, 3, 4]

        ..  container:: example

            Duplicates twice without period:

            >>> operator_ = abjad.Duplication(counts=2)
            >>> pitch_classes = abjad.PitchClassSegment([0, 1, 4, 7])
            >>> operator_(pitch_classes)
            PitchClassSegment([0, 1, 4, 7, 0, 1, 4, 7, 0, 1, 4, 7])

        ..  container:: example

            Duplicates periodically:

            >>> operator_ = abjad.Duplication(counts=1, period=3)
            >>> pitches = abjad.PitchSegment("c' d' e' f' g' a' b' c''")
            >>> for pitch in operator_(pitches):
            ...     pitch
            ...
            NamedPitch("c'")
            NamedPitch("d'")
            NamedPitch("e'")
            NamedPitch("c'")
            NamedPitch("d'")
            NamedPitch("e'")
            NamedPitch("f'")
            NamedPitch("g'")
            NamedPitch("a'")
            NamedPitch("f'")
            NamedPitch("g'")
            NamedPitch("a'")
            NamedPitch("b'")
            NamedPitch("c''")
            NamedPitch("b'")
            NamedPitch("c''")

        ..  container:: example

            Duplicate indices:

            >>> operator_ = abjad.Duplication(
            ...     counts=1,
            ...     indices=(0, -1),
            ...     )
            >>> pitch_classes = abjad.PitchClassSegment([0, 1, 4, 7])
            >>> operator_(pitch_classes)
            PitchClassSegment([0, 0, 1, 4, 7, 7])

        ..  container:: example

            Duplicate indices periodically:

            >>> operator_ = abjad.Duplication(
            ...     counts=1,
            ...     indices=(0,),
            ...     period=2,
            ...     )
            >>> pitch_classes = abjad.PitchClassSegment([0, 1, 4, 7, 9])
            >>> operator_(pitch_classes)
            PitchClassSegment([0, 0, 1, 4, 4, 7, 9, 9])

        ..  container:: example

            Duplicate indices periodically with different counts:

            >>> operator_ = abjad.Duplication(
            ...     counts=(1, 2),
            ...     indices=(0,),
            ...     period=2,
            ...     )
            >>> pitch_classes = abjad.PitchClassSegment([0, 1, 4, 7, 9])
            >>> operator_(pitch_classes)
            PitchClassSegment([0, 0, 1, 4, 4, 4, 7, 9, 9])

        ..  container:: example

            Cyclic counts:

            >>> operator_ = abjad.Duplication(counts=(0, 1, 2, 3))
            >>> pitch_classes = abjad.PitchClassSegment([0, 1, 4, 7, 9])
            >>> operator_(pitch_classes)
            PitchClassSegment([0, 1, 1, 4, 4, 4, 7, 7, 7, 7, 9])

        Returns new object with type equal to that of ``argument``.
        """
        if not isinstance(argument, collections.abc.Sequence):
            argument = (argument,)

        counts = self.counts
        if isinstance(counts, int):
            counts = counts + 1
        else:
            counts = [_ + 1 for _ in counts]

        if not self.period and not self.indices:
            if isinstance(counts, int):
                return type(argument)(argument * counts)
            else:
                counts = _cyclictuple.CyclicTuple(counts)
                result = []
                for i, x in enumerate(argument):
                    count = counts[i]
                    result.extend([x] * count)
                if isinstance(argument, _typedcollections.TypedCollection):
                    result = _new.new(argument, items=result)
                else:
                    result = type(argument)(result)
                return result

        if isinstance(counts, int):
            counts = [counts]
        counts = _cyclictuple.CyclicTuple(counts)

        if not self.indices:
            if isinstance(argument, _typedcollections.TypedCollection):
                result = _new.new(argument, items=())
            else:
                result = type(argument)()
            iterator = _sequence.Sequence(argument).partition_by_counts(
                [self.period], cyclic=True, overhang=True
            )
            for i, shard in enumerate(iterator):
                shard = type(argument)(shard) * counts[i]
                result = result + shard
            return result

        pattern = _pattern.Pattern(indices=self.indices, period=self.period)
        result = []
        length = len(argument)
        j = 0
        for i, x in enumerate(argument):
            if pattern.matches_index(i, length):
                count = counts[j]
                result.extend([x] * count)
                j += 1
            else:
                result.append(x)
        if isinstance(argument, _typedcollections.TypedCollection):
            result = _new.new(argument, items=result)
        else:
            result = type(argument)(result)
        return result

    def __eq__(self, argument) -> bool:
        """
        Delegates to ``abjad.format.compare_objects()``.
        """
        return _format.compare_objects(self, argument)

    def __hash__(self) -> int:
        """
        Hashes duplication.
        """
        return hash(self.__class__.__name__ + str(self))

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return _format.get_repr(self)

    ### PUBLIC PROPERTIES ###

    @property
    def counts(self):
        """
        Gets counts of duplication.

        ..  container:: example

            >>> operator_ = abjad.Duplication(counts=1, period=3)
            >>> operator_.counts
            1

        Returns integer or none.
        """
        return self._counts

    @property
    def indices(self):
        """
        Gets indices of duplication.

        ..  container:: example

            >>> operator_ = abjad.Duplication(
            ...     counts=1,
            ...     indices=(0, -1),
            ...     )
            >>> operator_.indices
            (0, -1)

        Returns integer or none.
        """
        return self._indices

    @property
    def period(self):
        """
        Gets period of duplication.

        ..  container:: example

            >>> operator_ = abjad.Duplication(counts=1, period=3)
            >>> operator_.period
            3

        Returns integer or none.
        """
        return self._period


class Inversion:
    """
    Inversion operator.

    ..  container:: example

        >>> abjad.Inversion()
        Inversion()

    ..  container:: example

        >>> abjad.Inversion(axis=15)
        Inversion(axis=NamedPitch("ef''"))

    Object model of twelve-tone inversion operator.
    """

    ### CLASS VARIABLES ##

    __slots__ = ("_axis",)

    ### INITIALIZER ###

    def __init__(self, *, axis=None):
        if axis is not None:
            axis = NamedPitch(axis)
        self._axis = axis

    ### SPECIAL METHODS ###

    def __add__(self, operator):
        r"""
        Composes inversion and ``operator``.

        ..  container:: example

            Example segment:

            >>> items = [0, 2, 4, 5]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            Example operators:

            >>> inversion = abjad.Inversion()
            >>> transposition = abjad.Transposition(n=3)

        ..  container:: example

            Transposition followed by inversion:

            >>> operator = inversion + transposition
            >>> str(operator)
            'IT3'

            >>> segment_ = operator(segment)
            >>> lilypond_file = abjad.illustrate(segment_)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    a'8
                    g'8
                    f'8
                    e'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Inversion followed by transposition:

            >>> operator = transposition + inversion
            >>> str(operator)
            'T3I'

            >>> segment_ = operator(segment)
            >>> lilypond_file = abjad.illustrate(segment_)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    ef'8
                    cs'8
                    b'8
                    bf'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Returns compound operator:

            >>> string = abjad.storage(operator)
            >>> print(string)
            abjad.CompoundOperator(
                operators=[
                    Inversion(),
                    Transposition(n=3),
                    ],
                )

        """
        return CompoundOperator._compose_operators(self, operator)

    def __call__(self, argument):
        """
        Calls inversion on ``argument``.

        ..  container:: example

            Inverts numbered pitch-class:

            >>> inversion = abjad.Inversion()
            >>> pitch_class = abjad.NumberedPitchClass(1)
            >>> inversion(pitch_class)
            NumberedPitchClass(11)

        ..  container:: example

            Inverts numbered pitch:

            >>> inversion = abjad.Inversion()
            >>> pitch = abjad.NumberedPitch(15)
            >>> inversion(pitch)
            NumberedPitch(-15)

        ..  container:: example

            Inverts named pitch:

            >>> inversion = abjad.Inversion()
            >>> pitch = abjad.NamedPitch("d'")
            >>> inversion(pitch)
            NamedPitch('bf')

        ..  container:: example

            Inverts named pitch class:

            >>> inversion = abjad.Inversion()
            >>> pitch_class = abjad.NamedPitchClass('d')
            >>> inversion(pitch_class)
            NamedPitchClass('bf')

        ..  container:: example

            Inverts pitch segment:

            >>> inversion = abjad.Inversion()
            >>> segment = abjad.PitchSegment("c' d' e'")
            >>> inversion(segment)
            PitchSegment("c' bf af")

        ..  container:: example

            Inverts pitch class segment:

            >>> inversion = abjad.Inversion()
            >>> segment = abjad.PitchClassSegment("c d e")
            >>> inversion(segment)
            PitchClassSegment("c bf af")

        ..  container:: example

            Inverts pitch class set:

            >>> inversion = abjad.Inversion()
            >>> setting = abjad.PitchClassSet("c d e")
            >>> inversion(setting)
            PitchClassSet(['c', 'af', 'bf'])

        Returns new object with type equal to that of ``argument``.
        """
        if hasattr(argument, "invert"):
            result = argument.invert(axis=self.axis)
        else:
            raise TypeError(f"do not know how to invert: {argument!r}.")
        return result

    def __eq__(self, argument) -> bool:
        """
        Delegates to ``abjad.format.compare_objects()``.
        """
        return _format.compare_objects(self, argument)

    def __hash__(self) -> int:
        """
        Hashes inversion.
        """
        return hash(self.__class__.__name__ + str(self))

    def __radd__(self, operator):
        """
        Right-addition not defined on inversion.

        ..  container:: example

            >>> abjad.Inversion().__radd__(abjad.Inversion())
            Traceback (most recent call last):
                ...
            NotImplementedError: right-addition not defined on Inversion.

        Raises not implemented error.
        """
        message = f"right-addition not defined on {type(self).__name__}."
        raise NotImplementedError(message)

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return _format.get_repr(self)

    def __str__(self):
        """
        Gets string representation of operator.

        ..  container:: example

            >>> str(abjad.Inversion())
            'I'

        ..  container:: example

            >>> str(abjad.Inversion(axis=15))
            'I(Eb5)'

        """
        if self.axis is None:
            return "I"
        axis = self.axis.get_name(locale="us")
        string = f"I({axis})"
        return string

    def _is_identity_operator(self):
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def axis(self):
        """
        Gets axis of inversion.

        ..  container:: example

            >>> inversion = abjad.Inversion()
            >>> inversion.axis is None
            True

        ..  container:: example

            >>> inversion = abjad.Inversion(axis=15)
            >>> inversion.axis
            NamedPitch("ef''")

        Returns named pitch or none.
        """
        return self._axis


class Multiplication:
    """
    Multiplication operator.

    ..  container:: example

        >>> abjad.Multiplication()
        Multiplication(n=1)

    ..  container:: example

        >>> abjad.Multiplication(n=5)
        Multiplication(n=5)

    Object model of twelve-tone multiplication operator.
    """

    ### CLASS VARIABLES ##

    __slots__ = ("_n",)

    ### INITIALIZER ###

    def __init__(self, *, n=1):
        self._n = n

    ### SPECIAL METHODS ###

    def __add__(self, operator):
        r"""
        Composes multiplication and ``operator``.

        ..  container:: example

            Example segment:

            >>> items = [0, 2, 4, 5]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            Example operators:

            >>> multiplication = abjad.Multiplication(n=5)
            >>> transposition = abjad.Transposition(n=3)

        ..  container:: example


            Transposition followed by multiplication:

            >>> operator = multiplication + transposition
            >>> str(operator)
            'M5T3'

            >>> segment_ = operator(segment)
            >>> lilypond_file = abjad.illustrate(segment_)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    ef'8
                    cs'8
                    b'8
                    e'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Same as above because multiplication and transposition commute:

            >>> operator = transposition + multiplication
            >>> str(operator)
            'T3M5'

            >>> segment_ = operator(segment)
            >>> lilypond_file = abjad.illustrate(segment_)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    ef'8
                    cs'8
                    b'8
                    e'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        Returns compound operator.
        """
        return CompoundOperator._compose_operators(self, operator)

    def __call__(self, argument):
        """
        Calls multiplication on ``argument``.

        ..  container:: example

            Multiplies pitch-class:

            >>> multiplication = abjad.Multiplication(n=5)
            >>> pitch_class = abjad.NumberedPitchClass(4)
            >>> multiplication(pitch_class)
            NumberedPitchClass(8)

        ..  container:: example

            Multiplies pitch:

            >>> multiplication = abjad.Multiplication(n=7)
            >>> pitch = abjad.NamedPitch("f'")
            >>> multiplication(pitch)
            NamedPitch("b'''")

        Returns new object with type equal to that of ``argument``.
        """
        if hasattr(argument, "multiply"):
            result = argument.multiply(self.n)
        else:
            raise TypeError(f"do not know how to multiply: {argument!r}.")
        return result

    def __eq__(self, argument) -> bool:
        """
        Delegates to ``abjad.format.compare_objects()``.
        """
        return _format.compare_objects(self, argument)

    def __hash__(self) -> int:
        """
        Hashes multiplication.
        """
        return hash(self.__class__.__name__ + str(self))

    def __radd__(self, operator):
        """
        Right-addition not defined on multiplication.

        ..  container:: example

            >>> abjad.Multiplication().__radd__(abjad.Multiplication())
            Traceback (most recent call last):
                ...
            NotImplementedError: right-addition not defined on Multiplication.

        Raises not implemented error.
        """
        message = f"right-addition not defined on {type(self).__name__}."
        raise NotImplementedError(message)

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return _format.get_repr(self)

    def __str__(self):
        """
        Gets string representation of operator.

        ..  container:: example

            >>> str(abjad.Multiplication())
            'M1'

        ..  container:: example

            >>> str(abjad.Multiplication(n=5))
            'M5'

        """
        string = f"M{self.n}"
        return string

    ### PRIVATE METHODS ###

    def _is_identity_operator(self):
        if self.n == 1:
            return True
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def n(self):
        """
        Gets index of multiplication.

        ..  container:: example

            >>> multiplication = abjad.Multiplication()
            >>> multiplication.n
            1

        ..  container:: example

            >>> multiplication = abjad.Multiplication(n=5)
            >>> multiplication.n
            5

        Set to integer or none.
        """
        return self._n


class Retrograde:
    """
    Retrograde operator.

    ..  container:: example:

        >>> abjad.Retrograde()
        Retrograde()

    Object model of twelve-tone retrograde operator.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_period",)

    ### INITIALIZER ###

    def __init__(self, period=None):
        if period is not None:
            period = abs(int(period))
            assert 0 < period
        self._period = period

    ### SPECIAL METHODS ###

    def __add__(self, operator):
        r"""
        Composes retrograde and ``operator``.

        ..  container:: example

            Example segment:

            >>> items = [0, 2, 4, 5]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            Example operators:

            >>> retrograde = abjad.Retrograde()
            >>> transposition = abjad.Transposition(n=3)

        ..  container:: example

            Transposition followed by retrograde:

            >>> operator = retrograde + transposition
            >>> str(operator)
            'RT3'

            >>> segment_ = operator(segment)
            >>> lilypond_file = abjad.illustrate(segment_)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    af'8
                    g'8
                    f'8
                    ef'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Same as above because retrograde and transposition commute:

            >>> operator = transposition + retrograde
            >>> str(operator)
            'T3R'

            >>> segment_ = operator(segment)
            >>> lilypond_file = abjad.illustrate(segment_)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    af'8
                    g'8
                    f'8
                    ef'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Returns compound operator:

            >>> string = abjad.storage(operator)
            >>> print(string)
            abjad.CompoundOperator(
                operators=[
                    Retrograde(),
                    Transposition(n=3),
                    ],
                )

        """
        return CompoundOperator._compose_operators(self, operator)

    def __call__(self, argument):
        """
        Calls retrograde on ``argument``.

        ..  container:: example

            Gets retrograde pitch classes:

            >>> retrograde = abjad.Retrograde()
            >>> segment = abjad.PitchClassSegment([0, 1, 4, 7])
            >>> retrograde(segment)
            PitchClassSegment([7, 4, 1, 0])

        ..  container:: example

            Does not retrograde single pitches or pitch-classes:

            >>> retrogresion = abjad.Retrograde()
            >>> pitch_class = abjad.NumberedPitchClass(6)
            >>> retrograde(pitch_class)
            NumberedPitchClass(6)

        ..  container:: example

            Periodic retrograde:

            ..  todo:: Deprecated.

            >>> retrograde = abjad.Retrograde(period=3)
            >>> segment = abjad.PitchSegment("c' d' e' f' g' a' b' c''")
            >>> retrograde(segment)
            PitchSegment("e' d' c' a' g' f' c'' b'")

        Returns new object with type equal to that of ``argument``.
        """
        if isinstance(argument, (Pitch, PitchClass)):
            return argument
        if not isinstance(argument, (PitchSegment, PitchClassSegment)):
            argument = PitchSegment(argument)
        if not self.period:
            return type(argument)(reversed(argument))
        result = _new.new(argument, items=())
        for shard in _sequence.Sequence(argument).partition_by_counts(
            [self.period], cyclic=True, overhang=True
        ):
            shard = type(argument)(shard)
            shard = type(argument)(reversed(shard))
            result = result + shard
        return result

    def __eq__(self, argument) -> bool:
        """
        Delegates to ``abjad.format.compare_objects()``.
        """
        return _format.compare_objects(self, argument)

    def __hash__(self) -> int:
        """
        Hashes retrograde.
        """
        return hash(self.__class__.__name__ + str(self))

    def __radd__(self, operator):
        """
        Right-addition not defined on retrograde.

        ..  container:: example

            >>> abjad.Retrograde().__radd__(abjad.Retrograde())
            Traceback (most recent call last):
                ...
            NotImplementedError: right-addition not defined on Retrograde.

        Raises not implemented error.
        """
        message = f"right-addition not defined on {type(self).__name__}."
        raise NotImplementedError(message)

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return _format.get_repr(self)

    def __str__(self):
        """
        Gets string representation of operator.

        ..  container:: example

            >>> str(abjad.Retrograde())
            'R'

        """
        return "R"

    ### PRIVATE METHODS ###

    def _is_identity_operator(self):
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def period(self):
        """
        Gets optional period of retrograde.

        ..  todo:: Deprecated.

        ..  container:: example

            >>> retrograde = abjad.Retrograde(period=3)
            >>> retrograde.period
            3

        Returns integer or none.
        """
        return self._period


class Rotation:
    """
    Rotation operator.

    ..  container:: example:

        >>> abjad.Rotation()
        Rotation(n=0)

    ..  container:: example

        >>> abjad.Rotation(n=1)
        Rotation(n=1)

    Object model of the twelve-tone rotation operator.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_n", "_period")

    ### INITIALIZER ###

    def __init__(self, *, n=0, period=None):
        self._n = int(n)
        if period is not None:
            period = abs(int(period))
            assert 0 < period
        self._period = period

    ### SPECIAL METHODS ###

    def __add__(self, operator):
        r"""
        Composes rotation and ``operator``.

        ..  container:: example

            Example segment:

            >>> items = [0, 2, 4, 5]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            Example operators:

            >>> rotation = abjad.Rotation(n=-1)
            >>> transposition = abjad.Transposition(n=3)

        ..  container:: example

            Transposition followed by rotation:

            >>> operator = rotation + transposition
            >>> str(operator)
            'r-1T3'

            >>> segment_ = operator(segment)
            >>> lilypond_file = abjad.illustrate(segment_)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    f'8
                    g'8
                    af'8
                    ef'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Same as above because rotation and transposition commute:

            >>> operator = transposition + rotation
            >>> str(operator)
            'T3r-1'

            >>> segment_ = operator(segment)
            >>> lilypond_file = abjad.illustrate(segment_)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    f'8
                    g'8
                    af'8
                    ef'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Returns compound operator:

            >>> string = abjad.storage(operator)
            >>> print(string)
            abjad.CompoundOperator(
                operators=[
                    Rotation(n=-1),
                    Transposition(n=3),
                    ],
                )

        """
        return CompoundOperator._compose_operators(self, operator)

    def __call__(self, argument):
        """
        Calls rotation on ``argument``.

        ..  container:: example

            Rotates pitch classes:

            >>> rotation = abjad.Rotation(n=1)
            >>> pitch_classes = abjad.PitchClassSegment([0, 1, 4, 7])
            >>> rotation(pitch_classes)
            PitchClassSegment([7, 0, 1, 4])

        ..  container:: example

            Does not rotate single pitches or pitch-classes:

            >>> rotation = abjad.Rotation(n=1)
            >>> pitch_class = abjad.NumberedPitchClass(6)
            >>> rotation(pitch_class)
            NumberedPitchClass(6)

        ..  container:: example

            Periodic rotation:

            ..  todo:: Deprecated.

            >>> rotation = abjad.Rotation(n=1, period=3)
            >>> pitches = abjad.PitchSegment("c' d' e' f' g' a' b' c''")
            >>> rotation(pitches)
            PitchSegment("e' c' d' a' f' g' c'' b'")

        Returns new object with type equal to that of ``argument``.
        """
        if isinstance(argument, (Pitch, PitchClass)):
            return argument
        if not isinstance(argument, (PitchSegment, PitchClassSegment)):
            argument = PitchSegment(argument)
        if not self.period:
            return argument.rotate(self.n)
        result = _new.new(argument, items=())
        for shard in _sequence.Sequence(argument).partition_by_counts(
            [self.period], cyclic=True, overhang=True
        ):
            shard = type(argument)(shard)
            shard = shard.rotate(self.n)
            result = result + shard
        return result

    def __eq__(self, argument) -> bool:
        """
        Delegates to ``abjad.format.compare_objects()``.
        """
        return _format.compare_objects(self, argument)

    def __hash__(self) -> int:
        """
        Hashes rotation.
        """
        return hash(self.__class__.__name__ + str(self))

    def __radd__(self, operator):
        """
        Right-addition not defined on rotation.

        ..  container:: example

            >>> abjad.Rotation().__radd__(abjad.Rotation())
            Traceback (most recent call last):
                ...
            NotImplementedError: right-addition not defined on Rotation.

        Raises not implemented error.
        """
        message = f"right-addition not defined on {type(self).__name__}."
        raise NotImplementedError(message)

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return _format.get_repr(self)

    def __str__(self):
        """
        Gets string representation of operator.

        ..  container:: example

            >>> str(abjad.Rotation())
            'r0'

        ..  container:: example

            >>> str(abjad.Rotation(n=1))
            'r1'

        """
        string = f"r{self.n}"
        return string

    ### PRIVATE METHODS ###

    def _is_identity_operator(self):
        if self.n == 0:
            return True
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def n(self):
        """
        Gets index of rotation.

        ..  container:: example

            >>> rotation = abjad.Rotation()
            >>> rotation.n
            0

        ..  container:: example

            >>> rotation = abjad.Rotation(n=2)
            >>> rotation.n
            2

        Returns integer.
        """
        return self._n

    @property
    def period(self):
        """
        Gets period of rotation.

        ..  todo:: Deprecated.

        ..  container:: example

            >>> rotation = abjad.Rotation(n=2, period=3)
            >>> rotation.period
            3

        Returns integer or none.
        """
        return self._period


class Transposition:
    """
    Transposition operator.

    ..  container:: example

        >>> abjad.Transposition()
        Transposition(n=0)

    ..  container:: example

        >>> abjad.Transposition(n=2)
        Transposition(n=2)

    Object model of twelve-tone transposition operator.
    """

    ### CLASS VARIABLES ##

    __slots__ = ("_n",)

    ### INITIALIZER ###

    def __init__(self, *, n=0):
        self._n = n

    ### SPECIAL METHODS ###

    def __add__(self, operator):
        r"""
        Composes transposition and ``operator``.

        ..  container:: example

            Example segment:

            >>> items = [0, 2, 4, 5]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            Example operators:

            >>> T_1 = abjad.Transposition(n=1)
            >>> T_3 = abjad.Transposition(n=3)

        ..  container:: example

            Successive transposition:

            >>> operator = T_1 + T_3
            >>> str(operator)
            'T1T3'

            >>> segment_ = operator(segment)
            >>> lilypond_file = abjad.illustrate(segment_)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    e'8
                    fs'8
                    af'8
                    a'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Same as above because transposition commutes:

            >>> operator = T_3 + T_1
            >>> str(operator)
            'T3T1'

            >>> segment_ = operator(segment)
            >>> lilypond_file = abjad.illustrate(segment_)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    e'8
                    fs'8
                    af'8
                    a'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        Returns compound operator.
        """
        return CompoundOperator._compose_operators(self, operator)

    def __call__(self, argument):
        """
        Calls transposition on ``argument``.

        ..  container:: example

            Transposes pitch-class:

            >>> transposition = abjad.Transposition(n=2)
            >>> pitch_class = abjad.NumberedPitchClass(1)
            >>> transposition(pitch_class)
            NumberedPitchClass(3)

        ..  container:: example

            Transposes pitch:

            >>> transposition = abjad.Transposition(n=2)
            >>> pitch = abjad.NumberedPitch(15)
            >>> transposition(pitch)
            NumberedPitch(17)

        ..  container:: example

            Transposes list of pitches:

            >>> transposition = abjad.Transposition(n=2)
            >>> pitches = [abjad.NumberedPitch(_) for _ in [15, 16]]
            >>> transposition(pitches)
            [NumberedPitch(17), NumberedPitch(18)]

        Returns new object with type equal to that of ``argument``.
        """
        if hasattr(argument, "transpose"):
            result = argument.transpose(self.n)
        elif isinstance(argument, collections.abc.Iterable):
            items = []
            for item in argument:
                item = item.transpose(self.n)
                items.append(item)
            result = type(argument)(items)
        else:
            raise TypeError(f"do not know how to transpose: {argument!r}.")
        return result

    def __eq__(self, argument) -> bool:
        """
        Delegates to ``abjad.format.compare_objects()``.
        """
        return _format.compare_objects(self, argument)

    def __hash__(self) -> int:
        """
        Hashes transposition.
        """
        return hash(self.__class__.__name__ + str(self))

    def __radd__(self, operator):
        """
        Right-addition not defined on transposition.

        ..  container:: example

            >>> abjad.Transposition().__radd__(abjad.Transposition())
            Traceback (most recent call last):
                ...
            NotImplementedError: right-addition not defined on Transposition.

        Raises not implemented error.
        """
        message = f"right-addition not defined on {type(self).__name__}."
        raise NotImplementedError(message)

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return _format.get_repr(self)

    def __str__(self):
        """
        Gets string representation of operator.

        ..  container:: example

            >>> str(abjad.Transposition())
            'T0'

        ..  container:: example

            >>> str(abjad.Transposition(n=2))
            'T2'

        """
        string = f"T{self.n}"
        return string

    ### PRIVATE METHODS ###

    def _is_identity_operator(self):
        if self.n == 0:
            return True
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def n(self):
        """
        Gets index of transposition.

        ..  container:: example

            >>> transposition = abjad.Transposition()
            >>> transposition.n
            0

        ..  container:: example

            >>> transposition = abjad.Transposition(n=2)
            >>> transposition.n
            2

        Set to integer, interval or none.
        """
        return self._n


@functools.total_ordering
class PitchClass:
    """
    Abstract pitch-class.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    _is_abstract = True

    ### INITIALIZER ###

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

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Delegates to ``abjad.format.compare_objects()``.
        """
        return _format.compare_objects(self, argument)

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

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return _format.get_repr(self)

    ### PRIVATE METHODS ###

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

    ### PUBLIC PROPERTIES ###

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

    ### PUBLIC METHODS ###

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

    ..  container:: example

        Initializes from number of semitones:

        >>> abjad.NamedPitchClass(14)
        NamedPitchClass('d')

        >>> abjad.NamedPitchClass(14.5)
        NamedPitchClass('dqs')

    ..  container:: example

        Initializes from named pitch:

        >>> abjad.NamedPitchClass(abjad.NamedPitch('d'))
        NamedPitchClass('d')

        >>> abjad.NamedPitchClass(abjad.NamedPitch('dqs'))
        NamedPitchClass('dqs')

    ..  container:: example

        Initializes from numbered pitch:

        >>> abjad.NamedPitchClass(abjad.NumberedPitch(14))
        NamedPitchClass('d')

        >>> abjad.NamedPitchClass(abjad.NumberedPitch(14.5))
        NamedPitchClass('dqs')

    ..  container:: example

        Initializes from numbered pitch-class:

        >>> abjad.NamedPitchClass(abjad.NumberedPitchClass(2))
        NamedPitchClass('d')

        >>> abjad.NamedPitchClass(abjad.NumberedPitchClass(2.5))
        NamedPitchClass('dqs')

    ..  container:: example

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

    ..  container:: example

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

    ..  container:: example

        Initializes from note:

        >>> abjad.NamedPitchClass(abjad.Note("d''8."))
        NamedPitchClass('d')

        >>> abjad.NamedPitchClass(abjad.Note("dqs''8."))
        NamedPitchClass('dqs')

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_diatonic_pc_number", "_accidental")

    ### INITIALIZER ###

    def __init__(self, name="c", *, accidental=None, arrow=None):
        super().__init__(name or "c")
        if accidental is not None:
            self._accidental = type(self._accidental)(accidental)
        if arrow is not None:
            self._accidental = type(self._accidental)(self._accidental, arrow=arrow)

    ### SPECIAL METHODS ###

    def __add__(self, named_interval):
        """
        Adds ``named_interval`` to named pitch-class.

        ..  container:: example

            >>> abjad.NamedPitchClass('cs') + abjad.NamedInterval('+M9')
            NamedPitchClass('ds')

            >>> abjad.NamedPitchClass('cs') + abjad.NamedInterval('-M9')
            NamedPitchClass('b')

        Returns new named pitch-class.
        """
        dummy_pitch = NamedPitch((self.name, 4))
        pitch = named_interval.transpose(dummy_pitch)
        return type(self)(pitch)

    def __eq__(self, argument):
        """
        Is true when ``argument`` can be coerced to a named pitch-class with
        pitch-class name equal to that of this named pitch-class.

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

        Returns true or false.
        """
        return super().__eq__(argument)

    def __hash__(self):
        """
        Hashes named pitch-class.

        Returns integer.
        """
        return super().__hash__()

    def __lt__(self, argument):
        """
        Is true when ``argument`` is a named pitch-class with a pitch
        number greater than that of this named pitch-class.

        ..  container:: example

            Compares less than:

            >>> abjad.NamedPitchClass('cs') < abjad.NamedPitchClass('d')
            True

        ..  container:: example

            Does not compare less than:

            >>> abjad.NamedPitchClass('d') < abjad.NamedPitchClass('cs')
            False

        Raises type error when ``argument`` is not a named pitch-class.
        """
        if not isinstance(argument, type(self)):
            raise TypeError(f"can not compare named pitch-class to {argument!r}.")
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

    def __str__(self):
        """
        Gets string representation of named pitch-class.

        ..  container:: example

            >>> str(abjad.NamedPitchClass('cs'))
            'cs'

        Returns string.
        """
        return self.name

    def __sub__(self, argument):
        """
        Subtracts ``argument`` from named pitch-class.

        ..  container:: example

            >>> abjad.NamedPitchClass('cs') - abjad.NamedPitchClass('g')
            NamedInversionEquivalentIntervalClass('+A4')

            >>> abjad.NamedPitchClass('c') - abjad.NamedPitchClass('cf')
            NamedInversionEquivalentIntervalClass('+A1')

            >>> abjad.NamedPitchClass('cf') - abjad.NamedPitchClass('c')
            NamedInversionEquivalentIntervalClass('+A1')

        Returns named inversion-equivalent interval-class.
        """
        if not isinstance(argument, type(self)):
            raise TypeError(f"must be named pitch-class: {argument!r}.")
        pitch_1 = NamedPitch((self.name, 4))
        pitch_2 = NamedPitch((argument.name, 4))
        mdi = NamedInterval.from_pitch_carriers(pitch_1, pitch_2)
        pair = (mdi.quality, mdi.number)
        dic = NamedInversionEquivalentIntervalClass(pair)
        return dic

    ### PRIVATE METHODS ###

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

    def _get_format_specification(self):
        values = [self.name]
        return _format.FormatSpecification(
            coerce_for_equality=True,
            storage_format_is_not_indented=True,
            storage_format_args_values=values,
            storage_format_keyword_names=[],
        )

    def _get_lilypond_format(self):
        name = self._get_diatonic_pc_name()
        accidental = Accidental(self._get_alteration())
        return f"{name}{accidental!s}"

    ### PUBLIC PROPERTIES ###

    @property
    def accidental(self):
        """
        Gets accidental.

        ..  container:: example

            >>> abjad.NamedPitchClass('cs').accidental
            Accidental('sharp')

        Returns accidental.
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
    def name(self):
        """
        Gets name of named pitch-class.

        ..  container:: example

            >>> abjad.NamedPitchClass('cs').name
            'cs'

        Returns string.
        """
        diatonic_pc_name = _diatonic_pc_number_to_diatonic_pc_name[
            self._diatonic_pc_number
        ]
        return f"{diatonic_pc_name}{self._accidental!s}"

    @property
    def number(self):
        """
        Gets number.

        ..  container:: example

            >>> abjad.NamedPitchClass('cs').number
            1

        Returns nonnegative integer or float.
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

            >>> abjad.NamedPitchClass('cs').pitch_class_label
            'C#'

        Returns string.
        """
        pc = self._get_diatonic_pc_name().upper()
        return f"{pc}{self.accidental.symbol}"

    ### PUBLIC METHODS ###

    def invert(self, axis=None):
        """
        Inverts named pitch-class.

        Not yet implemented.
        """
        axis = axis or NamedPitch("c")
        axis = NamedPitch(axis)
        this = NamedPitch(self)
        interval = this - axis
        result = axis.transpose(interval)
        result = type(self)(result)
        return result

    def multiply(self, n=1):
        """
        Multiplies named pitch-class by ``n``.

        ..  container:: example

            >>> abjad.NamedPitchClass('cs').multiply(3)
            NamedPitchClass('ef')

        Returns new named pitch-class.
        """
        return type(self)(n * self.number)

    def transpose(self, n=0):
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

        Returns new named pitch-class.
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

    ..  container:: example

        Initializes from pitch name.

        >>> abjad.NumberedPitchClass('d')
        NumberedPitchClass(2)

    ..  container:: example

        Initializes from named pitch.

        >>> abjad.NumberedPitchClass(abjad.NamedPitch('g,'))
        NumberedPitchClass(7)

    ..  container:: example

        Initializes from numbered pitch.

        >>> abjad.NumberedPitchClass(abjad.NumberedPitch(15))
        NumberedPitchClass(3)

    ..  container:: example

        Initializes from named pitch-class.

        >>> abjad.NumberedPitchClass(abjad.NamedPitchClass('e'))
        NumberedPitchClass(4)

    ..  container:: example

        Initializes from pitch-class / octave string:

        >>> abjad.NumberedPitchClass('C#5')
        NumberedPitchClass(1)

    ..  container:: example

        Initializes from other numbered pitch-class:

        >>> abjad.NumberedPitchClass(abjad.NumberedPitchClass(9))
        NumberedPitchClass(9)

    ..  container:: example

        Initializes from note:

        >>> abjad.NumberedPitchClass(abjad.Note("a'8."))
        NumberedPitchClass(9)

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_arrow", "_number")

    ### INITIALIZER ###

    def __init__(self, number=0, *, arrow=None):
        super().__init__(number or 0)
        if arrow is not None:
            arrow = _enums.VerticalAlignment.from_expr(arrow)
            if arrow is _enums.Center:
                arrow = None
            self._arrow = arrow

    ### SPECIAL METHODS ###

    def __add__(self, argument):
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

        Returns new numbered pitch-class.
        """
        interval = NumberedInterval(argument)
        return type(self)(self.number + interval.number % 12)

    def __copy__(self, *arguments):
        """
        Copies numbered pitch-class.

        ..  container:: example

            >>> import copy
            >>> pitch_class = abjad.NumberedPitchClass(9)
            >>> copy.copy(pitch_class)
            NumberedPitchClass(9)

        Returns new numbered pitch-class.
        """
        return type(self)(self)

    def __eq__(self, argument):
        """
        Is true when ``argument`` is a numbered pitch-class with pitch-class
        number equal to that of this numbered pitch-class.

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

        Returns true or false.
        """
        return super().__eq__(argument)

    def __hash__(self):
        """
        Hashes numbered pitch-class.

        Returns integer.
        """
        return super().__hash__()

    def __lt__(self, argument):
        """
        Is true when ``argument`` is a numbered pitch-class with a pitch
        number greater than that of this numberd pitch-class.

        ..  container:: example

            Compares less than:

            >>> abjad.NumberedPitchClass(1) < abjad.NumberedPitchClass(2)
            True

        ..  container:: example

            Does not compare less than:

            >>> abjad.NumberedPitchClass(2) < abjad.NumberedPitchClass(1)
            False

        Raises type error when ``argument`` is not a numbered pitch-class.
        """
        if not isinstance(argument, type(self)):
            raise TypeError(f"can not compare numbered pitch-class to {argument!r}.")
        return self.number < argument.number

    def __neg__(self):
        """
        Negates numbered pitch-class.

        ..  container:: example

            >>> pitch_class = abjad.NumberedPitchClass(9)
            >>> -pitch_class
            NumberedPitchClass(3)

        Returns new numbered pitch-class.
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

    def __str__(self):
        """
        Gets string representation of numbered pitch-class.

        Returns string.
        """
        return str(self.number)

    def __sub__(self, argument):
        """
        Subtracts ``argument`` from numbered pitch-class.

        Subtraction is defined against both numbered intervals
        and against other pitch-classes.

        ..  container:: example

            >>> abjad.NumberedPitchClass(6) - abjad.NumberedPitchClass(6)
            NumberedInversionEquivalentIntervalClass(0)

            >>> abjad.NumberedPitchClass(6) - abjad.NumberedPitchClass(7)
            NumberedInversionEquivalentIntervalClass(1)

            >>> abjad.NumberedPitchClass(7) - abjad.NumberedPitchClass(6)
            NumberedInversionEquivalentIntervalClass(1)

        ..  container:: example

            >>> abjad.NumberedPitchClass(6) - abjad.NumberedInterval(-1)
            NumberedPitchClass(5)

            >>> abjad.NumberedPitchClass(6) - abjad.NumberedInterval(0)
            NumberedPitchClass(6)

            >>> abjad.NumberedPitchClass(6) - abjad.NumberedInterval(1)
            NumberedPitchClass(5)

        Returns numbered inversion-equivalent interval-class.
        """
        if isinstance(argument, type(self)):
            interval_class_number = abs(self.number - argument.number)
            if 6 < interval_class_number:
                interval_class_number = 12 - interval_class_number
            return NumberedInversionEquivalentIntervalClass(interval_class_number)
        interval_class = NumberedInversionEquivalentIntervalClass(argument)
        return type(self)(self.number - interval_class.number % 12)

    ### PRIVATE METHODS ###

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

    def _get_format_specification(self):
        values = [self.number]
        return _format.FormatSpecification(
            coerce_for_equality=True,
            storage_format_is_not_indented=True,
            storage_format_args_values=values,
            storage_format_keyword_names=[],
        )

    def _get_lilypond_format(self):
        return NamedPitchClass(self)._get_lilypond_format()

    ### PUBLIC PROPERTIES ###

    @property
    def accidental(self):
        """
        Gets accidental.

        ..  container:: example

            >>> abjad.NumberedPitchClass(1).accidental
            Accidental('sharp')

        Returns accidental.
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
    def name(self):
        """
        Gets name of numbered pitch-class.

        ..  container:: example

            >>> abjad.NumberedPitchClass(13).name
            'cs'

        Returns string.
        """
        return _pitch_class_number_to_pitch_class_name[self.number]

    @property
    def number(self):
        """
        Gets number.

        ..  container:: example

            >>> abjad.NumberedPitchClass(1).number
            1

        ..  container:: example

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

        Returns string.
        """
        name = self._get_diatonic_pc_name().upper()
        return f"{name}{self.accidental.symbol}"

    ### PUBLIC METHODS ###

    def invert(self, axis=None):
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

        Returns new numbered pitch-class.
        """
        axis = axis or NumberedPitch("c")
        axis = NumberedPitch(axis)
        this = NumberedPitch(self)
        interval = this - axis
        result = axis.transpose(interval)
        result = type(self)(result)
        return result

    def multiply(self, n=1):
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

        Returns new numbered pitch-class.
        """
        return type(self)(n * self.number)

    def transpose(self, n=0):
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

        Returns new numbered pitch-class.
        """
        return type(self)(self.number + n)


@functools.total_ordering
class Pitch:
    """
    Abstract pitch.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_pitch_class", "_octave")

    _is_abstract = True

    ### INITIALIZER ###

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

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Delegates to ``abjad.format.compare_objects()``.
        """
        return _format.compare_objects(self, argument)

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

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return _format.get_repr(self)

    ### PRIVATE PROPERTIES ###

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

    ### PUBLIC PROPERTIES ###

    @property
    def arrow(self):
        """
        Gets arrow of pitch.
        """
        raise NotImplementedError

    @property
    def hertz(self):
        """
        Gets frequency of pitch in Hertz.

        Returns float.
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

    ### PUBLIC METHODS ###

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


### TYPINGS ###

PitchTyping = typing.Union[int, str, Pitch]


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

    ..  container:: example

        Initializes from pitch-class / octave string:

        >>> abjad.NamedPitch('C#5')
        NamedPitch("cs''")

        Initializes quartertone from pitch-class / octave string:

        >>> abjad.NamedPitch('A+3')
        NamedPitch('aqs')

        >>> abjad.NamedPitch('Aqs3')
        NamedPitch('aqs')

    ..  container:: example

        Initializes arrowed pitch:

        >>> abjad.NamedPitch('C#5', arrow=abjad.Up)
        NamedPitch("cs''", arrow=Up)

    ..  container:: example

        REGRESSION. Small floats just less than a C initialize in the correct
        octave.

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

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, name="c'", *, accidental=None, arrow=None, octave=None):
        super().__init__(
            name or "c'", accidental=accidental, arrow=arrow, octave=octave
        )

    ### SPECIAL METHODS ###

    def __add__(self, interval):
        """
        Adds named pitch to ``interval``.

        ..  container:: example

            >>> abjad.NamedPitch("cs''") + abjad.NamedInterval('-M2')
            NamedPitch("b'")

            >>> abjad.NamedPitch("cs''") + abjad.NamedInterval('P1')
            NamedPitch("cs''")

            >>> abjad.NamedPitch("cs''") + abjad.NamedInterval('+M2')
            NamedPitch("ds''")

        Returns new named pitch.
        """
        interval = NamedInterval(interval)
        return interval.transpose(self)

    def __copy__(self, *arguments):
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

        ..  container:: example

            Copies arrowed pitch:

            >>> pitch = abjad.NamedPitch("cs''", arrow=abjad.Up)
            >>> copy.copy(pitch)
            NamedPitch("cs''", arrow=Up)

        Returns new named pitch.
        """
        return type(self)(self, arrow=self.arrow)

    def __eq__(self, argument):
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
        return super().__eq__(argument)

    def __hash__(self):
        """
        Hashes named pitch.

        Returns integer.
        """
        return super().__hash__()

    def __lt__(self, argument):
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

        Returns string.
        """
        return self.name

    def __sub__(self, argument):
        """
        Subtracts ``argument`` from named pitch.

        ..  container:: example

            >>> abjad.NamedPitch("cs''") - abjad.NamedPitch("b'")
            NamedInterval('-M2')

            >>> abjad.NamedPitch("cs''") - abjad.NamedPitch("fs''")
            NamedInterval('+P4')

        Returns named interval.
        """
        if isinstance(argument, type(self)):
            return NamedInterval.from_pitch_carriers(self, argument)
        interval = NamedInterval(argument)
        interval = -interval
        return interval.transpose(self)

    ### PRIVATE METHODS ###

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

    def _get_format_specification(self):
        return _format.FormatSpecification(
            coerce_for_equality=True,
            storage_format_args_values=[self.name],
            storage_format_is_not_indented=True,
            storage_format_keyword_names=["arrow"],
        )

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

    def _respell(self, accidental="sharps"):
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

    ### PUBLIC PROPERTIES ###

    @property
    def accidental(self):
        """
        Gets accidental of named pitch.

        ..  container:: example

            >>> abjad.NamedPitch("c''").accidental
            Accidental('natural')

            >>> abjad.NamedPitch("cs''").accidental
            Accidental('sharp')

            >>> abjad.NamedPitch("df''").accidental
            Accidental('flat')

        Returns accidental.
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

        ..  container:: example

            Displays arrow in interpreter representation:

            >>> abjad.NamedPitch("cs''", arrow=abjad.Down)
            NamedPitch("cs''", arrow=Down)

        Returns up, down or none.
        """
        return self._pitch_class.arrow

    @property
    def hertz(self):
        """
        Gets frequency of named pitch in Hertz.

        ..  container:: example

            >>> abjad.NamedPitch("c''").hertz
            523.25...

            >>> abjad.NamedPitch("cs''").hertz
            554.36...

            >>> abjad.NamedPitch("df''").hertz
            554.36...

        Returns float.
        """
        return super().hertz

    @property
    def name(self):
        """
        Gets name of named pitch.

        ..  container:: example

            >>> abjad.NamedPitch("c''").name
            "c''"

            >>> abjad.NamedPitch("cs''").name
            "cs''"

            >>> abjad.NamedPitch("df''").name
            "df''"

        Returns string.
        """
        return f"{self.pitch_class!s}{self.octave!s}"

    @property
    def number(self):
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

        Returns number.
        """
        diatonic_pc_number = self.pitch_class._get_diatonic_pc_number()
        pc_number = _diatonic_pc_number_to_pitch_class_number[diatonic_pc_number]
        alteration = self.pitch_class._get_alteration()
        octave_base_pitch = (self.octave.number - 4) * 12
        return _math.integer_equivalent_number_to_integer(
            pc_number + alteration + octave_base_pitch
        )

    @property
    def octave(self):
        """
        Gets octave of named pitch.

        ..  container:: example

            >>> abjad.NamedPitch("c''").octave
            Octave(5)

            >>> abjad.NamedPitch("cs''").octave
            Octave(5)

            >>> abjad.NamedPitch("df''").octave
            Octave(5)

        Returns octave.
        """
        return self._octave

    @property
    def pitch_class(self):
        """
        Gets pitch-class of named pitch.

        ..  container:: example

            >>> abjad.NamedPitch("c''").pitch_class
            NamedPitchClass('c')

            >>> abjad.NamedPitch("cs''").pitch_class
            NamedPitchClass('cs')

            >>> abjad.NamedPitch("df''").pitch_class
            NamedPitchClass('df')

        Returns named pitch-class.
        """
        return self._pitch_class

    ### PUBLIC METHODS ###

    @classmethod
    def from_hertz(class_, hertz):
        """
        Makes named pitch from ``hertz``.

        ..  container:: example

            >>> abjad.NamedPitch.from_hertz(440)
            NamedPitch("a'")

        ..  container:: example

            REGRESSION. Returns c'' (C5) and not c' (C4):

            >>> abjad.NamedPitch.from_hertz(519)
            NamedPitch("c''")

        Returns newly constructed named pitch.
        """
        return super().from_hertz(hertz)

    def get_name(self, locale=None):
        """
        Gets name of named pitch according to ``locale``.

        ..  container:: example

            >>> abjad.NamedPitch("cs''").get_name()
            "cs''"

            >>> abjad.NamedPitch("cs''").get_name(locale='us')
            'C#5'

        Set ``locale`` to ``'us'`` or none.

        Returns string.
        """
        if locale is None:
            return self.name
        elif locale == "us":
            name = self._get_diatonic_pc_name().upper()
            return f"{name}{self.accidental.symbol}{self.octave.number}"
        else:
            raise ValueError(f"must be 'us' or none: {locale!r}.")

    def invert(self, axis=None):
        """
        Inverts named pitch around ``axis``.

        ..  container:: example

            Inverts pitch around middle C explicitly:

            >>> abjad.NamedPitch("d'").invert("c'")
            NamedPitch('bf')

            >>> abjad.NamedPitch('bf').invert("c'")
            NamedPitch("d'")

        ..  container:: example

            Inverts pitch around middle C implicitly:

            >>> abjad.NamedPitch("d'").invert()
            NamedPitch('bf')

            >>> abjad.NamedPitch('bf').invert()
            NamedPitch("d'")

        ..  container:: example

            Inverts pitch around A3:

            >>> abjad.NamedPitch("d'").invert('a')
            NamedPitch('e')

        Interprets none-valued ``axis`` equal to middle C.

        Returns new named pitch.
        """
        return super().invert(axis=axis)

    def multiply(self, n=1):
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

        Returns new named pitch.
        """
        return super().multiply(n=n)

    def simplify(self):
        """
        Reduce alteration to between -2 and 2 while maintaining identical pitch
        number.

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
        octave = Octave(octave)
        pitch_name = f"{diatonic_pc_name}{accidental!s}{octave!s}"
        return type(self)(pitch_name, arrow=self.arrow)

    def transpose(self, n=0):
        """
        Transposes named pitch by index ``n``.

        ..  container:: example

            Transposes C4 up a minor second:

            >>> abjad.NamedPitch("c'").transpose(n='m2')
            NamedPitch("df'")

        ..  container:: example

            Transposes C4 down a major second:

            >>> abjad.NamedPitch("c'").transpose(n='-M2')
            NamedPitch('bf')

        Returns new named pitch.
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
        octave = int(math.floor((pitch_number - semitones) / 12)) + 4
        octave = Octave(octave)
        name = diatonic_pc_name + str(accidental) + octave.ticks
        return type(self)(name)


class NumberedPitch(Pitch):
    r"""
    Numbered pitch.

    ..  container:: example

        Initializes from number:

        >>> abjad.NumberedPitch(13)
        NumberedPitch(13)

    ..  container:: example

        Initializes from other numbered pitch

        >>> abjad.NumberedPitch(abjad.NumberedPitch(13))
        NumberedPitch(13)

    ..  container:: example

        Initializes from pitch-class / octave pair:

        >>> abjad.NumberedPitch((1, 5))
        NumberedPitch(13)

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_number",)

    ### INITIALIZER ###

    def __init__(self, number=0, *, arrow=None, octave=None):
        super().__init__(number or 0, arrow=arrow, octave=octave)

    ### SPECIAL METHODS ###

    def __add__(self, argument):
        """
        Adds ``argument`` to numbered pitch.

        ..  container:: example

            >>> abjad.NumberedPitch(12) + abjad.NumberedPitch(13)
            NumberedPitch(25)

            >>> abjad.NumberedPitch(13) + abjad.NumberedPitch(12)
            NumberedPitch(25)

        Returns new numbered pitch.
        """
        argument = type(self)(argument)
        semitones = float(self) + float(argument)
        return type(self)(semitones)

    def __lt__(self, argument):
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

        Returns true or false.
        """
        try:
            argument = type(self)(argument)
        except (ValueError, TypeError):
            return False
        return self.number < argument.number

    def __neg__(self):
        """
        Negates numbered pitch.

        ..  container:: example

            >>> -abjad.NumberedPitch(13.5)
            NumberedPitch(-13.5)

            >>> -abjad.NumberedPitch(-13.5)
            NumberedPitch(13.5)

        Returns new numbered pitch.
        """
        return type(self)(-self.number)

    def __radd__(self, argument):
        """
        Adds numbered pitch to ``argument``.

        ..  container:: example

            >>> pitch = abjad.NumberedPitch(13)
            >>> abjad.NumberedPitch(12).__radd__(pitch)
            NumberedPitch(25)

            >>> pitch = abjad.NumberedPitch(12)
            >>> abjad.NumberedPitch(13).__radd__(pitch)
            NumberedPitch(25)

        Returns new numbered pitch.
        """
        argument = type(self)(argument)
        return argument.__add__(self)

    def __str__(self):
        """
        Gets string representation of numbered pitch.

        Returns string.
        """
        return str(self.number)

    def __sub__(self, argument):
        """
        Subtracts ``argument`` from numbered pitch.

        ..  container:: example

            >>> abjad.NumberedPitch(12) - abjad.NumberedPitch(12)
            NumberedInterval(0)

            >>> abjad.NumberedPitch(12) - abjad.NumberedPitch(13)
            NumberedInterval(1)

            >>> abjad.NumberedPitch(13) - abjad.NumberedPitch(12)
            NumberedInterval(-1)

        Returns numbered interval.
        """
        if isinstance(argument, type(self)):
            return NumberedInterval.from_pitch_carriers(self, argument)
        interval = NumberedInterval(argument)
        interval = -interval
        return interval.transpose(self)

    ### PRIVATE METHODS ###

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

    def _get_format_specification(self):
        return _format.FormatSpecification(
            coerce_for_equality=True,
            storage_format_is_not_indented=True,
            storage_format_args_values=[self.number],
            storage_format_keyword_names=["arrow"],
        )

    def _get_lilypond_format(self):
        return self.name

    ### PUBLIC PROPERTIES ###

    @property
    def accidental(self):
        """
        Gets accidental of numbered pitch.

        ..  container:: example

            >>> abjad.NumberedPitchClass(13).accidental
            Accidental('sharp')

        Returns accidental.
        """
        return self.pitch_class.accidental

    @property
    def arrow(self):
        """
        Gets arrow of numbered pitch.

        ..  container:: example

            Gets no arrow:

            >>> abjad.NumberedPitch(13).arrow is None
            True

        ..  container:: example

            Gets up-arrow:

            >>> abjad.NumberedPitch(13, arrow=abjad.Up).arrow
            Up

        ..  container:: example

            Gets down-arrow:

            >>> abjad.NumberedPitch(13, arrow=abjad.Down).arrow
            Down

        Returns up, down or none.
        """
        return self._pitch_class.arrow

    @property
    def hertz(self):
        """
        Gets frequency of numbered pitch in Hertz.

        ..  container:: example

            >>> abjad.NumberedPitch(9).hertz
            440.0

            >>> abjad.NumberedPitch(0).hertz
            261.62...

            >>> abjad.NumberedPitch(12).hertz
            523.25...

        Returns float.
        """
        return super().hertz

    @property
    def name(self):
        """
        Gets name of numbered pitch.

        ..  container:: example

            >>> abjad.NumberedPitch(13).name
            "cs''"

        Returns string
        """
        return f"{self.pitch_class.name}{self.octave.ticks}"

    @property
    def number(self):
        """
        Gets number of numbered pitch.

        ..  container:: example

            >>> abjad.NumberedPitch(13).number
            13

        Returns number.
        """
        pc_number = float(self.pitch_class)
        octave_base_pitch = (self.octave.number - 4) * 12
        return _math.integer_equivalent_number_to_integer(pc_number + octave_base_pitch)

    @property
    def octave(self):
        """
        Gets octave of numbered pitch.

        ..  container:: example

            >>> abjad.NumberedPitch(13).octave
            Octave(5)

        Returns octave.
        """
        return self._octave

    @property
    def pitch_class(self):
        """
        Gets pitch-class of numbered pitch.

        ..  container:: example

            >>> abjad.NumberedPitch(13).pitch_class
            NumberedPitchClass(1)

        Returns numbered pitch-class.
        """
        return self._pitch_class

    ### PUBLIC METHODS ###

    @classmethod
    def from_hertz(class_, hertz):
        """
        Makes numbered pitch from ``hertz``.

        ..  container:: example

            >>> abjad.NumberedPitch.from_hertz(440)
            NumberedPitch(9)

        ..  container:: example

            REGRESSION. Returns 12 (not 0):

            >>> abjad.NumberedPitch.from_hertz(519)
            NumberedPitch(12)

        Returns newly constructed numbered pitch.
        """
        return super().from_hertz(hertz)

    def get_name(self, locale=None):
        """
        Gets name of numbered pitch name according to ``locale``.

        ..  container:: example

            >>> abjad.NumberedPitch(13).get_name()
            "cs''"

            >>> abjad.NumberedPitch(13).get_name(locale='us')
            'C#5'

        Set ``locale`` to ``'us'`` or none.

        Returns string.
        """
        return NamedPitch(self).get_name(locale=locale)

    def interpolate(self, stop_pitch, fraction):
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

        ..  container:: example

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

        Returns new numbered pitch.
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

    def invert(self, axis=None):
        """
        Inverts numbered pitch around ``axis``.

        ..  container:: example

            Inverts pitch-class about pitch-class 0 explicitly:

            >>> abjad.NumberedPitch(2).invert(0)
            NumberedPitch(-2)

            >>> abjad.NumberedPitch(-2).invert(0)
            NumberedPitch(2)

        ..  container:: example

            Inverts pitch-class about pitch-class 0 implicitly:

            >>> abjad.NumberedPitch(2).invert()
            NumberedPitch(-2)

            >>> abjad.NumberedPitch(-2).invert()
            NumberedPitch(2)

        ..  container:: example

            Inverts pitch-class about pitch-class -3:

            >>> abjad.NumberedPitch(2).invert(-3)
            NumberedPitch(-8)

        Returns new numbered pitch.
        """
        return Pitch.invert(self, axis=axis)

    def multiply(self, n=1):
        """
        Multiplies numbered pitch by index ``n``.

        ..  container:: example

            >>> abjad.NumberedPitch(14).multiply(3)
            NumberedPitch(42)

        Returns new numbered pitch.
        """
        return super().multiply(n=n)

    def transpose(self, n=0):
        """
        Tranposes numbered pitch by ``n`` semitones.

        ..  container:: example

            >>> abjad.NumberedPitch(13).transpose(1)
            NumberedPitch(14)

        Returns new numbered pitch.
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

            >>> string = abjad.storage(pitch_range)
            >>> print(string)
            abjad.PitchRange('[C3, C7]')

    ..  container:: example

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

    Initalizes from pitch numbers, pitch names, pitch instances,
    one-line reprs or other pitch range objects.

    Pitch ranges do not sort relative to other pitch ranges.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_start", "_stop")

    ### INITIALIZER ###

    def __init__(self, range_string="[A0, C8]"):
        if isinstance(range_string, type(self)):
            range_string = range_string.range_string
        start, stop = self._parse_range_string(range_string)
        self._start = start
        self._stop = stop

    ### SPECIAL METHODS ###

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
        if isinstance(argument, (int, float)):
            pitch = NamedPitch(argument)
            return self._contains_pitch(pitch)
        if isinstance(argument, Pitch):
            return self._contains_pitch(argument)
        raise Exception(f"must be pitch or number {argument!r}.")

    def __eq__(self, argument):
        """
        Delegates to ``abjad.format.compare_objects()``.

        ..  container:: example

            >>> range_1 = abjad.PitchRange.from_pitches(-39, 0)
            >>> range_2 = abjad.PitchRange.from_pitches(-39, 0)
            >>> range_3 = abjad.PitchRange.from_pitches(-39, 48)

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

        Returns true or false.
        """
        return _format.compare_objects(self, argument)

    def __hash__(self):
        """
        Hashes pitch range.

        Returns integer.
        """
        return hash(self.__class__.__name__ + str(self))

    def __lt__(self, argument):
        """
        Is true when start pitch of this pitch-range is less than start
        pitch of ``argument`` pitch range.

        ..  container:: example

            >>> range_1 = abjad.PitchRange.from_pitches(-39, 0)
            >>> range_2 = abjad.PitchRange.from_pitches(-39, 0)
            >>> range_3 = abjad.PitchRange.from_pitches(-39, 48)

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

        Returns true or false.
        """
        try:
            argument = type(self)(argument)
        except (TypeError, ValueError):
            return False
        if self.start_pitch == argument.start_pitch:
            return self.stop_pitch < argument.stop_pitch
        return self.start_pitch < argument.start_pitch

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return _format.get_repr(self)

    ### PRIVATE PROPERTIES ###

    @property
    def _close_bracket_string(self):
        if self.stop_pitch_is_included_in_range:
            return "]"
        else:
            return ")"

    @property
    def _open_bracket_string(self):
        if self.start_pitch_is_included_in_range:
            return "["
        else:
            return "("

    ### PRIVATE METHODS ###

    def _contains_pitch(self, pitch):
        if isinstance(pitch, numbers.Number):
            pitch = NamedPitch(pitch)
        elif isinstance(pitch, str):
            pitch = NamedPitch(pitch)
        if self.start_pitch is None and self.stop_pitch is None:
            return True
        elif self.start_pitch is None:
            if self.stop_pitch_is_included_in_range:
                return pitch <= self.stop_pitch
            else:
                return pitch < self.stop_pitch
        elif self.stop_pitch is None:
            if self.start_pitch_is_included_in_range:
                return self.start_pitch <= pitch
            else:
                return self.start_pitch < pitch
        else:
            if self.start_pitch_is_included_in_range:
                if self.stop_pitch_is_included_in_range:
                    return self.start_pitch <= pitch <= self.stop_pitch
                else:
                    return self.start_pitch <= pitch < self.stop_pitch
            else:
                if self.stop_pitch_is_included_in_range:
                    return self.start_pitch < pitch <= self.stop_pitch
                else:
                    return self.start_pitch < pitch < self.stop_pitch

    def _get_format_specification(self):
        return _format.FormatSpecification(
            coerce_for_equality=True,
            storage_format_args_values=[self.range_string],
            storage_format_is_not_indented=True,
        )

    def _get_named_range_string(self):
        result = []
        result.append(self._open_bracket_string)
        if self.start_pitch:
            result.append(self.start_pitch.get_name(locale="us"))
        else:
            result.append("-inf")
        result.append(", ")
        if self.stop_pitch:
            result.append(self.stop_pitch.get_name(locale="us"))
        else:
            result.append("+inf")
        result.append(self._close_bracket_string)
        result = "".join(result)
        return result

    def _get_numbered_range_string(self):
        result = []
        result.append(self._open_bracket_string)
        result.append(str(self.start_pitch.number))
        result.append(", ")
        result.append(str(self.stop_pitch.number))
        result.append(self._close_bracket_string)
        result = "".join(result)
        return result

    def _parse_range_string(self, range_string):
        assert isinstance(range_string, str), repr(range_string)
        range_string = range_string.replace("-inf", "-1000")
        range_string = range_string.replace("+inf", "1000")
        match = _range_string_regex.match(range_string)
        if match is None:
            raise ValueError(f"can not instantiate pitch range: {range_string!r}")
        group_dict = match.groupdict()
        start_punctuation = group_dict["open_bracket"]
        start_pitch_string = group_dict["start_pitch"]
        stop_pitch_string = group_dict["stop_pitch"]
        stop_punctuation = group_dict["close_bracket"]
        start_inclusivity_string = _start_punctuation_to_inclusivity_string[
            start_punctuation
        ]
        stop_inclusivity_string = _stop_punctuation_to_inclusivity_string[
            stop_punctuation
        ]
        if start_pitch_string == "-1000":
            start_pitch = None
        else:
            try:
                start_pitch = NamedPitch(start_pitch_string)
            except (TypeError, ValueError):
                start_pitch = NumberedPitch(int(start_pitch_string))
        if stop_pitch_string == "1000":
            stop_pitch = None
        else:
            try:
                stop_pitch = NamedPitch(stop_pitch_string)
            except (TypeError, ValueError):
                stop_pitch = NumberedPitch(int(stop_pitch_string))
        start_pair = (start_pitch, start_inclusivity_string)
        stop_pair = (stop_pitch, stop_inclusivity_string)
        return start_pair, stop_pair

    ### PUBLIC PROPERTIES ###

    @property
    def range_string(self) -> str:
        """
        Gets range string of pitch range.

        ..  container:: example

            >>> pitch_range = abjad.PitchRange("[C3, C7]")
            >>> pitch_range.range_string
            '[C3, C7]'

        """
        return self._get_named_range_string()

    @property
    def start_pitch(self) -> typing.Optional[NamedPitch]:
        """
        Start pitch of pitch range.

        ..  container:: example

            >>> pitch_range = abjad.PitchRange("[C3, C7]")
            >>> pitch_range.start_pitch
            NamedPitch('c')

        """
        if self._start is None:
            return None
        return self._start[0]

    @property
    def start_pitch_is_included_in_range(self) -> bool:
        """
        Is true when start pitch is included in range.

        ..  container:: example

            >>> pitch_range = abjad.PitchRange("[C3, C7]")
            >>> pitch_range.start_pitch_is_included_in_range
            True

        """
        if self._start is None:
            return True
        return self._start[1] == "inclusive"

    @property
    def stop_pitch(self) -> typing.Optional[NamedPitch]:
        """
        Stop pitch of pitch range.

        ..  container:: example

            >>> pitch_range = abjad.PitchRange("[C3, C7]")
            >>> pitch_range.stop_pitch
            NamedPitch("c''''")

        """
        if self._stop is None:
            return None
        return self._stop[0]

    @property
    def stop_pitch_is_included_in_range(self) -> bool:
        """
        Is true when stop pitch is included in range.

        ..  container:: example

            >>> pitch_range = abjad.PitchRange("[C3, C7]")
            >>> pitch_range.stop_pitch_is_included_in_range
            True

        """
        if self._stop is None:
            return True
        return self._stop[1] == "inclusive"

    ### PUBLIC METHODS ###

    @staticmethod
    def from_octave(octave) -> "PitchRange":
        """
        Initializes pitch range from octave.

        ..  container:: example

            >>> abjad.PitchRange.from_octave(5)
            PitchRange('[C5, C6)')

        """
        octave = Octave(octave)
        return PitchRange(f"[C{octave.number}, C{octave.number + 1})")

    @staticmethod
    def from_pitches(
        start_pitch,
        stop_pitch,
        start_pitch_is_included_in_range=True,
        stop_pitch_is_included_in_range=True,
    ) -> "PitchRange":
        """
        Initializes pitch range from numbers.

        ..  container:: example

            >>> abjad.PitchRange.from_pitches(-18, 19)
            PitchRange('[F#2, G5]')

        """
        if start_pitch is None:
            start_pitch_string = "-inf"
        else:
            start_pitch_string = str(NamedPitch(start_pitch))
        if stop_pitch is None:
            stop_pitch_string = "+inf"
        else:
            stop_pitch_string = str(NamedPitch(stop_pitch))
        start_containment = "["
        if not start_pitch_is_included_in_range:
            start_containment = "("
        stop_containment = "]"
        if not stop_pitch_is_included_in_range:
            stop_containment = ")"
        string = "{}{}, {}{}"
        string = string.format(
            start_containment,
            start_pitch_string,
            stop_pitch_string,
            stop_containment,
        )
        pitch_range = PitchRange(string)
        return pitch_range

    @classmethod
    def is_range_string(class_, argument) -> bool:
        """Is true when ``argument`` is a pitch range string.

        ..  container:: example

            >>> abjad.PitchRange.is_range_string("[A0, C8]")
            True

            >>> abjad.PitchRange.is_range_string("[A#0, Cb~8]")
            True

            >>> abjad.PitchRange.is_range_string("[A#+0, cs'')")
            True

            >>> abjad.PitchRange.is_range_string("(b,,,, ctqs]")
            True

        ..  container:: example

            >>> abjad.PitchRange.is_range_string("text")
            False

        The regex that underlies this predicate matches against two
        comma-separated pitches enclosed in some combination of square
        brackets and round parentheses.
        """
        if not isinstance(argument, str):
            return False
        return bool(_range_string_regex.match(argument))

    def voice_pitch_class(self, pitch_class):
        """
        Voices ``pitch_class``:

        ..  container:: example

            Voices C three times:

            >>> pitch_range = abjad.PitchRange("[C4, C6]")
            >>> pitch_range.voice_pitch_class("c")
            (NamedPitch("c'"), NamedPitch("c''"), NamedPitch("c'''"))

        ..  container:: example

            Voices B two times:

            >>> pitch_range = abjad.PitchRange("[C4, C6]")
            >>> pitch_range.voice_pitch_class("b")
            (NamedPitch("b'"), NamedPitch("b''"))

        ..  container:: example

            Returns empty because B can not voice:

            >>> pitch_range = abjad.PitchRange("[C4, A4)")
            >>> pitch_range.voice_pitch_class('b')
            ()

        """
        named_pitch_class = NamedPitchClass(pitch_class)
        assert self.start_pitch is not None
        assert self.stop_pitch is not None
        pair = (named_pitch_class.name, self.start_pitch.octave.number)
        named_pitch = NamedPitch(pair)
        result = []
        while named_pitch <= self.stop_pitch:
            if named_pitch in self:
                result.append(named_pitch)
            named_pitch += 12
        return tuple(result)


class Segment(_typedcollections.TypedTuple):
    """
    Abstract segment.
    """

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, items=None, item_class=None):
        prototype = (collections.abc.Iterator, types.GeneratorType)
        if isinstance(items, str):
            items = items.split()
        elif isinstance(items, prototype):
            items = [_ for _ in items]
        if item_class is None:
            item_class = self._named_item_class
            if items is not None:
                if isinstance(items, _typedcollections.TypedCollection) and issubclass(
                    items.item_class, self._parent_item_class
                ):
                    item_class = items.item_class
                elif len(items):
                    if isinstance(items, collections.abc.Set):
                        items = tuple(items)
                    if isinstance(items[0], str):
                        item_class = self._named_item_class
                    elif isinstance(items[0], (int, float)):
                        item_class = self._numbered_item_class
                    elif isinstance(items[0], self._parent_item_class):
                        item_class = type(items[0])
        if isinstance(item_class, str):
            abjad = importlib.import_module("abjad")
            globals_ = {"abjad": abjad}
            globals_.update(abjad.__dict__.copy())
            item_class = eval(item_class, globals_)
        assert issubclass(item_class, self._parent_item_class)
        _typedcollections.TypedTuple.__init__(self, items=items, item_class=item_class)

    ### SPECIAL METHODS ###

    def __str__(self) -> str:
        """
        Gets string representation of segment.
        """
        items = [str(_) for _ in self]
        string = ", ".join(items)
        return f"<{string}>"

    ### PRIVATE PROPERTIES ###

    @abc.abstractproperty
    def _named_item_class(self):
        raise NotImplementedError

    @abc.abstractproperty
    def _numbered_item_class(self):
        raise NotImplementedError

    @abc.abstractproperty
    def _parent_item_class(self):
        raise NotImplementedError

    ### PRIVATE METHODS ###

    def _coerce_item(self, item):
        return self._item_class(item)

    def _get_format_specification(self):
        items = []
        if self.item_class.__name__.startswith("Named"):
            items = [str(x) for x in self]
        elif hasattr(self.item_class, "pitch_number"):
            items = [x.pitch_number for x in self]
        elif hasattr(self.item_class, "pitch_class_number"):
            items = [x.pitch_class_number for x in self]
        elif self.item_class.__name__.startswith("Numbered"):
            items = [
                _math.integer_equivalent_number_to_integer(float(x.number))
                for x in self
            ]
        elif hasattr(self.item_class, "__abs__"):
            items = [abs(x) for x in self]
        else:
            raise ValueError(f"invalid item class: {self.item_class!r}.")
        return _format.FormatSpecification(
            repr_keyword_names=["name"],
            repr_args_values=[items],
            storage_format_args_values=[tuple(self._collection)],
        )

    def _get_padded_string(self, width=2):
        strings = []
        for item in self:
            string = f"{item!s:>{width}}"
            strings.append(string)
        string = ", ".join(strings)
        return f"<{string}>"

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def from_selection(class_, selection, item_class=None):
        """
        Makes segment from ``selection``.

        Returns new segment.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def has_duplicates(self):
        """
        Is true when segment has duplicates.

        Returns true or false.
        """
        raise NotImplementedError


class IntervalClassSegment(Segment):
    """
    Interval-class segment.

    ..  container:: example

        An interval-class segment:

        >>> intervals = 'm2 M10 -aug4 P5'
        >>> abjad.IntervalClassSegment(intervals)
        IntervalClassSegment(['+m2', '+M3', '-A4', '+P5'])

    ..  container:: example

        Another interval-class segment:

        >>> intervals = 'P4 P5 P11 P12'
        >>> abjad.IntervalClassSegment(intervals)
        IntervalClassSegment(['+P4', '+P5', '+P4', '+P5'])

    Returns interval-class segment.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### PRIVATE PROPERTIES ###

    @property
    def _named_item_class(self):
        return NamedIntervalClass

    @property
    def _numbered_item_class(self):
        return NumberedIntervalClass

    @property
    def _parent_item_class(self):
        return IntervalClass

    ### PUBLIC PROPERTIES ###

    @property
    def is_tertian(self):
        """
        Is true when all named interval-classes in segment are tertian.

        ..  container:: example

            >>> interval_class_segment = abjad.IntervalClassSegment(
            ...     items=[('major', 3), ('minor', 6), ('major', 6)],
            ...     item_class=abjad.NamedIntervalClass,
            ...     )
            >>> interval_class_segment.is_tertian
            True

        Returns true or false.
        """
        inversion_equivalent_interval_class_segment = _new.new(
            self, item_class=NamedInversionEquivalentIntervalClass
        )
        for interval in inversion_equivalent_interval_class_segment:
            if not interval.number == 3:
                return False
        return True

    ### PUBLIC METHODS ###

    @classmethod
    def from_selection(class_, selection, item_class=None):
        """
        Initializes interval-class segment from component selection.

        ..  container:: example

            >>> staff_1 = abjad.Staff("c'4 <d' fs' a'>4 b2")
            >>> staff_2 = abjad.Staff("c4. r8 g2")
            >>> selection = abjad.select((staff_1, staff_2))
            >>> abjad.IntervalClassSegment.from_selection(selection)
            IntervalClassSegment(['-M2', '-M3', '-m3', '+m7', '+M7', '-P5'])

        Returns interval-class segment.
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


class IntervalSegment(Segment):
    """
    Interval segment.

    ..  container:: example

        Initializes from string:

        >>> intervals = 'm2 M10 -aug4 P5'
        >>> abjad.IntervalSegment(intervals)
        IntervalSegment(['+m2', '+M10', '-A4', '+P5'])

    ..  container:: example

        Initializes from pitch segment:

        >>> pitch_segment = abjad.PitchSegment("c d e f g a b c'")
        >>> abjad.IntervalSegment(pitch_segment)
        IntervalSegment(['+M2', '+M2', '+m2', '+M2', '+M2', '+M2', '+m2'])

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, items=None, item_class=None):
        if isinstance(items, PitchSegment):
            intervals = []
            for one, two in _sequence.Sequence(items).nwise():
                intervals.append(one - two)
            items = intervals
        Segment.__init__(self, items=items, item_class=item_class)

    ### PRIVATE PROPERTIES ###

    @property
    def _named_item_class(self):
        return NamedInterval

    @property
    def _numbered_item_class(self):
        return NumberedInterval

    @property
    def _parent_item_class(self):
        return Interval

    ### PUBLIC PROPERTIES ###

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

    ### PUBLIC METHODS ###

    @classmethod
    def from_selection(class_, selection, item_class=None):
        """
        Makes interval segment from component ``selection``.

        ..  container:: example

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
            >>> abjad.IntervalSegment.from_selection(
            ...     abjad.select(staff),
            ...     item_class=abjad.NumberedInterval,
            ...     )
            IntervalSegment([2, 2, 1, 2, 2, 2, 1])

        Returns interval segment.
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
        return _new.new(self, self[-n:] + self[:-n])


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

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, items=None, item_class=None):
        if not items and not item_class:
            item_class = self._named_item_class
        Segment.__init__(self, items=items, item_class=item_class)

    ### SPECIAL METHODS ###

    def __add__(self, argument):
        r"""
        Adds ``argument`` to segment.

        ..  container:: example

            Example segments:

            >>> pitch_numbers = [-2, -1.5, 6, 7, -1.5, 7]
            >>> abjad.PitchClassSegment(items=pitch_numbers)
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

            >>> J = abjad.PitchClassSegment(items=pitch_numbers)
            >>> lilypond_file = abjad.illustrate(J)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> pitch_names = ['c', 'ef', 'bqs,', 'd']
            >>> abjad.PitchClassSegment(items=pitch_names)
            PitchClassSegment("c ef bqs d")

            >>> K = abjad.PitchClassSegment(items=pitch_names)
            >>> lilypond_file = abjad.illustrate(K)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Adds J and K:

            >>> J + K
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7, 0, 3, 11.5, 2])

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
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7, 10, 10.5, 6, 7, 10.5, 7, 10, 10.5, 6, 7, 10.5, 7])


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
            PitchClassSegment([7, 10, 10.5, 6, 7, 10.5, 11.5, 2, 0, 3])

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
            PitchClassSegment([3, 0, 2, 11.5, 10.5, 7, 6, 10.5, 10, 7])

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

        Returns new segment.
        """
        argument = type(self)(items=argument)
        items = self.items + argument.items
        return type(self)(items=items)

    def __contains__(self, argument):
        r"""
        Is true when pitch-class segment contains ``argument``.

        ..  container:: example

            Example segments:

            >>> pitch_numbers = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(items=pitch_numbers)
            >>> segment
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

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
        return super().__contains__(argument)

    def __getitem__(self, argument):
        r"""
        Gets ``argument`` from segment.

        ..  container:: example

            Example segment:

            >>> pitch_numbers = [-2, -1.5, 6, 7, -1.5, 7]
            >>> abjad.PitchClassSegment(items=pitch_numbers)
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

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
            PitchClassSegment([10, 10.5, 6, 7])

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
            PitchClassSegment([7, 6, 10.5, 10])

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
            PitchClassSegment([7, 10.5, 7, 6])

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
        return super().__getitem__(argument)

    def __mul__(self, n):
        r"""
        Multiplies pitch-class segment by ``n``.

        ..  container:: example

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> 2 * abjad.PitchClassSegment(items=items)
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7, 10, 10.5, 6, 7, 10.5, 7])

        Returns new pitch-class segment.
        """
        return super().__mul__(n)

    def __repr__(self):
        r"""
        Gets interpreter representation.

        ..  container:: example

            Interpreter representation:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> abjad.PitchClassSegment(items=items)
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

        Returns string.
        """
        if self.item_class is NamedPitchClass:
            contents = " ".join([str(_) for _ in self])
            contents = '"' + contents + '"'
        else:
            contents = ", ".join([str(_) for _ in self])
            contents = "[" + contents + "]"
        return f"{type(self).__name__}({contents})"

    def __rmul__(self, n):
        r"""
        Multiplies ``n`` by pitch-class segment.

        ..  container:: example

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> abjad.PitchClassSegment(items=items) * 2
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7, 10, 10.5, 6, 7, 10.5, 7])

        Returns new pitch-class segment.
        """
        return super().__rmul__(n)

    def __str__(self):
        r"""
        Gets string representation of pitch-class segment.

        ..  container::

            Gets string represenation of numbered pitch class:

            >>> segment = abjad.PitchClassSegment([-2, -1.5, 6, 7, -1.5, 7])
            >>> str(segment)
            'PC<10, 10.5, 6, 7, 10.5, 7>'

        ..  container::

            Gets string represenation of named pitch class:

            >>> segment = abjad.PitchClassSegment(
            ...     items=[-2, -1.5, 6, 7, -1.5, 7],
            ...     item_class=abjad.NamedPitchClass,
            ...     )
            >>> str(segment)
            'PC<bf bqf fs g bqf g>'

        Returns string.
        """
        items = [str(_) for _ in self]
        separator = " "
        if self.item_class is NumberedPitchClass:
            separator = ", "
        return f"PC<{separator.join(items)}>"

    ### PRIVATE PROPERTIES ###

    @property
    def _named_item_class(self):
        return NamedPitchClass

    @property
    def _numbered_item_class(self):
        return NumberedPitchClass

    @property
    def _parent_item_class(self):
        return PitchClass

    ### PRIVATE METHODS ###

    def _get_padded_string(self, width=2):
        string = super()._get_padded_string(width=width)
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
        new_pitch_classes = _new.new(self, items=new_pitch_classes)
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

    ### PUBLIC PROPERTIES ###

    @property
    def item_class(self):
        r"""
        Gets item class of segment.

        ..  container:: example

            Gets item class of numbered segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> segment.item_class.__name__
            'NumberedPitchClass'

        ..  container:: example

            Gets item class of named segment:

            >>> items = ['c', 'ef', 'bqs,', 'd']
            >>> segment = abjad.PitchClassSegment(
            ...     items=items,
            ...     item_class=abjad.NamedPitchClass,
            ...     )
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> segment.item_class.__name__
            'NamedPitchClass'

        """
        return super().item_class

    @property
    def items(self):
        r"""
        Gets items in segment.

        ..  container:: example

            Initializes items positionally:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(items)
            >>> for item in segment.items:
            ...     item
            ...
            NumberedPitchClass(10)
            NumberedPitchClass(10.5)
            NumberedPitchClass(6)
            NumberedPitchClass(7)
            NumberedPitchClass(10.5)
            NumberedPitchClass(7)

            Initializes items from keyword:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> for item in segment.items:
            ...     item
            NumberedPitchClass(10)
            NumberedPitchClass(10.5)
            NumberedPitchClass(6)
            NumberedPitchClass(7)
            NumberedPitchClass(10.5)
            NumberedPitchClass(7)

        ..  container:: example

            Returns list:

            >>> isinstance(segment.items, list)
            True

        """
        return super().items

    ### PUBLIC METHODS ###

    def count(self, item):
        """
        Counts ``item`` in segment.

        ..  container:: example

            Example segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Counts existing item in segment:

            >>> segment.count(-1.5)
            2

        ..  container:: example

            Counts nonexisting item in segment:

            >>> segment.count('text')
            0

        ..  container:: example

            Returns nonnegative integer:

            >>> isinstance(segment.count('text'), int)
            True

        """
        return super().count(item)

    @classmethod
    def from_selection(class_, selection, item_class=None):
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

        ..  container:: example

            Returns pitch-class segment:

            >>> segment
            PitchClassSegment("c d fs a b c g")

        """
        pitch_segment = PitchSegment.from_selection(selection)
        return class_(items=pitch_segment, item_class=item_class)

    def has_duplicates(self):
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

        ..  container:: example

            Has no duplicates:

            >>> items = "c d e f g a b"
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> segment.has_duplicates()
            False

        Returns true or false.
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

        ..  container:: example

            Gets index of first item in segment:

            >>> segment.index(-2)
            0

        ..  container:: example

            Gets index of second item in segment:

            >>> segment.index(-1.5)
            1

        ..  container:: example

            Returns nonnegative integer:

            >>> isinstance(segment.index(-1.5), int)
            True

        """
        return super().index(item)

    def invert(self, axis=None):
        r"""
        Inverts segment.

        ..  container:: example

            Example segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> J = abjad.PitchClassSegment(items=items)
            >>> J
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

            >>> lilypond_file = abjad.illustrate(J)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Inverts segment:

            >>> J.invert()
            PitchClassSegment([2, 1.5, 6, 5, 1.5, 5])

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

        ..  container:: example

            Inverts inversion of segment:

            >>> J.invert().invert()
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

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

        ..  container:: example

            Returns pitch-class segment:

            >>> isinstance(segment, abjad.PitchClassSegment)
            True

        """
        items = [_.invert(axis=axis) for _ in self]
        return type(self)(items=items)

    def multiply(self, n=1):
        r"""
        Multiplies pitch-classes in segment by ``n``.

        ..  container:: example

            Example segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> J = abjad.PitchClassSegment(items=items)
            >>> J
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

            >>> lilypond_file = abjad.illustrate(J)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Multiplies pitch-classes in segment by 1:

            >>> J.multiply(n=1)
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

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

        ..  container:: example

            Multiplies pitch-classes in segment by 5:

            >>> J.multiply(n=5)
            PitchClassSegment([2, 4.5, 6, 11, 4.5, 11])

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

        ..  container:: example

            Multiplies pitch-classes in segment by 7:

            >>> J.multiply(n=7)
            PitchClassSegment([10, 1.5, 6, 1, 1.5, 1])

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

        ..  container:: example

            Multiplies pitch-classes in segment by 11:

            >>> segment = J.multiply(n=11)
            >>> segment
            PitchClassSegment([2, 7.5, 6, 5, 7.5, 5])

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

        ..  container:: example

            Returns pitch-class segment:

            >>> isinstance(segment, abjad.PitchClassSegment)
            True

        """
        items = [NumberedPitchClass(_) for _ in self]
        items = [_.multiply(n) for _ in items]
        return type(self)(items=items)

    def permute(self, row=None):
        r"""
        Permutes segment by twelve-tone ``row``.

        ..  container:: example

            >>> abjad.PitchClassSegment([-2, -1, 6, 7, -1, 7])
            PitchClassSegment([10, 11, 6, 7, 11, 7])

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
            PitchClassSegment([4, 11, 5, 3, 11, 3])

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

        Returns new segment.
        """
        row = TwelveToneRow(items=row)
        items = row(self)
        return type(self)(items=items)

    def retrograde(self):
        r"""
        Gets retrograde of segment.

        ..  container:: example

            Example segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> J = abjad.PitchClassSegment(items=items)
            >>> J
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

            >>> lilypond_file = abjad.illustrate(J)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Gets retrograde of segment:

            >>> segment = J.retrograde()
            >>> segment
            PitchClassSegment([7, 10.5, 7, 6, 10.5, 10])

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

        ..  container:: example

            Gets retrograde of retrograde of segment:

            >>> segment = J.retrograde().retrograde()
            >>> segment
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

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

        ..  container:: example

            Returns pitch-class segment:

            >>> isinstance(segment, abjad.PitchClassSegment)
            True

        """
        return type(self)(items=reversed(self))

    def rotate(self, n=0):
        r"""
        Rotates segment by index ``n``.

        ..  container:: example

            Example segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> J = abjad.PitchClassSegment(items=items)
            >>> J
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

            >>> lilypond_file = abjad.illustrate(J)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Rotates segment to the right:

            >>> J.rotate(n=1)
            PitchClassSegment([7, 10, 10.5, 6, 7, 10.5])

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

        ..  container:: example

            Rotates segment to the left:

            >>> J.rotate(n=-1)
            PitchClassSegment([10.5, 6, 7, 10.5, 7, 10])

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

        ..  container:: example

            Rotates segment by zero:

            >>> J.rotate(n=0)
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

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

        ..  container:: example

            Returns pitch-class segment:

            >>> isinstance(segment, abjad.PitchClassSegment)
            True

        """
        items = _sequence.Sequence(self._collection).rotate(n=n)
        return type(self)(items=items)

    def to_pitch_classes(self):
        r"""
        Changes to pitch-classes.

        ..  container:: example

            To numbered pitch-class segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> segment
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

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
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

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
            PitchClassSegment("bf bqf fs g bqf g")

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
            PitchClassSegment("bf bqf fs g bqf g")

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
        return _new.new(self)

    def to_pitches(self):
        r"""
        Changes to pitches.

        ..  container:: example

            To numbered pitch segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> segment
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

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
            PitchSegment([10, 10.5, 6, 7, 10.5, 7])

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
            PitchClassSegment("bf bqf fs g bqf g")

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
            PitchSegment("bf' bqf' fs' g' bqf' g'")

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

        Returns new segment.
        """
        class_ = Pitch
        item_class = class_._to_pitch_item_class(self.item_class)
        return PitchSegment(items=self.items, item_class=item_class)

    def transpose(self, n=0):
        r"""
        Transposes segment by index ``n``.

        ..  container:: example

            Example segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> J = abjad.PitchClassSegment(items=items)
            >>> J
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

            >>> lilypond_file = abjad.illustrate(J)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Transposes segment by positive index:

            >>> J.transpose(n=13)
            PitchClassSegment([11, 11.5, 7, 8, 11.5, 8])

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
            PitchClassSegment([9, 9.5, 5, 6, 9.5, 6])

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
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

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

        ..  container:: example

            Returns pitch-class segment:

            >>> isinstance(segment, abjad.PitchClassSegment)
            True

        """
        items = [_.transpose(n=n) for _ in self]
        return type(self)(items=items)

    def voice_horizontally(self, initial_octave=4):
        r"""
        Voices segment with each pitch as close to the previous pitch as
        possible.

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

        ..  container:: example

            Returns pitch segment:

            >>> voiced_segment
            PitchSegment("c' b d' e' f' g' e' b a c'")

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
                semitones = abs((pitch - pitches[-1]).semitones)
                while 6 < semitones:
                    if pitch < pitches[-1]:
                        pitch += 12
                    else:
                        pitch -= 12
                    semitones = abs((pitch - pitches[-1]).semitones)
                pitches.append(pitch)
        if self.item_class is NamedPitchClass:
            item_class = NamedPitch
        else:
            item_class = NumberedPitch
        return PitchSegment(items=pitches, item_class=item_class)

    def voice_vertically(self, initial_octave=4):
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

        ..  container:: example

            Returns pitch segment:

            >>> voiced_segment
            PitchSegment("c' ef' g' bf' d'' f'' af''")

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
            item_class = NamedPitch
        else:
            item_class = NumberedPitch
        return PitchSegment(items=pitches, item_class=item_class)


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

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, items=None, item_class=None):
        if not items and not item_class:
            item_class = self._named_item_class
        Segment.__init__(self, items=items, item_class=item_class)

    ### SPECIAL METHODS ###

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
        return super().__contains__(argument)

    def __repr__(self):
        """
        Gets interpreter representation of segment.

        Returns string.
        """
        if self.item_class is NamedPitch:
            contents = " ".join([str(_) for _ in self])
            contents = '"' + contents + '"'
        else:
            contents = ", ".join([str(_) for _ in self])
            contents = "[" + contents + "]"
        return f"{type(self).__name__}({contents})"

    def __str__(self):
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

        Returns string.
        """
        items = [str(_) for _ in self]
        separator = " "
        if self.item_class is NumberedPitch:
            separator = ", "
        return f"<{separator.join(items)}>"

    ### PRIVATE PROPERTIES ###

    @property
    def _named_item_class(self):
        return NamedPitch

    @property
    def _numbered_item_class(self):
        return NumberedPitch

    @property
    def _parent_item_class(self):
        return Pitch

    ### PRIVATE METHODS ###

    def _is_equivalent_under_transposition(self, argument):
        if not isinstance(argument, type(self)):
            return False
        if not len(self) == len(argument):
            return False
        difference = -(NamedPitch(argument[0], 4) - NamedPitch(self[0], 4))
        new_pitches = (x + difference for x in self)
        new_pitches = _new.new(self, items=new_pitches)
        return argument == new_pitches

    ### PUBLIC PROPERTIES ###

    @property
    def hertz(self):
        """
        Gets Hertz of pitches in segment.

        ..  container:: example

            >>> segment = abjad.PitchSegment('c e g b')
            >>> segment.hertz
            [130.81..., 164.81..., 195.99..., 246.94...]

        Returns list.
        """
        return [_.hertz for _ in self]

    @property
    def inflection_point_count(self):
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

        Returns nonnegative integer.
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

    ### PUBLIC METHODS ###

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

    def invert(self, axis=None):
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

        Returns new pitch segment.
        """
        items = [_.invert(axis=axis) for _ in self]
        return _new.new(self, items=items)

    def multiply(self, n=1):
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

        Returns new pitch segment.
        """
        items = [_.multiply(n=n) for _ in self]
        return _new.new(self, items=items)

    def retrograde(self):
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

        Returns new pitch segment.
        """
        return _new.new(self, items=reversed(self))

    def rotate(self, n=0):
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

        Returns new pitch segment.
        """
        rotated_pitches = _sequence.Sequence(self._collection).rotate(n=n)
        new_segment = _new.new(self, items=rotated_pitches)
        return new_segment

    def to_pitch_classes(self):
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

        Returns new segment.
        """
        class_ = Pitch
        item_class = class_._to_pitch_class_item_class(self.item_class)
        return PitchClassSegment(items=self.items, item_class=item_class)

    def to_pitches(self):
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

        Returns new segment.
        """
        return _new.new(self)

    def transpose(self, n=0):
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

        Returns new pitch segment.
        """
        items = [_.transpose(n=n) for _ in self]
        return _new.new(self, items=items)


class TwelveToneRow(PitchClassSegment):
    """
    Twelve-tone row.

    ..  container:: example

        Initializes from defaults:

        >>> row = abjad.TwelveToneRow()
        >>> lilypond_file = abjad.illustrate(row)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  container:: example

        Initializes from integers:

        >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
        >>> row = abjad.TwelveToneRow(numbers)
        >>> lilypond_file = abjad.illustrate(row)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  container:: example

        Interpreter representation:

        >>> row
        TwelveToneRow([1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0])

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, items=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)):
        assert items is not None
        PitchClassSegment.__init__(self, items=items, item_class=NumberedPitchClass)
        self._validate_pitch_classes(self)

    ### SPECIAL METHODS ###

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

            Returns pitch-class segment:

            >>> row[-6:]
            PitchClassSegment([5, 4, 10, 2, 8, 0])

        """
        item = self._collection.__getitem__(argument)
        try:
            return PitchClassSegment(items=item, item_class=NumberedPitchClass)
        except TypeError:
            return item

    def __mul__(self, argument):
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

        ..  container:: example

            Returns pitch-class segment:

            >>> segment
            PitchClassSegment([1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0, 1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0])

        Returns pitch-class segment.
        """
        return PitchClassSegment(self) * argument

    def __rmul__(self, argument):
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

        ..  container:: example

            Returns pitch-class segment:

            >>> segment
            PitchClassSegment([1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0, 1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0])

        """
        return PitchClassSegment(self) * argument

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_string(self):
        return ", ".join([str(abs(pc)) for pc in self])

    ### PRIVATE METHODS ###

    @staticmethod
    def _validate_pitch_classes(pitch_classes):
        numbers = [pc.number for pc in pitch_classes]
        numbers.sort()
        if not numbers == list(range(12)):
            message = f"must contain all twelve pitch-classes: {pitch_classes!r}."
            raise ValueError(message)

    ### PUBLIC PROPERTIES ###

    @property
    def item_class(self):
        """
        Gets item class of row.

        ..  container:: example

            Gets item class:

            >>> row = abjad.TwelveToneRow()
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> row.item_class.__name__
            'NumberedPitchClass'

        ..  container:: example

            Gets item class:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> row.item_class.__name__
            'NumberedPitchClass'

        """
        return super().item_class

    @property
    def items(self):
        """
        Gets items in row.

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

        ..  container:: example

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

        ..  container:: example

            Returns list:

            >>> isinstance(row.items, list)
            True

        """
        return super().items

    ### PUBLIC METHODS ###

    def count(self, item):
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

        ..  container:: example

            Returns nonnegative integer equal to 0 or 1:

            >>> isinstance(row.count('text'), int)
            True

        """
        return super().count(item)

    @classmethod
    def from_selection(class_, selection, item_class=None):
        """
        Makes row from ``selection``.

        Not yet implemented.

        Returns twelve-tone row.
        """
        raise NotImplementedError

    def has_duplicates(self):
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

        Returns false.
        """
        return super().has_duplicates()

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
        return super().index(item)

    def invert(self, axis=None):
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

        ..  container:: example

            Returns twelve-tone row:

            >>> inversion
            TwelveToneRow([9, 11, 1, 7, 4, 3, 5, 6, 0, 8, 2, 10])

        """
        if axis is None:
            axis = self[0]
        items = [pc.invert(axis=axis) for pc in self]
        return _new.new(self, items=items)

    def multiply(self, n=1):
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

        ..  container:: example

            Returns twelve-tone row:

            >>> multiplication
            TwelveToneRow([1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0])

        """
        return super().multiply(n=n)

    def retrograde(self):
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

        ..  container:: example

            Returns row:

            >>> retrograde
            TwelveToneRow([1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0])

        """
        return super().retrograde()

    def rotate(self, n=0):
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

        ..  container:: example

            Returns row:

            >>> rotation
            TwelveToneRow([1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0])

        """
        return super().rotate(n=n)

    def transpose(self, n=0):
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

        ..  container:: example

            Returns row:

            >>> transposition
            TwelveToneRow([1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0])

        """
        return super().transpose(n=n)


class Set(_typedcollections.TypedFrozenset):
    """
    Abstract set.
    """

    ### INITIALIZER ###

    def __init__(self, items=None, item_class=None):
        if isinstance(items, str):
            items = items.split()
        elif isinstance(items, (collections.abc.Iterator, types.GeneratorType)):
            items = [item for item in items]
        if item_class is None:
            item_class = self._named_item_class
            if items is not None:
                if isinstance(items, _typedcollections.TypedCollection) and issubclass(
                    items.item_class, self._parent_item_class
                ):
                    item_class = items.item_class
                elif len(items):
                    if isinstance(items, collections.abc.Set):
                        items = tuple(items)
                    if isinstance(items[0], str):
                        item_class = self._named_item_class
                    elif isinstance(items[0], (int, float)):
                        item_class = self._numbered_item_class
                    elif isinstance(items[0], self._parent_item_class):
                        item_class = type(items[0])
        assert issubclass(item_class, self._parent_item_class)
        _typedcollections.TypedFrozenset.__init__(
            self, items=items, item_class=item_class
        )

    ### SPECIAL METHODS ###

    def __str__(self):
        """
        Gets string representation.

        Returns string.
        """
        items = self._get_sorted_repr_items()
        items = [str(_) for _ in items]
        string = ", ".join(items)
        return f"{{{string}}}"

    ### PRIVATE PROPERTIES ###

    @abc.abstractproperty
    def _named_item_class(self):
        raise NotImplementedError

    @abc.abstractproperty
    def _numbered_item_class(self):
        raise NotImplementedError

    @abc.abstractproperty
    def _parent_item_class(self):
        raise NotImplementedError

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        repr_items = self._get_sorted_repr_items()
        return _format.FormatSpecification(
            repr_args_values=[repr_items],
            storage_format_args_values=[repr_items],
            storage_format_keyword_names=[],
        )

    def _get_sorted_repr_items(self):
        items = sorted(self, key=lambda x: (float(x.number), str(x)))
        if self.item_class.__name__.startswith("Named"):
            repr_items = [str(x) for x in items]
        elif hasattr(self.item_class, "number"):
            repr_items = [x.number for x in items]
        elif hasattr(self.item_class, "pitch_class_number"):
            repr_items = [x.pitch_class_number for x in items]
        elif hasattr(self.item_class, "__abs__"):
            repr_items = [abs(x) for x in items]
        else:
            raise ValueError(f"invalid item class: {self.item_class!r}.")
        return repr_items

    def _sort_self(self):
        return tuple(self)

    ### PUBLIC PROPERTIES ###

    @property
    def cardinality(self):
        """
        Gets cardinality of set.

        Defined equal to length of set.

        Returns nonnegative integer.
        """
        return len(self)

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def from_selection(class_, selection, item_class=None):
        """
        Makes set from ``selection``.

        Returns set.
        """
        raise NotImplementedError


class IntervalClassSet(Set):
    """
    Interval-class set.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, items=None, item_class=None):
        prototype = (
            PitchClassSegment,
            PitchSegment,
            PitchClassSet,
            PitchSet,
        )
        if isinstance(items, prototype):
            items = list(items)
            pairs = _enumerate.yield_pairs(items)
            items = [second - first for first, second in pairs]
        super().__init__(items=items, item_class=item_class)

    ### PRIVATE PROPERTIES ###

    @property
    def _named_item_class(self):
        return NamedIntervalClass

    @property
    def _numbered_item_class(self):
        return NumberedIntervalClass

    @property
    def _parent_item_class(self):
        return IntervalClass

    ### PUBLIC METHODS ###

    @classmethod
    def from_selection(class_, selection, item_class=None):
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

        Returns interval set.
        """
        interval_set = IntervalSet.from_selection(selection)
        return class_(items=interval_set, item_class=item_class)


class IntervalSet(Set):
    """
    Interval set.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, items=None, item_class=None):
        prototype = (
            PitchClassSegment,
            PitchClassSet,
            PitchSegment,
            PitchSet,
        )
        if isinstance(items, prototype):
            items = list(items)
            pairs = _enumerate.yield_pairs(items)
            items = [second - first for first, second in pairs]
        super().__init__(items=items, item_class=item_class)

    ### PRIVATE PROPERTIES ###

    @property
    def _named_item_class(self):
        return NamedInterval

    @property
    def _numbered_item_class(self):
        return NumberedInterval

    @property
    def _parent_item_class(self):
        return Interval

    ### PUBLIC METHODS ###

    @classmethod
    def from_selection(class_, selection, item_class=None):
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

        Returns interval set.
        """
        pitch_segment = PitchSegment.from_selection(selection)
        pairs = _enumerate.yield_pairs(pitch_segment)
        intervals = [second - first for first, second in pairs]
        return class_(items=intervals, item_class=item_class)


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
        PitchClassSet([6, 7, 10, 10.5])

    ..  container:: example

        Initializes named pitch-class set:

        >>> named_pitch_class_set = abjad.PitchClassSet(
        ...     items=['c', 'ef', 'bqs,', 'd'],
        ...     item_class=abjad.NamedPitchClass,
        ...     )
        >>> named_pitch_class_set
        PitchClassSet(['c', 'd', 'ef', 'bqs'])

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

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
            PitchClassSet([6, 7, 10, 10.5])

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
        return super().__contains__(argument)

    def __hash__(self):
        """
        Hashes pitch-class set.

        Returns integer.
        """
        return super().__hash__()

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

    ### PRIVATE PROPERTIES ###

    @property
    def _named_item_class(self):
        return NamedPitchClass

    @property
    def _numbered_item_class(self):
        return NumberedPitchClass

    @property
    def _parent_item_class(self):
        return PitchClass

    ### PRIVATE METHODS ###

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

    ### PUBLIC METHODS ###

    @classmethod
    def from_selection(class_, selection, item_class=None):
        """
        Makes pitch-class set from ``selection``.

        ..  container:: example

            >>> staff_1 = abjad.Staff("c'4 <d' fs' a'>4 b2")
            >>> staff_2 = abjad.Staff("c4. r8 g2")
            >>> selection = abjad.select((staff_1, staff_2))
            >>> abjad.PitchClassSet.from_selection(selection)
            PitchClassSet(['c', 'd', 'fs', 'g', 'a', 'b'])

        Returns pitch-class set.
        """
        pitch_segment = PitchSegment.from_selection(selection)
        return class_(items=pitch_segment, item_class=item_class)

    def get_normal_order(self):
        """
        Gets normal order.

        ..  container:: example

            Gets normal order of empty pitch-class set:

            >>> pc_set = abjad.PitchClassSet()
            >>> pc_set.get_normal_order()
            PitchClassSegment([])

        ..  container:: example

            Gets normal order:

            >>> pc_set = abjad.PitchClassSet([0, 1, 10, 11])
            >>> pc_set.get_normal_order()
            PitchClassSegment([10, 11, 0, 1])

        ..  container:: example

            Gets normal order:

            >>> pc_set = abjad.PitchClassSet([2, 8, 9])
            >>> pc_set.get_normal_order()
            PitchClassSegment([8, 9, 2])

        ..  container:: example

            Gets normal order of pitch-class set with degree of symmetry equal
            to 2:

            >>> pc_set = abjad.PitchClassSet([1, 2, 7, 8])
            >>> pc_set.get_normal_order()
            PitchClassSegment([1, 2, 7, 8])

        ..  container:: example

            Gets normal order of pitch-class set with degree of symmetry equal
            to 4:

            >>> pc_set = abjad.PitchClassSet([0, 3, 6, 9])
            >>> pc_set.get_normal_order()
            PitchClassSegment([0, 3, 6, 9])

        Returns pitch-class segment.
        """
        if not len(self):
            return PitchClassSegment(items=None, item_class=NumberedPitchClass)
        pitch_classes = list(self)
        pitch_classes.sort()
        candidates = []
        for i in range(self.cardinality):
            candidate = [NumberedPitch(_) for _ in pitch_classes]
            candidate = _sequence.Sequence(candidate).rotate(n=-i)
            candidates.append(candidate)
        return self._get_most_compact_ordering(candidates)

    def get_prime_form(self, transposition_only=False):
        """
        Gets prime form.

        ..  container:: example

            Gets prime form of empty pitch-class set:

            >>> pc_set = abjad.PitchClassSet()
            >>> pc_set.get_prime_form()
            PitchClassSet([])

            >>> pc_set = abjad.PitchClassSet()
            >>> pc_set.get_prime_form(transposition_only=True)
            PitchClassSet([])

        ..  container:: example

            Gets prime form:

            >>> pc_set = abjad.PitchClassSet([0, 1, 10, 11])
            >>> pc_set.get_prime_form()
            PitchClassSet([0, 1, 2, 3])

            >>> pc_set = abjad.PitchClassSet([0, 1, 10, 11])
            >>> pc_set.get_prime_form(transposition_only=True)
            PitchClassSet([0, 1, 2, 3])

        ..  container:: example

            Gets prime form:

            >>> pc_set = abjad.PitchClassSet([2, 8, 9])
            >>> pc_set.get_prime_form()
            PitchClassSet([0, 1, 6])

            >>> pc_set = abjad.PitchClassSet([2, 8, 9])
            >>> pc_set.get_prime_form(transposition_only=True)
            PitchClassSet([0, 1, 6])

        ..  container:: example

            Gets prime form of pitch-class set with degree of symmetry equal to
            2:

            >>> pc_set = abjad.PitchClassSet([1, 2, 7, 8])
            >>> pc_set.get_prime_form()
            PitchClassSet([0, 1, 6, 7])

            >>> pc_set = abjad.PitchClassSet([1, 2, 7, 8])
            >>> pc_set.get_prime_form(transposition_only=True)
            PitchClassSet([0, 1, 6, 7])

        ..  container:: example

            Gets prime form of pitch-class set with degree of symmetry equal to
            4:

            >>> pc_set = abjad.PitchClassSet([0, 3, 6, 9])
            >>> pc_set.get_prime_form()
            PitchClassSet([0, 3, 6, 9])

            >>> pc_set = abjad.PitchClassSet([0, 3, 6, 9])
            >>> pc_set.get_prime_form(transposition_only=True)
            PitchClassSet([0, 3, 6, 9])

        ..  container:: example

            Gets prime form of pitch-class that is not inversion-equivalent:

            >>> pc_set = abjad.PitchClassSet([0, 4, 6, 7])
            >>> pc_set.get_prime_form()
            PitchClassSet([0, 1, 3, 7])

            >>> pc_set = abjad.PitchClassSet([0, 4, 6, 7])
            >>> pc_set.get_prime_form(transposition_only=True)
            PitchClassSet([0, 4, 6, 7])

        ..  container:: example

            Gets prime form of inversionally nonequivalent pitch-class set:

            >>> pc_set = abjad.PitchClassSet([0, 4, 7])
            >>> pc_set.get_prime_form()
            PitchClassSet([0, 3, 7])

            >>> pc_set = abjad.PitchClassSet([0, 4, 7])
            >>> pc_set.get_prime_form(transposition_only=True)
            PitchClassSet([0, 4, 7])

        ..  container:: example

            REGRESSION:

            >>> pc_set = abjad.PitchClassSet([0, 1, 2, 5, 8, 9])
            >>> pc_set.get_prime_form()
            PitchClassSet([0, 1, 2, 5, 6, 9])

            REGRESSION:

            >>> pc_set = abjad.PitchClassSet([0, 1, 2, 3, 6, 7])
            >>> pc_set.get_prime_form()
            PitchClassSet([0, 1, 2, 3, 6, 7])

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

    def invert(self, axis=None):
        """
        Inverts pitch-class set.

        ..  container:: example

            >>> abjad.PitchClassSet(
            ...     [-2, -1.5, 6, 7, -1.5, 7],
            ...     ).invert()
            PitchClassSet([1.5, 2, 5, 6])

        Returns numbered pitch-class set.
        """
        return type(self)([pc.invert(axis=axis) for pc in self])

    def is_transposed_subset(self, pcset):
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

        Returns true or false.
        """
        for n in range(12):
            if self.transpose(n).issubset(pcset):
                return True
        return False

    def is_transposed_superset(self, pcset):
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

        Returns true or false.
        """
        for n in range(12):
            if self.transpose(n).issuperset(pcset):
                return True
        return False

    def multiply(self, n):
        """
        Multiplies pitch-class set by ``n``.

        ..  container:: example

            >>> abjad.PitchClassSet(
            ...     [-2, -1.5, 6, 7, -1.5, 7],
            ...     ).multiply(5)
            PitchClassSet([2, 4.5, 6, 11])

        Returns new pitch-class set.
        """
        items = (pitch_class.multiply(n) for pitch_class in self)
        return _new.new(self, items=items)

    def order_by(self, segment):
        """
        Orders pitch-class set by pitch-class ``segment``.

        ..  container:: example

            >>> set_ = abjad.PitchClassSet(['c', 'e', 'b'])
            >>> segment = abjad.PitchClassSegment(['e', 'a', 'f'])
            >>> set_.order_by(segment)
            PitchClassSegment("b e c")

        Returns pitch-class segment.
        """
        if not len(self) == len(segment):
            raise ValueError("set and segment must be on equal length.")
        for pitch_classes in _enumerate.yield_permutations(self):
            candidate = PitchClassSegment(pitch_classes)
            if candidate._is_equivalent_under_transposition(segment):
                return candidate
        raise ValueError(f"{self!s} can not order by {segment!s}.")

    def transpose(self, n=0):
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

        Returns new pitch-class set.
        """
        items = (pitch_class + n for pitch_class in self)
        return _new.new(self, items=items)


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
        PitchSet([-2, -1.5, 6, 7])

        >>> string = abjad.storage(set_)
        >>> print(string)
        abjad.PitchSet(
            [-2, -1.5, 6, 7]
            )

    ..  container:: example

        Named pitch set:

        >>> set_ = abjad.PitchSet(
        ...     ['bf,', 'aqs', "fs'", "g'", 'bqf', "g'"],
        ...     item_class=abjad.NamedPitch,
        ...     )
        >>> set_
        PitchSet(['bf,', 'aqs', 'bqf', "fs'", "g'"])

        >>> string = abjad.storage(set_)
        >>> print(string)
        abjad.PitchSet(
            ['bf,', 'aqs', 'bqf', "fs'", "g'"]
            )

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        """
        Is true when pitch set equals ``argument``.

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

        Return true or false.
        """
        return super().__eq__(argument)

    def __hash__(self):
        """
        Hashes pitch set.

        Returns number.
        """
        return super().__hash__()

    ### PRIVATE PROPERTIES ###

    @property
    def _named_item_class(self):
        return NamedPitch

    @property
    def _numbered_item_class(self):
        return NumberedPitch

    @property
    def _parent_item_class(self):
        return Pitch

    ### PRIVATE METHODS ###

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
        new_pitches = _new.new(self, items=new_pitches)
        return argument == new_pitches

    def _sort_self(self):
        return sorted(PitchSegment(tuple(self)))

    ### PUBLIC PROPERTIES ###

    @property
    def duplicate_pitch_classes(self):
        """
        Gets duplicate pitch-classes in pitch set.

        ..  container:: example

            >>> set_ = abjad.PitchSet(
            ...     items=[-2, -1.5, 6, 7, -1.5, 7],
            ...     item_class=abjad.NumberedPitch,
            ...     )
            >>> set_.duplicate_pitch_classes
            PitchClassSet([])

            >>> set_ = abjad.PitchSet(
            ...     items=[-2, -1.5, 6, 7, 10.5, 7],
            ...     item_class=abjad.NumberedPitch,
            ...     )
            >>> set_.duplicate_pitch_classes
            PitchClassSet([10.5])

        Returns pitch-class set.
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
    def hertz(self):
        """
        Gets hertz of pitches in pitch segment.

        ..  container:: example

            >>> pitch_set = abjad.PitchSet('c e g b')
            >>> sorted(pitch_set.hertz)
            [130.81..., 164.81..., 195.99..., 246.94...]

        Returns set.
        """
        return set(_.hertz for _ in self)

    @property
    def is_pitch_class_unique(self):
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

        Returns true or false.
        """
        numbered_pitch_class_set = PitchClassSet(self, item_class=NumberedPitchClass)
        return len(self) == len(numbered_pitch_class_set)

    ### PUBLIC METHODS ###

    @classmethod
    def from_selection(class_, selection, item_class=None):
        """
        Makes pitch set from ``selection``.

        ..  container:: example

            >>> staff_1 = abjad.Staff("c'4 <d' fs' a'>4 b2")
            >>> staff_2 = abjad.Staff("c4. r8 g2")
            >>> selection = abjad.select((staff_1, staff_2))
            >>> abjad.PitchSet.from_selection(selection)
            PitchSet(['c', 'g', 'b', "c'", "d'", "fs'", "a'"])

        Returns pitch set.
        """
        pitch_segment = PitchSegment.from_selection(selection)
        return class_(items=pitch_segment, item_class=item_class)

    def invert(self, axis):
        """
        Inverts pitch set about ``axis``.

        Returns new pitch set.
        """
        items = (pitch.invert(axis) for pitch in self)
        return _new.new(self, items=items)

    def issubset(self, argument):
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

        Returns true or false.
        """
        return super().issubset(argument)

    def issuperset(self, argument):
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

        Returns true or false.
        """
        return super().issubset(argument)

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

    def transpose(self, n=0):
        """
        Transposes pitch set by index ``n``.

        Returns new pitch set.
        """
        items = (pitch.transpose(n=n) for pitch in self)
        return _new.new(self, items=items)


class Vector(_typedcollections.TypedCounter):
    """
    Abstract vector.
    """

    ### CLASS VARIABLES ##

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, items=None, item_class=None):
        prototype_1 = (collections.abc.Iterator, types.GeneratorType)
        prototype_2 = (_typedcollections.TypedCounter, collections.Counter)
        if isinstance(items, str):
            items = items.split()
        elif isinstance(items, prototype_1):
            items = [item for item in items]
        elif isinstance(items, dict):
            items = self._dictionary_to_items(items, item_class)
        if isinstance(items, prototype_2):
            new_tokens = []
            for item, count in items.items():
                new_tokens.extend(count * [item])
            items = new_tokens
        if item_class is None:
            item_class = self._named_item_class
            if items is not None:
                if isinstance(items, _typedcollections.TypedCollection) and issubclass(
                    items.item_class, self._parent_item_class
                ):
                    item_class = items.item_class
                elif len(items):
                    if isinstance(items, collections.abc.Set):
                        items = tuple(items)
                    if isinstance(items, dict):
                        item_class = self._dictionary_to_item_class(items)
                    elif isinstance(items[0], str):
                        item_class = self._named_item_class
                    elif isinstance(items[0], (int, float)):
                        item_class = self._numbered_item_class
                    elif isinstance(items[0], self._parent_item_class):
                        item_class = type(items[0])
        assert issubclass(item_class, self._parent_item_class)
        _typedcollections.TypedCounter.__init__(
            self, items=items, item_class=item_class
        )

    ### SPECIAL METHODS ###

    def __str__(self):
        """
        String representation of vector.

        Returns string.
        """
        parts = [f"{key}: {value}" for key, value in self.items()]
        string = ", ".join(parts)
        return f"<{string}>"

    ### PRIVATE PROPERTIES ###

    @abc.abstractproperty
    def _named_item_class(self):
        raise NotImplementedError

    @abc.abstractproperty
    def _numbered_item_class(self):
        raise NotImplementedError

    @abc.abstractproperty
    def _parent_item_class(self):
        raise NotImplementedError

    ### PRIVATE METHODS ###

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

    def _dictionary_to_items(self, dictionary, item_class):
        items = []
        for initializer_token, count in dictionary.items():
            for _ in range(count):
                item = item_class(initializer_token)
                items.append(item)
        return items

    def _get_format_specification(self):
        if self.item_class.__name__.startswith("Named"):
            repr_items = {str(k): v for k, v in self.items()}
        else:
            repr_items = {
                _math.integer_equivalent_number_to_integer(float(k.number)): v
                for k, v in self.items()
            }
        return _format.FormatSpecification(
            repr_args_values=[repr_items],
            storage_format_args_values=[self._collection],
        )

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def from_selection(class_, selection, item_class=None):
        """
        Makes vector from ``selection``.

        Returns vector.
        """
        raise NotImplementedError


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
        >>> for interval, count in sorted(numbered_interval_vector.items(),
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

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, items=None, item_class=None):
        if isinstance(
            items,
            (
                PitchSegment,
                PitchSet,
                PitchClassSegment,
                PitchClassSet,
            ),
        ):
            intervals = []
            pairs = _enumerate.yield_pairs(items)
            for first, second in pairs:
                intervals.append(second - first)
            items = intervals
        Vector.__init__(self, items=items, item_class=item_class)

    ### SPECIAL METHODS ###

    def __repr__(self):
        """
        Gets interpret representation of interval vector.

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
            IntervalVector({-11: 1, -10: 1, -9: 1, -8: 2, -7: 3, -6: 3, -5: 4, -4: 4, -3: 4, -2: 5, -1: 6, 1: 5, 2: 5, 3: 5, 4: 4, 5: 3, 6: 3, 7: 2, 8: 2, 9: 2, 10: 1}, item_class=NumberedInterval)

        ..  container:: example

            Initializes from interpreter representation of interval vector:

            >>> abjad.IntervalVector(vector)
            IntervalVector({-11: 1, -10: 1, -9: 1, -8: 2, -7: 3, -6: 3, -5: 4, -4: 4, -3: 4, -2: 5, -1: 6, 1: 5, 2: 5, 3: 5, 4: 4, 5: 3, 6: 3, 7: 2, 8: 2, 9: 2, 10: 1}, item_class=NumberedInterval)

        Returns string.
        """
        return super().__repr__()

    ### PRIVATE PROPERTIES ###

    @property
    def _named_item_class(self):
        return NamedInterval

    @property
    def _numbered_item_class(self):
        return NumberedInterval

    @property
    def _parent_item_class(self):
        return Interval

    ### PUBLIC METHODS ###

    @classmethod
    def from_selection(class_, selection, item_class=None):
        """
        Makes interval vector from ``selection``.

        Returns interval vector.
        """
        pitch_segment = PitchSegment.from_selection(selection)
        return class_(pitch_segment, item_class=item_class)


class IntervalClassVector(Vector):
    """
    Interval-class vector.

    ..  container:: example

        An interval-class vector:

        >>> pitch_segment = abjad.PitchSegment(
        ...     items=[0, 11, 7, 4, 2, 9, 3, 8, 10, 1, 5, 6],
        ...     )
        >>> numbered_interval_class_vector = abjad.IntervalClassVector(
        ...     items=pitch_segment,
        ...     item_class=abjad.NumberedInversionEquivalentIntervalClass,
        ...     )

        >>> items = sorted(numbered_interval_class_vector.items())
        >>> for interval, count in items:
        ...     print(interval, count)
        ...
        1 12
        2 12
        3 12
        4 12
        5 12
        6 6

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

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

    ### SPECIAL METHODS ###

    def __repr__(self):
        """
        Gets interpreter representation of interval-class vector.

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
            IntervalClassVector({1: 12, 2: 12, 3: 12, 4: 12, 5: 12, 6: 6}, item_class=NumberedInversionEquivalentIntervalClass)

        ..  container:: example

            Initializes from interpreter representation of interval-class
            vector:

            >>> abjad.IntervalClassVector(vector)
            IntervalClassVector({1: 12, 2: 12, 3: 12, 4: 12, 5: 12, 6: 6}, item_class=NumberedInversionEquivalentIntervalClass)

        Returns string.
        """
        return super().__repr__()

    ### PRIVATE PROPERTIES ###

    @property
    def _label(self):
        counts = []
        for i in range(7):
            counts.append(self[i])
        counts = "".join([str(x) for x in counts])
        if len(self) == 13:
            quartertones = []
            for i in range(6):
                quartertones.append(self[i + 0.5])
            quartertones = "".join([str(x) for x in quartertones])
            return r'\tiny \column { "%s" "%s" }' % (counts, quartertones)
        else:
            return r"\tiny %s" % counts

    @property
    def _named_item_class(self):
        return NamedIntervalClass

    @property
    def _numbered_item_class(self):
        return NumberedIntervalClass

    @property
    def _parent_item_class(self):
        return IntervalClass

    ### PUBLIC METHODS ###

    @classmethod
    def from_selection(class_, selection, item_class=None):
        """
        Makes interval-class vector from ``selection``.

        ..  container:: example

            Makes numbered inversion-equivalent interval-class vector from
            selection:

            >>> chord = abjad.Chord("<c' d' b''>4"),
            >>> vector = abjad.IntervalClassVector.from_selection(
            ...     abjad.select(chord),
            ...     item_class=abjad.NumberedInversionEquivalentIntervalClass,
            ...     )
            >>> vector
            IntervalClassVector({1: 1, 2: 1, 3: 1}, item_class=NumberedInversionEquivalentIntervalClass)

        ..  container:: example

            Makes numbered interval-class vector from selection:

            >>> chord = abjad.Chord("<c' d' b''>4")
            >>> vector = abjad.IntervalClassVector.from_selection(
            ...     abjad.select(chord),
            ...     item_class=abjad.NumberedIntervalClass,
            ...     )
            >>> vector
            IntervalClassVector({-11: 1, -9: 1, -2: 1}, item_class=NumberedIntervalClass)

            .. todo:: This should probabaly be checked. Resulting values
                should probabaly be positive (or signless) instead of negative.

        ..  container:: example

            Makes named interval-class vector from selection:

            >>> chord = abjad.Chord("<c' d' b''>4")
            >>> vector = abjad.IntervalClassVector.from_selection(
            ...     abjad.select(chord),
            ...     item_class=None,
            ...     )
            >>> vector
            IntervalClassVector({'-M2': 1, '-M6': 1, '-M7': 1}, item_class=NamedIntervalClass)

            .. todo:: This should probabaly be checked. Resulting values
                should probabaly be positive (or signless) instead of negative.

        Returns new interval-class vector.
        """
        pitch_segment = PitchSegment.from_selection(selection)
        return class_(pitch_segment, item_class=item_class)


class PitchClassVector(Vector):
    """
    Pitch-class vector.

    ..  container:: example

        Pitch-class vector:

        >>> vector = abjad.PitchClassVector(
        ...     items=[7, 6, -2, -3, -3, 0, 1, 14, 15, 16, 16],
        ...     item_class=abjad.NumberedPitchClass,
        ...     )

        >>> items = sorted(vector.items())
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

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __repr__(self):
        """
        Gets interpreter representation of pitch-class vector.

        ..  container:: example

            Gets interpreter representation of pitch-class vector:

            >>> vector = abjad.PitchClassVector(
            ...     items=[7, 6, -2, -3, -3, 0, 1, 14, 15, 16, 16],
            ...     item_class=abjad.NumberedPitchClass,
            ...     )

            >>> vector
            PitchClassVector({0: 1, 1: 1, 2: 1, 3: 1, 4: 2, 6: 1, 7: 1, 9: 2, 10: 1}, item_class=NumberedPitchClass)

        ..  container:: example

            Initializes from interpreter representation of pitch-class vector:


                >>> abjad.PitchClassVector(vector)
                PitchClassVector({0: 1, 1: 1, 2: 1, 3: 1, 4: 2, 6: 1, 7: 1, 9: 2, 10: 1}, item_class=NumberedPitchClass)

        Returns string.
        """
        return super().__repr__()

    ### PRIVATE PROPERTIES ###

    @property
    def _named_item_class(self):
        return NamedPitchClass

    @property
    def _numbered_item_class(self):
        return NumberedPitchClass

    @property
    def _parent_item_class(self):
        return PitchClass

    ### PUBLIC METHODS ###

    @classmethod
    def from_selection(class_, selection, item_class=None):
        """
        Makes pitch-class vector from ``selection``.

        Returns pitch-class vector.
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
        ...     )

        >>> items = list(vector.items())
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

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __repr__(self):
        """
        Gets interpreter representation of pitch vector.

        ..  container:: example

            Gets interpreter representation of pitch vector:

            >>> vector = abjad.PitchVector(
            ...     items=[7, 6, -2, -3, -3, 0, 1, 14, 15, 16, 16],
            ...     item_class=abjad.NumberedPitch,
            ...     )

            >>> vector
            PitchVector({-3: 2, -2: 1, 0: 1, 1: 1, 6: 1, 7: 1, 14: 1, 15: 1, 16: 2}, item_class=NumberedPitch)

        ..  container:: example

            Initializes from interpreter representation of pitch vector:

                >>> abjad.PitchVector(vector)
                PitchVector({-3: 2, -2: 1, 0: 1, 1: 1, 6: 1, 7: 1, 14: 1, 15: 1, 16: 2}, item_class=NumberedPitch)

        Returns string.
        """
        return super().__repr__()

    ### PRIVATE PROPERTIES ###

    @property
    def _named_item_class(self):
        return NamedPitch

    @property
    def _numbered_item_class(self):
        return NumberedPitch

    @property
    def _parent_item_class(self):
        return Pitch

    ### PUBLIC METHODS ###

    @classmethod
    def from_selection(class_, selection, item_class=None):
        """
        Makes pitch vector from ``selection``.

        Returns pitch vector.
        """
        pitch_segment = PitchSegment.from_selection(selection)
        return class_(pitch_segment, item_class=item_class)
