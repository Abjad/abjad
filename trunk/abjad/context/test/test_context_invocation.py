from abjad import *
import py.test


def test_init_typical_invocation_01( ):
   t = Staff([ ])
   assert t.format == '\\new Staff {\n}'


def test_init_typical_invocation_02( ):
   t = Staff([ ])
   t.invocation = 'Breath'
   assert t.format == '\\new Breath {\n}'


def test_init_typical_invocation_03( ):
   t = Staff([ ])
   t.invocation = 'Breath', 'flute'
   assert t.format == '\\context Breath = "flute" {\n}'
