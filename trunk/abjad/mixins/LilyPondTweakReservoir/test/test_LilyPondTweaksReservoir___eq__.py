from abjad import *


def test_LilyPondTweaksReservoir___eq___01():

    chord = Chord([0, 2, 10], (1, 4))

    chord[0].tweak.color = 'red'
    chord[0].tweak.thickness = 2

    chord[1].tweak.color = 'red'
    chord[1].tweak.thickness = 2

    chord[2].tweak.color = 'blue'

    tweak_reservoir_1 = chord[0].tweak
    tweak_reservoir_2 = chord[1].tweak
    tweak_reservoir_3 = chord[2].tweak

    assert      tweak_reservoir_1 == tweak_reservoir_1
    assert      tweak_reservoir_1 == tweak_reservoir_2
    assert not tweak_reservoir_1 == tweak_reservoir_3
    assert      tweak_reservoir_2 == tweak_reservoir_1
    assert      tweak_reservoir_2 == tweak_reservoir_2
    assert not tweak_reservoir_2 == tweak_reservoir_3
    assert not tweak_reservoir_3 == tweak_reservoir_1
    assert not tweak_reservoir_3 == tweak_reservoir_2
    assert      tweak_reservoir_3 == tweak_reservoir_3
