from abjad import *
from abjad.core.LilyPondTweakReservoir import LilyPondTweakReservoir


def test_LilyPondTweaksReservoir___repr___01():
    '''LilyPond grob proxy repr is evaluable.
    '''

    chord = Chord([0, 2, 10], (1, 4))
    chord[1].tweak.color = 'red'

    tweak_reservoir_1 = chord[1].tweak
    tweak_reservoir_2 = eval(repr(tweak_reservoir_1))

    assert isinstance(tweak_reservoir_1, LilyPondTweakReservoir)
    assert isinstance(tweak_reservoir_2, LilyPondTweakReservoir)
