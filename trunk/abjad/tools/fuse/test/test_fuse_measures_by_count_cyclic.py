from abjad import *

import py.test
py.test.skip('measure redo')


def test_fuse_measures_by_count_cyclic_01( ):
   '''Docs.'''

   t = Staff(RigidMeasure((2, 8), construct.run(2)) * 5)
   pitchtools.diatonicize(t) 

   r'''\new Staff {
                   \time 2/8
                   c'8
                   d'8
                   \time 2/8
                   e'8
                   f'8
                   \time 2/8
                   g'8
                   a'8
                   \time 2/8
                   b'8
                   c''8
                   \time 2/8
                   d''8
                   e''8
   }'''

   part_counts = (2, 1)
   fuse.measures_by_count_cyclic(t, part_counts)

   r'''\new Staff {
                   \time 4/8
                   c'8
                   d'8
                   e'8
                   f'8
                   \time 2/8
                   g'8
                   a'8
                   \time 4/8
                   b'8
                   c''8
                   d''8
                   e''8
   }'''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t\t\\time 4/8\n\t\tc'8\n\t\td'8\n\t\te'8\n\t\tf'8\n\t\t\\time 2/8\n\t\tg'8\n\t\ta'8\n\t\t\\time 4/8\n\t\tb'8\n\t\tc''8\n\t\td''8\n\t\te''8\n}"


def test_fuse_measures_by_count_cyclic_02( ):
   '''Docs.'''

   t = Staff(RigidMeasure((2, 8), construct.run(2)) * 5)
   pitchtools.diatonicize(t) 

   r'''\new Staff {
                   \time 2/8
                   c'8
                   d'8
                   \time 2/8
                   e'8
                   f'8
                   \time 2/8
                   g'8
                   a'8
                   \time 2/8
                   b'8
                   c''8
                   \time 2/8
                   d''8
                   e''8
   }'''

   part_counts = (3, )
   fuse.measures_by_count_cyclic(t, part_counts)

   r'''\new Staff {
                   \time 6/8
                   c'8
                   d'8
                   e'8
                   f'8
                   g'8
                   a'8
                   \time 4/8
                   b'8
                   c''8
                   d''8
                   e''8
   }'''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t\t\\time 6/8\n\t\tc'8\n\t\td'8\n\t\te'8\n\t\tf'8\n\t\tg'8\n\t\ta'8\n\t\t\\time 4/8\n\t\tb'8\n\t\tc''8\n\t\td''8\n\t\te''8\n}"
