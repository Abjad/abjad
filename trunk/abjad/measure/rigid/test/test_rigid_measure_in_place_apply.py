from abjad import *
from abjad.checks import MeasuresMisdurated
checker = MeasuresMisdurated( )



def test_measure_in_place_apply_01( ):

   t = Voice([Note(n, (1, 8)) for n in range(8)])
   leaves_before = t.leaves
   RigidMeasure((4, 8), t[0 : 4])
   leaves_after = t.leaves

   assert len(t) == 5
   assert leaves_before == leaves_after
   for i, x in enumerate(t):
      if i == 0:
         assert isinstance(x, RigidMeasure)
      else:
         assert isinstance(x, Note)
   assert checker.check(t)


def test_measure_in_place_apply_02( ):

   t = Staff([Note(n, (1, 8)) for n in range(8)])
   leaves_before = t.leaves
   RigidMeasure((4, 8), t[0 : 4])
   leaves_after = t.leaves

   assert len(t) == 5
   assert leaves_before == leaves_after
   for i, x in enumerate(t):
      if i == 0:
         assert isinstance(x, RigidMeasure)
      else:
         assert isinstance(x, Note)
   assert checker.check(t)


def test_measure_in_place_apply_03( ):

   t = Staff([Note(n, (1, 1)) for n in range(4)])
   leaves_before = t.leaves
   RigidMeasure((1, 1), t[0 : 1])
   leaves_after = t.leaves

   assert len(t) == 4
   assert leaves_before == leaves_after
   for i, x in enumerate(t):
      if i == 0:
         assert isinstance(x, RigidMeasure)
      else:
         assert isinstance(x, Note)
   assert checker.check(t)


def test_measure_in_place_apply_04( ):

   t = Staff([Note(n, (1, 1)) for n in range(4)])
   RigidMeasure((1, 1), t[:1])
   RigidMeasure((1, 1), t[1:2])
   RigidMeasure((1, 1), t[2:3])
   RigidMeasure((1, 1), t[3:])

   r'''
   \new Staff {
           {
                   \time 1/1
                   c'1
           }
           {
                   \time 1/1
                   cs'1
           }
           {
                   \time 1/1
                   d'1
           }
           {
                   \time 1/1
                   ef'1
           }
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t{\n\t\t\\time 1/1\n\t\tc'1\n\t}\n\t{\n\t\t\\time 1/1\n\t\tcs'1\n\t}\n\t{\n\t\t\\time 1/1\n\t\td'1\n\t}\n\t{\n\t\t\\time 1/1\n\t\tef'1\n\t}\n}"
