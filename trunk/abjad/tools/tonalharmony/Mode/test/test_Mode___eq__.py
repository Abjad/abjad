from abjad import *


def test_Mode___eq___01( ):

   mode_1 = tonalharmony.Mode('dorian')
   mode_2 = tonalharmony.Mode('dorian')
   mode_3 = tonalharmony.Mode('phrygian')

   assert     mode_1 == mode_1
   assert     mode_1 == mode_2
   assert not mode_1 == mode_3
   assert     mode_2 == mode_1
   assert     mode_2 == mode_2
   assert not mode_2 == mode_3
   assert not mode_3 == mode_1
   assert not mode_3 == mode_2
   assert     mode_3 == mode_3


def test_Mode___eq___02( ):
   '''Synonym modes do not compare equal, by definition.'''

   major = tonalharmony.Mode('major')
   ionian = tonalharmony.Mode('ionian')

   assert not major == ionian
   assert not ionian == major
