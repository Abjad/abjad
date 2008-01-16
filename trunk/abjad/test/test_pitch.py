from abjad import *


### INIT TYPICAL PITCH ###

def test_public_pitch_interface( ):

   p = Pitch(13)
   assert repr(p) == 'Pitch(cs, 5)'
   assert p.letter == 'c'
   assert p.octave == 5
   assert p.name == 'cs'
   assert p.pair == ('cs', 5)
   assert p.number == 13
   assert p.pc == 1
   assert p.diatonicScaleDegree == 1


### INIT EMPTY PITCH ###

def test_empty_pitch( ):
   
   p = Pitch( )
   assert repr(p) == 'Pitch( )'
   assert p.letter == None
   assert p.octave == None
   assert p.name == None
   assert p.pair == None
   assert p.number == None
   assert p.pc == None
   assert p.diatonicScaleDegree == None
