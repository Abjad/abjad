from abjad import *
import py.test


def test_container_parallel_01( ):
   '''True when container encloses contents in LilyPond << >> brackets,
      otherwise False.'''

   assert not Container([ ]).parallel
   assert not FixedDurationTuplet((2, 8), [ ]).parallel
   assert not FixedMultiplierTuplet((2, 3), [ ]).parallel
   assert GrandStaff([ ]).parallel
   assert not RhythmicSketchStaff([ ]).parallel
   assert not RhythmicStaff([ ]).parallel
   assert not RigidMeasure((4, 8), [ ]).parallel
   assert Score([ ]).parallel
   assert not Container([ ]).parallel
   assert not Staff([ ]).parallel
   assert StaffGroup([ ]).parallel
   assert not Voice([ ]).parallel


def test_container_parallel_02( ):
   '''True when container encloses contents in LilyPond << >> brackets,
      otherwise False.'''

   t = Container([ ])
   t.parallel = True
   assert t.parallel


def test_container_parallel_03( ):
   '''Container 'parallel' is settable.'''

   t = Container([ ])
   assert not t.parallel

   t.parallel = True
   assert t.parallel


def test_container_parallel_04( ):
   '''A parallel container can hold Contexts.'''
   t = Container(Voice(construct.run(2)) * 2)
   pitchtools.chromaticize(t)
   t.parallel = True
   assert t.format == "<<\n\t\\new Voice {\n\t\tc'8\n\t\tcs'8\n\t}\n\t\\new Voice {\n\t\td'8\n\t\tef'8\n\t}\n>>"

   r'''<<
           \new Voice {
                   c'8
                   cs'8
           }
           \new Voice {
                   d'8
                   ef'8
           }
   >>'''


## Parallel Errors ##

def test_container_parallel_10( ):
   '''Parallel containers must contain only Contexts.
   It cannot take leaves.'''

   t = Container(construct.run(4))
   py.test.raises(TypeError, 't.parallel = True')


def test_container_parallel_11( ):
   '''Parallel containers must contain only Contexts.
   It cannot take Containers.'''

   t = Container(Container(construct.run(4)) * 2)
   py.test.raises(TypeError, 't.parallel = True')
