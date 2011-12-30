from abjad import *


def test_pitchtools_is_symbolic_accidental_string_01():

    assert pitchtools.is_symbolic_accidental_string('#')
    assert pitchtools.is_symbolic_accidental_string('##')
    assert pitchtools.is_symbolic_accidental_string('b')
    assert pitchtools.is_symbolic_accidental_string('bb')
    assert pitchtools.is_symbolic_accidental_string('+')
    assert pitchtools.is_symbolic_accidental_string('#+')
    assert pitchtools.is_symbolic_accidental_string('~')
    assert pitchtools.is_symbolic_accidental_string('b~')
    assert pitchtools.is_symbolic_accidental_string('')


def test_pitchtools_is_symbolic_accidental_string_02():

    assert not pitchtools.is_symbolic_accidental_string('foo')
    assert not pitchtools.is_symbolic_accidental_string(7)
    assert not pitchtools.is_symbolic_accidental_string(True)
    assert not pitchtools.is_symbolic_accidental_string('++')
    assert not pitchtools.is_symbolic_accidental_string('~~')
