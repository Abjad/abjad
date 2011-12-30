from abjad import *


def test_pitchtools_symbolic_accidental_string_to_alphabetic_accidental_abbreviation_01():

    assert pitchtools.symbolic_accidental_string_to_alphabetic_accidental_abbreviation('') == ''
    assert pitchtools.symbolic_accidental_string_to_alphabetic_accidental_abbreviation('!') == '!'
    assert pitchtools.symbolic_accidental_string_to_alphabetic_accidental_abbreviation('bb') == 'ff'
    assert pitchtools.symbolic_accidental_string_to_alphabetic_accidental_abbreviation('b~') == 'tqf'
    assert pitchtools.symbolic_accidental_string_to_alphabetic_accidental_abbreviation('b') == 'f'
    assert pitchtools.symbolic_accidental_string_to_alphabetic_accidental_abbreviation('~') == 'qf'
    assert pitchtools.symbolic_accidental_string_to_alphabetic_accidental_abbreviation('##') == 'ss'
    assert pitchtools.symbolic_accidental_string_to_alphabetic_accidental_abbreviation('#+') == 'tqs'
    assert pitchtools.symbolic_accidental_string_to_alphabetic_accidental_abbreviation('#') == 's'
    assert pitchtools.symbolic_accidental_string_to_alphabetic_accidental_abbreviation('+') == 'qs'


def test_pitchtools_symbolic_accidental_string_to_alphabetic_accidental_abbreviation_02():

    assert pitchtools.symbolic_accidental_string_to_alphabetic_accidental_abbreviation('foo') is None
