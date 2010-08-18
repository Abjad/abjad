from abjad import *
import py.test


def test_Container_parallel_01( ):
   '''True when container encloses contents in LilyPond << >> brackets,
      otherwise False.'''

   assert not Container([ ]).parallel
   assert not tuplettools.FixedDurationTuplet((2, 8), [ ]).parallel
   assert not Tuplet((2, 3), [ ]).parallel
   assert scoretools.GrandStaff([ ]).parallel
   assert not stafftools.make_rhythmic_sketch_staff([ ]).parallel
   assert not stafftools.make_rhythmic_staff([ ]).parallel
   assert not Measure((4, 8), [ ]).parallel
   assert Score([ ]).parallel
   assert not Container([ ]).parallel
   assert not Staff([ ]).parallel
   assert scoretools.StaffGroup([ ]).parallel
   assert not Voice([ ]).parallel


def test_Container_parallel_02( ):
   '''True when container encloses contents in LilyPond << >> brackets,
      otherwise False.'''

   t = Container([ ])
   t.parallel = True
   assert t.parallel


def test_Container_parallel_03( ):
   '''Container 'parallel' is settable.'''

   t = Container([ ])
   assert not t.parallel

   t.parallel = True
   assert t.parallel


def test_Container_parallel_04( ):
   '''A parallel container can hold Contexts.'''
   t = Container(Voice(notetools.make_repeated_notes(2)) * 2)
   macros.chromaticize(t)
   t.parallel = True
   assert t.format == "<<\n\t\\new Voice {\n\t\tc'8\n\t\tcs'8\n\t}\n\t\\new Voice {\n\t\td'8\n\t\tef'8\n\t}\n>>"

   r'''
   <<
           \new Voice {
                   c'8
                   cs'8
           }
           \new Voice {
                   d'8
                   ef'8
           }
   >>
   '''


## Parallel Errors ##

def test_Container_parallel_05( ):
   '''Parallel containers must contain only Contexts.
   It cannot take leaves.'''

   t = Container(notetools.make_repeated_notes(4))
   py.test.raises(AssertionError, 't.parallel = True')


def test_Container_parallel_06( ):
   '''Parallel containers must contain only Contexts.
   It cannot take Containers.'''

   t = Container(Container(notetools.make_repeated_notes(4)) * 2)
   py.test.raises(AssertionError, 't.parallel = True')
