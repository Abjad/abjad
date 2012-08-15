from abjad import *


def test_pitchtools_spell_chromatic_interval_number_01():

    diatonic_interval = pitchtools.spell_chromatic_interval_number(1, 0)
    assert diatonic_interval == pitchtools.MelodicDiatonicInterval('perfect', 1)

    diatonic_interval = pitchtools.spell_chromatic_interval_number(1, 1)
    assert diatonic_interval == pitchtools.MelodicDiatonicInterval(
        'augmented', 1)

    diatonic_interval = pitchtools.spell_chromatic_interval_number(2, 0)
    assert diatonic_interval == pitchtools.MelodicDiatonicInterval('diminished', 2)

    diatonic_interval = pitchtools.spell_chromatic_interval_number(2, 1)
    assert diatonic_interval == pitchtools.MelodicDiatonicInterval('minor', 2)

    diatonic_interval = pitchtools.spell_chromatic_interval_number(2, 2)
    assert diatonic_interval == pitchtools.MelodicDiatonicInterval('major', 2)

    diatonic_interval = pitchtools.spell_chromatic_interval_number(2, 3)
    assert diatonic_interval == pitchtools.MelodicDiatonicInterval('augmented', 2)


# TODO: Refactor all diatonic stuff so unison is 0 instead of 1 #

def test_pitchtools_spell_chromatic_interval_number_02():

    diatonic_interval = pitchtools.spell_chromatic_interval_number(1, 0)
    assert diatonic_interval == pitchtools.MelodicDiatonicInterval('perfect', 1)

    diatonic_interval = pitchtools.spell_chromatic_interval_number(1, -1)
    assert diatonic_interval == pitchtools.MelodicDiatonicInterval(
        'augmented', -1)

    diatonic_interval = pitchtools.spell_chromatic_interval_number(2, 0)
    # THE ASCENDING INTERVAL HERE IS WEIRD #
    assert diatonic_interval == pitchtools.MelodicDiatonicInterval(
        'diminished', 2)

    diatonic_interval = pitchtools.spell_chromatic_interval_number(2, -1)
    assert diatonic_interval == pitchtools.MelodicDiatonicInterval('minor', -2)

    diatonic_interval = pitchtools.spell_chromatic_interval_number(2, -2)
    assert diatonic_interval == pitchtools.MelodicDiatonicInterval('major', -2)

    diatonic_interval = pitchtools.spell_chromatic_interval_number(2, -3)
    assert diatonic_interval == pitchtools.MelodicDiatonicInterval(
        'augmented', -2)
