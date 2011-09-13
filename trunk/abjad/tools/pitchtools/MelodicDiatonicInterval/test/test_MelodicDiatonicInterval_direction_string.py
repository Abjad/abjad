from abjad import *


def test_MelodicDiatonicInterval_direction_string_01():

    assert pitchtools.MelodicDiatonicInterval('perfect', 1).direction_string is \
        None
    assert pitchtools.MelodicDiatonicInterval('minor', 2).direction_string == \
        'ascending'
    assert pitchtools.MelodicDiatonicInterval('major', 2).direction_string == \
        'ascending'
    assert pitchtools.MelodicDiatonicInterval('minor', 3).direction_string == \
        'ascending'
    assert pitchtools.MelodicDiatonicInterval('major', 3).direction_string == \
        'ascending'


def test_MelodicDiatonicInterval_direction_string_02():

    assert pitchtools.MelodicDiatonicInterval('perfect', -1).direction_string \
        is None
    assert pitchtools.MelodicDiatonicInterval('minor', -2).direction_string == \
        'descending'
    assert pitchtools.MelodicDiatonicInterval('major', -2).direction_string == \
        'descending'
    assert pitchtools.MelodicDiatonicInterval('minor', -3).direction_string == \
        'descending'
    assert pitchtools.MelodicDiatonicInterval('major', -3).direction_string == \
        'descending'
