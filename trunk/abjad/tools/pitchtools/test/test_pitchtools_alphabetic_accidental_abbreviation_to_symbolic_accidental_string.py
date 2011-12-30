from abjad import *


def test_pitchtools_alphabetic_accidental_abbreviation_to_symbolic_accidental_string_01():

    assert pitchtools.alphabetic_accidental_abbreviation_to_symbolic_accidental_string('ff') == 'bb'
    assert pitchtools.alphabetic_accidental_abbreviation_to_symbolic_accidental_string('tqf') == 'b~'
    assert pitchtools.alphabetic_accidental_abbreviation_to_symbolic_accidental_string('f') == 'b'
    assert pitchtools.alphabetic_accidental_abbreviation_to_symbolic_accidental_string('qf') == '~'
    assert pitchtools.alphabetic_accidental_abbreviation_to_symbolic_accidental_string('') == ''
    assert pitchtools.alphabetic_accidental_abbreviation_to_symbolic_accidental_string('!') == '!'
    assert pitchtools.alphabetic_accidental_abbreviation_to_symbolic_accidental_string('qs') == '+'
    assert pitchtools.alphabetic_accidental_abbreviation_to_symbolic_accidental_string('s') == '#'
    assert pitchtools.alphabetic_accidental_abbreviation_to_symbolic_accidental_string('tqs') == '#+'
    assert pitchtools.alphabetic_accidental_abbreviation_to_symbolic_accidental_string('ss') == '##'


def test_pitchtools_alphabetic_accidental_abbreviation_to_symbolic_accidental_string_02():

    assert pitchtools.alphabetic_accidental_abbreviation_to_symbolic_accidental_string('foo') is None
