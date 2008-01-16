from abjad import *


### TEST TYPICAL VOICE ###

def test_typical_voice_01( ):
   v = Voice(Note(0, (1, 8)) * 5)
   assert isinstance(v, Voice)
   assert v.invocation.lhs == 'Voice'
   assert v.brackets == 'curly'
   assert len(v) == 5



### TEST EMPTY VOICE ###

def test_empty_voice_01( ):
   v = Voice([ ])
   assert isinstance(v, Voice)
   assert v.invocation.lhs == 'Voice'
   assert v.brackets == 'curly'
   assert len(v) == 0
