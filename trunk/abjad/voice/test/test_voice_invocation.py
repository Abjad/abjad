from abjad import *


def test_voice_invocation_01( ):
   '''
   Anonymous voices invoke with \\new Voice.
   '''

   t = Voice(scale(4))
   assert t.invocation.command == r'\new'
   assert t.invocation.name is None
   assert t.invocation.type == 'Voice'


def test_voice_invocation_02( ):
   '''
   Named voices invoke with \\context Voice = "name".
   '''

   t = Voice(scale(4))
   t.invocation.name = 'foo'
   assert t.invocation.command == r'\context'
   assert t.invocation.name == 'foo'
   assert t.invocation.type == 'Voice'
