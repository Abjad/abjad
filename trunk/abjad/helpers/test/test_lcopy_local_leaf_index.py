from abjad import *


def test_lcopy_local_leaf_index_01( ):
   '''Copy consecutive leaves from tuplet in staff;
      pass start and stop indices local to tuplet.'''

   t = Staff(FixedDurationTuplet((2, 8), run(3)) * 2)
   diatonicize(t)

   r'''
   \new Staff {
           \times 2/3 {
                   c'8
                   d'8
                   e'8
           }
           \times 2/3 {
                   f'8
                   g'8
                   a'8
           }
   }
   '''

   u = lcopy(t[1], 1, 3)

   r'''
   \new Staff {
           \times 2/3 {
                   g'8
                   a'8
           }
   }
   '''

   assert check(t)
   assert check(u)
   assert u.format == "\\new Staff {\n\t\\times 2/3 {\n\t\tg'8\n\t\ta'8\n\t}\n}"


def test_lcopy_local_leaf_index_02( ):
   '''Copy consecutive leaves from measure in staff;
      pass start and stop indices local to measure.'''

   t = Staff(RigidMeasure((3, 8), run(3)) * 2)
   diatonicize(t)

   r'''
   \new Staff {
                   \time 3/8
                   c'8
                   d'8
                   e'8
                   \time 3/8
                   f'8
                   g'8
                   a'8
   }
   '''

   u = lcopy(t[1], 1, 3)

   r'''
   \new Staff {
                   \time 2/8
                   g'8
                   a'8
   }
   '''

   assert check(t)
   assert check(u)
   assert u.format == "\\new Staff {\n\t\t\\time 2/8\n\t\tg'8\n\t\ta'8\n}"   


def test_lcopy_local_leaf_index_03( ):
   '''Copy consecutive leaves from nonbinary measure in staff;
      pass start and stop indices local to measure.'''

   t = Staff(RigidMeasure((3, 9), run(3)) * 2)
   diatonicize(t)

   r'''
   \new Staff {
                   \time 3/9
                   \scaleDurations #'(8 . 9) {
                           c'8
                           d'8
                           e'8
                   }
                   \time 3/9
                   \scaleDurations #'(8 . 9) {
                           f'8
                           g'8
                           a'8
                   }
   }
   '''

   u = lcopy(t[1], 1, 3)

   r'''
   \new Staff {
                   \time 2/9
                   \scaleDurations #'(8 . 9) {
                           g'8
                           a'8
                   }
   }
   '''
   
   assert check(t)
   assert check(u)
   assert u.format == "\\new Staff {\n\t\t\\time 2/9\n\t\t\\scaleDurations #'(8 . 9) {\n\t\t\tg'8\n\t\t\ta'8\n\t\t}\n}"
