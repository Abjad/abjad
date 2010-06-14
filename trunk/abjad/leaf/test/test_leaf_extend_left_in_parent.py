from abjad import *


def test_leaf_extend_left_in_parent_01( ):
   '''Extend leaves leftwards of leaf. Do not extend edge spanners.'''

   t = Voice(leaftools.make_first_n_notes_in_ascending_diatonic_scale(3))
   Beam(t[:])
   result = t[0].extend_left_in_parent(leaftools.make_first_n_notes_in_ascending_diatonic_scale(3, Rational(1, 16)))

   r'''
   \new Voice {
           c'16 
           d'16
           e'16
           c'8 [
           d'8
           e'8 ]
   }
   '''
   
   assert check.wf(t)
   assert result == t[:4]
   assert t.format == "\\new Voice {\n\tc'16\n\td'16\n\te'16\n\tc'8 [\n\td'8\n\te'8 ]\n}"


def test_leaf_extend_left_in_parent_02( ):
   '''Extend leaf leftwards of interior leaf. Do extend interior spanners.'''

   t = Voice(leaftools.make_first_n_notes_in_ascending_diatonic_scale(3))
   Beam(t[:])
   result = t[1].extend_left_in_parent([Note(1.5, (1, 8))])

   r'''
   \new Voice {
           c'8 [
           dqf'8
           d'8
           e'8 ]
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\tdqf'8\n\td'8\n\te'8 ]\n}"
   assert result == t[1:3]
