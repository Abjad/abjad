from abjad import *


def test_container_parallel_01( ):
   '''True when container encloses contents in LilyPond << >> brackets,
      otherwise False.'''

   assert not Container([ ]).parallel
   assert not FixedDurationTuplet((2, 8), [ ]).parallel
   assert not FixedMultiplierTuplet((2, 3), [ ]).parallel
   assert GrandStaff([ ]).parallel
   assert Parallel([ ]).parallel
   assert not RhythmicSketchStaff([ ]).parallel
   assert not RhythmicStaff([ ]).parallel
   assert not RigidMeasure((4, 8), [ ]).parallel
   assert Score([ ]).parallel
   assert not Sequential([ ]).parallel
   assert not Staff([ ]).parallel
   assert StaffGroup([ ]).parallel
   assert not Voice([ ]).parallel


def test_container_parallel_02( ):
   '''True when container encloses contents in LilyPond << >> brackets,
      otherwise False.'''

   t = Container([ ])
   t.parallel = True
   assert t.parallel

   t = Container([ ])
   t.parallel = True
   assert t.parallel


def test_container_parallel_03( ):
   '''Container 'parallel' is settable.'''

   t = Container([ ])
   assert not t.parallel

   t.parallel = True
   assert t.parallel
