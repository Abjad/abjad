from abjad import *


def test_Accidental_symbolic_accidental_string_01():

    assert pitchtools.Accidental('s').symbolic_accidental_string == '#'
    assert pitchtools.Accidental('ss').symbolic_accidental_string == '##'
    assert pitchtools.Accidental('f').symbolic_accidental_string == 'b'
    assert pitchtools.Accidental('ff').symbolic_accidental_string == 'bb'
    assert pitchtools.Accidental('').symbolic_accidental_string == ''
