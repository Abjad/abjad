from abjad import *


def test_Accidental_symbolic_string_01():

    assert pitchtools.Accidental('s').symbolic_string == '#'
    assert pitchtools.Accidental('ss').symbolic_string == '###'
    assert pitchtools.Accidental('f').symbolic_string == 'b'
    assert pitchtools.Accidental('ff').symbolic_string == 'bb'
    assert pitchtools.Accidental('').symbolic_string == ''
