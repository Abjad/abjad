from abjad import *


def test_fuse_leaves_by_reference_01( ):
   '''Wokrs with list of leaves.'''
   fused = fuse.leaves_by_reference(leaftools.make_repeated_notes(8, Rational(1, 4)))
   assert len(fused) == 1 
   assert fused[0].duration.written == Rational(2)


def test_fuse_leaves_by_reference_02( ):
   '''Works with Leaf component.'''
   fused = fuse.leaves_by_reference([Note(0, (1, 4))])
   assert len(fused) == 1 
   assert fused[0].duration.written == Rational(1, 4) 


def test_fuse_leaves_by_reference_03( ):
   '''Works with containers.'''
   t = Voice(Note(0, (1, 4)) * 8)
   fused = fuse.leaves_by_reference(t[:])
   assert len(fused) == 1 
   assert fused[0].duration.written == 2 
   assert t[0] is fused[0]


def test_fuse_leaves_by_reference_04( ):
   '''Fusion results in tied notes.'''
   t = Voice([Note(0, (2, 16)), Note(9, (3, 16))])
   fused = fuse.leaves_by_reference(t[:])
   assert len(fused) == 2 
   assert fused[0].duration.written == Rational(1, 4) 
   assert fused[1].duration.written == Rational(1, 16) 
   assert fused[0].tie.spanner is fused[1].tie.spanner
   assert t[0] is fused[0]
   assert t[1] is fused[1]
   assert t[0].pitch.number == t[1].pitch.number


def test_fuse_leaves_by_reference_05( ):
   '''Fuse leaves with differing LilyPond multipliers.'''

   t = Staff([Skip((1, 1)), Skip((1, 1))])
   t[0].duration.multiplier = Rational(1, 16)
   t[1].duration.multiplier = Rational(5, 16)

   r'''
   \new Staff {
           s1 * 1/16
           s1 * 5/16
   }
   '''

   assert t.duration.prolated == Rational(3, 8)

   result = fuse.leaves_by_reference(t[:])

   r'''
   \new Staff {
           s1 * 3/8
   }
   '''

   assert check.wf(t)
   assert len(result) == 1
   assert t.duration.prolated == Rational(3, 8)
