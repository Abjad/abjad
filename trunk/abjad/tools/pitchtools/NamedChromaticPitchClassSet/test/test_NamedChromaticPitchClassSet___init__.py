from abjad import *


def test_NamedChromaticPitchClassSet___init___01():
    '''Init with named pitch-classes.'''

    npc_set = pitchtools.NamedChromaticPitchClassSet([
        pitchtools.NamedChromaticPitchClass('c'),
        pitchtools.NamedChromaticPitchClass('d'),
        pitchtools.NamedChromaticPitchClass('e')])

    assert len(npc_set) == 3


def test_NamedChromaticPitchClassSet___init___02():
    '''Works with chords.'''

    chord = Chord([12, 14, 16], (1, 4))
    npc_set_1 = pitchtools.NamedChromaticPitchClassSet(chord)

    npc_set_2 = pitchtools.NamedChromaticPitchClassSet([
        pitchtools.NamedChromaticPitchClass('c'),
        pitchtools.NamedChromaticPitchClass('d'),
        pitchtools.NamedChromaticPitchClass('e')])

    assert npc_set_1 == npc_set_2


def test_NamedChromaticPitchClassSet___init___03():
    '''Works with notes.'''

    note = Note(13, (1, 4))
    npc_set_1 = pitchtools.NamedChromaticPitchClassSet(note)

    npc_set_2 = pitchtools.NamedChromaticPitchClassSet([
        pitchtools.NamedChromaticPitchClass('cs')])

    assert npc_set_1 == npc_set_2
