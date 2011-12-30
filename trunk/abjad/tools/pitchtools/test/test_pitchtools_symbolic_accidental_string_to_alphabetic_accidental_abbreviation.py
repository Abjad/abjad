from abjad import *


def test_pitchtools_symbolic_accidental_string_to_alphabetic_accidental_abbreviation_01():

    assert pitchtools.symbolic_accidental_string_to_alphabetic_accidental_abbreviation('') == ''
    assert pitchtools.symbolic_accidental_string_to_alphabetic_accidental_abbreviation('!') == ''
    assert pitchtools.symbolic_accidental_string_to_alphabetic_accidental_abbreviation('bb') == ''
    assert pitchtools.symbolic_accidental_string_to_alphabetic_accidental_abbreviation('b~') == ''
    assert pitchtools.symbolic_accidental_string_to_alphabetic_accidental_abbreviation('b') == ''
    assert pitchtools.symbolic_accidental_string_to_alphabetic_accidental_abbreviation('~') == ''
    assert pitchtools.symbolic_accidental_string_to_alphabetic_accidental_abbreviation('##') == ''
    assert pitchtools.symbolic_accidental_string_to_alphabetic_accidental_abbreviation('#+') == ''
    assert pitchtools.symbolic_accidental_string_to_alphabetic_accidental_abbreviation('#') == ''
    assert pitchtools.symbolic_accidental_string_to_alphabetic_accidental_abbreviation('+') == ''


def test_pitchtools_symbolic_accidental_string_to_alphabetic_accidental_abbreviation_01():

    assert pitchtools.symbolic_accidental_string_to_alphabetic_accidental_abbreviation('foo') is None
