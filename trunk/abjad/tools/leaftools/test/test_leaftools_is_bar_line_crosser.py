from abjad import *


def test_leaftools_is_bar_line_crosser_01( ):

   t = Staff(construct.scale(4))
   t[2].duration.written *= 2
   meter = Meter(2, 8)
   meter.partial = Rational(1, 8)
   t.meter.forced = meter   


   r'''
   \new Staff {
           \time 2/8
           \partial 8
           c'8
           d'8
           e'4
           f'8
   }
   '''

   assert not leaftools.is_bar_line_crosser(t[0])
   assert not leaftools.is_bar_line_crosser(t[1])
   assert leaftools.is_bar_line_crosser(t[2])
   assert not leaftools.is_bar_line_crosser(t[3])
