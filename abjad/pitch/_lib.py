import re

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

        >>> module = abjad.pitch._lib
        >>> function = module._diatonic_number_to_octaves_and_diatonic_remainder
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

    >>> function = abjad.pitch._lib._diatonic_number_and_quality_to_semitones

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

del re
