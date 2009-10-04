from abjad import *


def test_rigid_measure_number_01( ):
   '''Measures in staff number correctly starting from 1.'''

   t = Staff(measuretools.make([(3, 16), (5, 16), (5, 16)]))
   assert t[0].number == 1
   assert t[1].number == 2
   assert t[2].number == 3


def test_rigid_measure_number_02( ):
   '''Orphan measures number correctly starting from 1.'''

   t = RigidMeasure((3, 8), construct.scale(3))
   assert t.number == 1


def test_rigid_measure_number_03( ):
   '''Mesaure numbering works correctly after contents rotation.'''

   t = Staff(RigidMeasure((2, 8), construct.run(2)) * 3)
   pitchtools.diatonicize(t)
   
   assert t[0].number == 1
   assert t[1].number == 2
   assert t[2].number == 3

   contents = t[:]
   contents = listtools.rotate(contents, -1)
   t[:] = contents

   r'''
   \new Staff {
           {
                   \time 2/8
                   e'8
                   f'8
           }
           {
                   \time 2/8
                   g'8
                   a'8
           }
           {
                   \time 2/8
                   c'8
                   d'8
           }
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\te'8\n\t\tf'8\n\t}\n\t{\n\t\t\\time 2/8\n\t\tg'8\n\t\ta'8\n\t}\n\t{\n\t\t\\time 2/8\n\t\tc'8\n\t\td'8\n\t}\n}"

   assert t[0].number == 1
   assert t[1].number == 2
   assert t[2].number == 3
