from abjad import *


def test_measuretools_append_spacer_skips_to_underfull_measures_in_01( ):

   t = Staff(RigidMeasure((3, 8), construct.scale(3)) * 3)
   t[1].meter.forced = Meter(4, 8)
   t[2].meter.forced = Meter(5, 8)

   assert not t[0].duration.is_underfull
   assert t[1].duration.is_underfull
   assert t[2].duration.is_underfull

   measuretools.append_spacer_skips_to_underfull_measures_in(t)

   r'''
   \new Staff {
           {
                   \time 3/8
                   c'8
                   d'8
                   e'8
           }
           {
                   \time 4/8
                   c'8
                   d'8
                   e'8
                   s1 * 1/8
           }
           {
                   \time 5/8
                   c'8
                   d'8
                   e'8
                   s1 * 1/4
           }
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t{\n\t\t\\time 3/8\n\t\tc'8\n\t\td'8\n\t\te'8\n\t}\n\t{\n\t\t\\time 4/8\n\t\tc'8\n\t\td'8\n\t\te'8\n\t\ts1 * 1/8\n\t}\n\t{\n\t\t\\time 5/8\n\t\tc'8\n\t\td'8\n\t\te'8\n\t\ts1 * 1/4\n\t}\n}"
