from abjad import *


def test_NamedPitchClassSet___init___01( ):
   '''Init with named pitch classes.'''

   npc_set = pitchtools.NamedPitchClassSet([
      pitchtools.NamedPitchClass('c'),
      pitchtools.NamedPitchClass('d'),
      pitchtools.NamedPitchClass('e')])

   assert len(npc_set) == 3


def test_NamedPitchClassSet___init___02( ):
   '''Works with chords.'''

   chord = Chord([12, 14, 16], (1, 4))
   npc_set_1 = pitchtools.NamedPitchClassSet(chord)

   npc_set_2 = pitchtools.NamedPitchClassSet([
      pitchtools.NamedPitchClass('c'),
      pitchtools.NamedPitchClass('d'),
      pitchtools.NamedPitchClass('e')])

   assert npc_set_1 == npc_set_2


def test_NamedPitchClassSet___init___03( ):
   '''Works with notes.'''

   note = Note(13, (1, 4))
   npc_set_1 = pitchtools.NamedPitchClassSet(note)

   npc_set_2 = pitchtools.NamedPitchClassSet([
      pitchtools.NamedPitchClass('cs')])

   assert npc_set_1 == npc_set_2
