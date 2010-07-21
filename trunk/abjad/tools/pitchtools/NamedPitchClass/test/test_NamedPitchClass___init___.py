from abjad import *


def test_NamedPitchClass___init___01( ):
   '''Init from name string.'''

   assert pitchtools.NamedPitchClass('c').name == 'c'
   assert pitchtools.NamedPitchClass('cs').name == 'cs'
   assert pitchtools.NamedPitchClass('cf').name == 'cf'
   assert pitchtools.NamedPitchClass('cqs').name == 'cqs'
   assert pitchtools.NamedPitchClass('cqf').name == 'cqf'


def test_NamedPitchClass___init___02( ):
   '''Init from other named pitch class instance.'''

   npc = pitchtools.NamedPitchClass('c')
   new = pitchtools.NamedPitchClass(npc)

   assert new == npc
   assert new is not npc


def test_NamedPitchClass___init___03( ):
   '''Init from note head instance.'''

   chord = Chord([0, 2, 3], (1, 4))
   note_head = chord[0]
   npc = pitchtools.NamedPitchClass(note_head)

   assert npc == pitchtools.NamedPitchClass('c')
