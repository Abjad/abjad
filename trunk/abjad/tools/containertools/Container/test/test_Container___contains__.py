from abjad import *


def test_Container___contains___01( ):

   note = Note(0, (1, 4))
   voice = Voice([Note(0, (1, 4))])
  
   assert not note in voice
