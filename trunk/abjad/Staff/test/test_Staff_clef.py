from abjad import *


def test_Staff_clef_01( ):
   '''Test ClefInterface public attributes.'''
   t = Staff(Note(0, (1, 4)) * 8)
   assert t.clef.change == False
   assert isinstance(t.clef.effective, Clef)
   assert t.clef.forced is None
   assert t.clef.effective == Clef('treble')


def test_Staff_clef_02( ):
   '''Force clef on nonempty staff.'''
   t = Staff(Note(0, (1, 4)) * 8)
   t.clef.forced = Clef('bass')
   assert t.format == '''\\new Staff {\n\t\\clef "bass"\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n}'''
   r'''
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


def test_Staff_clef_03( ):
   '''Force clef on empty staff.'''
   t = Staff([ ])
   t.clef.forced = Clef('bass')
   assert t.format == '\\new Staff {\n\t\\clef "bass"\n}'
   r'''
   \new Staff {
      \clef "bass"
   }
   '''


def test_Staff_clef_04( ):
   '''Staff clef carries over to staff-contained leaves.'''
   t = Staff(Note(0, (1, 4)) * 8)
   t.clef.forced = Clef('bass')
   for x in t:
      assert x.clef.effective == Clef('bass')


def test_Staff_clef_05( ):
   '''Staff cleff carries over to staff-contained leaves,
      but leaves can reassert new clef.'''
   t = Staff(Note(0, (1, 4)) * 8)
   t.clef.forced = Clef('bass')
   t[4].clef.forced = Clef('treble')
   for i, leaf in enumerate(t):
      if i in (0, 1, 2, 3):
         assert leaf.clef.effective == Clef('bass')
      else:
         assert leaf.clef.effective == Clef('treble')


def test_Staff_clef_06( ):
   '''Staff clef clears with None.'''
   t = Staff(Note(0, (1, 4)) * 8)
   t.clef.forced = Clef('bass')
   t.clef.forced = None
   for leaf in t:
      assert leaf.clef.effective == Clef('treble')


def test_Staff_clef_07( ):
   '''Staff / first-leaf clef competition resolves
      in favor of first leaf.'''
   t = Staff(Note(0, (1, 4)) * 8)
   t.clef.forced = Clef('treble')
   t[0].clef.forced = Clef('bass')
   for leaf in t:
      assert leaf.clef.effective == Clef('bass')
