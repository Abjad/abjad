from abjad import *


def test_container_eject_contents_01( ):
   '''Eject container contents.'''

   t = Staff(scale(4))
   Beam(t)

   contents = container_eject_contents(t)

   assert len(t) == 0
   assert len(contents) == 4
   assert t.format == '\\new Staff {\n}'


def test_container_eject_contents_02( ):
   '''Eject container contents.'''

   t = Staff([ ])
   contents = container_eject_contents(t)

   assert len(t) == 0
   assert contents == [ ]
