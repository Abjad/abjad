from abjad import *
import py.test


def test_containertools_contents_delete_01( ):
   '''Eject container contents.'''

   t = Staff(construct.scale(4))
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


def test_containertools_contents_delete_03( ):
   '''Raise type error on noncontainer.'''

   assert py.test.raises(TypeError, 
      'containertools.contents_delete(Note(0, (1, 4)))')
