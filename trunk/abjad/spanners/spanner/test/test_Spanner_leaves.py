from abjad import *
import py.test


def test_Spanner_leaves_01( ):
   '''Spanner attaching to container knows about both container and 
      also leaves in container.'''

   t = Voice(leaftools.make_repeated_notes(4))
   pitchtools.chromaticize(t)
   p = Spanner(t)

   assert len(p.components) == 1
   assert p.components[0] is t
   assert len(p.leaves) == 4
   for i, leaf in enumerate(p.leaves):
      assert leaf is t[i]
   assert p.duration.prolated == Rational(4, 8)
   

def test_Spanner_leaves_02( ):
   '''Spanner attaching only to leaves makes p.components and p.leaves
      hold the same references.'''

   t = Voice(leaftools.make_repeated_notes(4))
   pitchtools.chromaticize(t)
   p = Spanner(t[:])
   
   assert len(p.components) == 4
   assert len(p.leaves) == 4
   for i, leaf in enumerate(p.leaves):
      assert leaf is t[i]
   assert p.duration.prolated == Rational(4, 8)


def test_Spanner_leaves_03( ):
   '''Spanner attaching to empty container knows about container
      and also about empty leaves.'''

   t = Voice([ ])
   p = Spanner(t)

   assert len(p.components) == 1
   assert p.components[0] is t
   assert len(p.leaves) == 0
   assert p.duration.prolated == Rational(0)


def test_Spanner_leaves_04( ):
   '''Spanner attaching to container with multidimensional contents.'''

   t = Voice(leaftools.make_repeated_notes(4))
   t.insert(1, Container(leaftools.make_repeated_notes(2)))
   t.insert(3, Container(leaftools.make_repeated_notes(2)))
   pitchtools.chromaticize(t)
   p = Spanner(t)

   r'''
   \new Voice {
      c'8
      {
         cs'8
         d'8
      }
      ef'8
      {
         e'8
         f'8
      }
      fs'8
      g'8
   }
   '''

   assert len(p.components) == 1
   assert len(p.leaves) == 8
   for i, leaf in enumerate(t.leaves):
      assert leaf is t.leaves[i]
   assert p.duration.prolated == Rational(8, 8)
   

def test_Spanner_leaves_05( ):
   '''Spanner spanning a mixture of containers and leaves.'''
   
   t = Voice(leaftools.make_repeated_notes(4))
   t.insert(1, Container(leaftools.make_repeated_notes(2)))
   t.insert(3, Container(leaftools.make_repeated_notes(2)))
   pitchtools.chromaticize(t)
   p = Spanner(t[0:3])

   r'''
   \new Voice {
      c'8
      {
         cs'8
         d'8
      }
      ef'8
      {
         e'8
         f'8
      }
      fs'8
      g'8
   }
   '''

   assert len(p.components) == 3
   assert p.components[0] is t[0]
   assert p.components[1] is t[1]
   assert p.components[2] is t[2]
   assert len(p.leaves) == 4
   for i, leaf in enumerate(p.leaves):
      assert leaf is t.leaves[i]
   assert p.duration.prolated == Rational(4, 8)


def test_Spanner_leaves_06( ):
   '''Spanner attaching to container with some parallel contents.
      Spanner absolutely does not descend into parallel container.
      Spanner duration does, however, account for parallel duration.'''

   t = Staff(leaftools.make_repeated_notes(4))
   t.insert(2, Container(Voice(leaftools.make_repeated_notes(2)) * 2))
   t[2].parallel = True
   pitchtools.chromaticize(t)

   r'''
   \new Staff {
      c'8
      cs'8
      <<
         \new Voice {
            d'8
            ef'8
         }
         \new Voice {
            e'8
            f'8
         }
      >>
      fs'8
      g'8
   }
   '''

   assert py.test.raises(AssertionError, 'p = Spanner(t)')
#   assert len(p.components) == 1
#   assert p.components[0] is t
#   assert len(p.leaves) == 4
#   assert p.leaves[0] is t[0]
#   assert p.leaves[1] is t[1]
#   assert p.leaves[2] is t[3]
#   assert p.leaves[3] is t[4]
#   assert p.duration.prolated == Rational(6, 8)


def test_Spanner_leaves_07( ):
   '''Spanner attaching to mixture of parallel and leaf components.
      Spanner absolutely does not descend into parallel container.
      Spanner duration does, however, account for parallel duration.'''

   t = Staff(leaftools.make_repeated_notes(4))
   t.insert(2, Container(Voice(leaftools.make_repeated_notes(2)) * 2))
   t[2].parallel = True
   pitchtools.chromaticize(t)

   r'''
   \new Staff {
      c'8
      cs'8
      <<
         \new Voice {
            d'8
            ef'8
         }
         \new Voice {
            e'8
            f'8
         }
      >>
      fs'8
      g'8
   }
   '''

   assert py.test.raises(AssertionError, 'p = Spanner(t[:])')
#   for i, component in enumerate(t[:]):
#      assert component is t[i]
#   assert len(p.leaves) == 4
#   assert p.leaves[0] is t[0]
#   assert p.leaves[1] is t[1]
#   assert p.leaves[2] is t[3]
#   assert p.leaves[3] is t[4]
#   assert p.duration.prolated == Rational(6, 8)
