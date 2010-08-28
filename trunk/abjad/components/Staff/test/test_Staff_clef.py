from abjad import *
import py.test


def test_Staff_clef_01( ):
   '''Test ClefInterface public attributes.'''
   t = Staff(Note(0, (1, 4)) * 8)
   #assert t.clef.change == False
   #assert isinstance(t.clef.effective, stafftools.Clef)
   #assert t.clef.forced is None
   #assert t.clef.effective == stafftools.Clef('treble')
   assert t.clef.effective is None


def test_Staff_clef_02( ):

   t = Staff(Note(0, (1, 4)) * 8)
   #t.clef.forced = stafftools.Clef('bass')
   marktools.ClefMark('bass')(t)

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

   assert t.format == '''\\new Staff {\n\t\\clef "bass"\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n}'''


def test_Staff_clef_03( ):

   t = Staff([ ])
   #t.clef.forced = stafftools.Clef('bass')
   marktools.ClefMark('bass')(t)

#   r'''
#   \new Staff {
#      \clef "bass"
#   }
#   '''
#
#   assert t.format == '\\new Staff {\n\t\\clef "bass"\n}'


def test_Staff_clef_04( ):
   '''Staff clef carries over to staff-contained leaves.
   '''

   staff = Staff(macros.scale(4))
   #staff.clef.forced = stafftools.Clef('bass')
   marktools.ClefMark('bass')(staff)

   for note in staff:
      assert note.clef.effective == marktools.ClefMark('bass')


def test_Staff_clef_05( ):
   '''Staff cleff carries over to staff-contained leaves,
   but leaves can reassert new clef.
   '''

   t = Staff(macros.scale(8))
   #t.clef.forced = stafftools.Clef('bass')
   #t[4].clef.forced = stafftools.Clef('treble')
   marktools.ClefMark('bass')(t)
   marktools.ClefMark('treble')(t[4])
   for i, leaf in enumerate(t):
      if i in (0, 1, 2, 3):
         #assert leaf.clef.effective == stafftools.Clef('bass')
         assert leaf.clef.effective == marktools.ClefMark('bass')
      else:
         #assert leaf.clef.effective == stafftools.Clef('treble')
         assert leaf.clef.effective == marktools.ClefMark('treble')


def test_Staff_clef_06( ):
   '''Detach clef.
   '''

   t = Staff(macros.scale(4))
   #t.clef.forced = stafftools.Clef('bass')
   #t.clef.forced = None
   clef = marktools.ClefMark('bass')(t)
   clef( )
   for leaf in t:
      #assert leaf.clef.effective == stafftools.Clef('treble')
      assert leaf.clef.effective is None


def test_Staff_clef_07( ):
   #'''Staff / first-leaf clef competition resolves
   #in favor of first leaf.'''
   '''Clef contention raises extra mark error.
   '''
   
   py.test.skip('fix and make sure clef contention raises exception at format time.')
   t = Staff(macros.scale(4))
   #t.clef.forced = stafftools.Clef('treble')
   #t[0].clef.forced = stafftools.Clef('bass')
   marktools.ClefMark('treble')(t)
   marktools.ClefMark('bass')(t[0])
   for leaf in t:
      #assert leaf.clef.effective == stafftools.Clef('bass')
      assert py.test.raises(ExtraMarkError, 'leaf.clef.effective')
