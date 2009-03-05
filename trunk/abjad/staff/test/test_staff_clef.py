from abjad import *
#from abjad.clef.clef import _Clef
from abjad.clef.clef import Clef
from abjad.clef.interface import _ClefInterface


def test_staff_clef_01( ):
   '''Staff has a clef interface.'''
   t = Staff(Note(0, (1, 4)) * 8)
   assert isinstance(t.clef, _ClefInterface)
   

def test_staff_clef_02( ):
   '''Test _ClefInterface public attributes.'''
   t = Staff(Note(0, (1, 4)) * 8)
   assert t.clef.change == False
   #assert isinstance(t.clef.effective, _Clef)
   assert isinstance(t.clef.effective, Clef)
   assert t.clef.forced is None
   assert t.clef.name == 'treble'


def test_staff_clef_03( ):
   '''Force clef on nonempty staff.'''
   t = Staff(Note(0, (1, 4)) * 8)
   t.clef = 'bass'
   assert t.format == '''\\new Staff {\n\t\\clef "bass"\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n}'''
   '''
   \new Staff {
      \clef "bass"
      c'4
      c'4
      c'4
      c'4
      c'4
      c'4
      c'4
      c'4
   }
   '''


def test_staff_clef_04( ):
   '''Force clef on empty staff.'''
   t = Staff([ ])
   t.clef = 'bass'
   assert t.format == '\\new Staff {\n\t\\clef "bass"\n}'
   '''
   \new Staff {
      \clef "bass"
   }
   '''


def test_staff_clef_05( ):
   '''Staff clef carries over to staff-contained leaves.'''
   t = Staff(Note(0, (1, 4)) * 8)
   t.clef = 'bass'
   for x in t:
      assert x.clef.name == 'bass'


def test_staff_clef_06( ):
   '''Staff cleff carries over to staff-contained leaves,
      but leaves can reassert new clef.'''
   t = Staff(Note(0, (1, 4)) * 8)
   t.clef = 'bass'
   t[4].clef = 'treble'
   for i, leaf in enumerate(t):
      if i in (0, 1, 2, 3):
         assert leaf.clef.name == 'bass'
      else:
         assert leaf.clef.name == 'treble'


def test_staff_clef_07( ):
   '''Staff clef clears with None.'''
   t = Staff(Note(0, (1, 4)) * 8)
   t.clef = 'bass'
   t.clef = None
   for leaf in t:
      assert leaf.clef.name == 'treble'


def test_staff_clef_08( ):
   '''Staff / first-leaf clef competition resolves
      in favor of first leaf.'''
   t = Staff(Note(0, (1, 4)) * 8)
   t.clef = 'treble'
   t[0].clef = 'bass'
   for leaf in t:
      assert leaf.clef.name == 'bass'
