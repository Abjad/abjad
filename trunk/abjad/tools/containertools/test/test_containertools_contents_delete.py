from abjad import *


def test_containertools_contents_delete_01( ):
   '''Eject container contents.'''

   t = Staff(scale(4))
   Beam(t)

   contents = containertools.contents_delete(t)

   assert len(t) == 0
   assert len(contents) == 4
   assert t.format == '\\new Staff {\n}'


def test_containertools_contents_delete_02( ):
   '''Eject container contents.'''

   t = Staff([ ])
   contents = containertools.contents_delete(t)

   assert len(t) == 0
   assert contents == [ ]
