from abjad import *


def test_voice_invocation_01( ):
   r'''Anonymous voices invoke with \new Voice.'''

   t = Voice(scale(4))

   assert t.name is None
   assert t.context == 'Voice'


def test_voice_invocation_02( ):
   r''' Named voices invoke with \context Voice = "name".'''

   t = Voice(scale(4))
   t.name = 'foo'

   assert t.name == 'foo'
   assert t.context == 'Voice'
