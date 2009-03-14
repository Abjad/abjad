from abjad import *


def test_voice_len_01( ):
   '''Voice length returns the number of elements in voice.'''

   t = Voice( )
   assert len(t) == 0


def test_voice_len_02( ):
   '''Voice length returns the number of elements in voice.'''

   t = Voice(scale(4))
   assert len(t) == 4
