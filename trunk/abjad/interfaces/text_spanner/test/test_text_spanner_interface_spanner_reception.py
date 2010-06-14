from abjad import *


def test_text_spanner_interface_spanner_reception_01( ):

   t = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   text_spanner = TextSpanner(t[:])

   r'''
   \new Staff {
           c'8 \startTextSpan
           d'8
           e'8
           f'8 \stopTextSpan
   }
   '''

   assert check.wf(t)
   assert t[0].text_spanner.spanner is text_spanner
