from abjad import *


def test_NamedPitchClass___init____01( ):
   '''Init from name string.'''

   assert pitchtools.NamedChromaticPitchClass('c').name == 'c'
   assert pitchtools.NamedChromaticPitchClass('cs').name == 'cs'
   assert pitchtools.NamedChromaticPitchClass('cf').name == 'cf'
   assert pitchtools.NamedChromaticPitchClass('cqs').name == 'cqs'
   assert pitchtools.NamedChromaticPitchClass('cqf').name == 'cqf'


def test_NamedPitchClass___init____02( ):
   '''Init from other named pitch class instance.'''

   npc = pitchtools.NamedChromaticPitchClass('c')
   new = pitchtools.NamedChromaticPitchClass(npc)

   assert new == npc
   assert new is not npc


def test_NamedPitchClass___init____03( ):
   '''Init from note head instance.'''

   chord = Chord([0, 2, 3], (1, 4))
   note_head = chord[0]
   npc = pitchtools.NamedChromaticPitchClass(note_head)

   assert npc == pitchtools.NamedChromaticPitchClass('c')
