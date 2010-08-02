from abjad import *


def test_Voice___len___01( ):
   '''Voice length returns the number of elements in voice.'''

   t = Voice( )
   assert len(t) == 0


def test_Voice___len___02( ):
   '''Voice length returns the number of elements in voice.'''

   t = Voice(macros.scale(4))
   assert len(t) == 4
