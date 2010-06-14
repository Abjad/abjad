from abjad import *


def test_accidental_interface_suggest_accidentals_01( ):
   '''AccidentalInterface.suggest_accidentals interfaces with
   LilyPond suggestAccidentals context setting. Formats with-block
   of contexts like staff.
   '''

   t = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   t.accidental.suggest_accidentals = True

   r'''
   \new Staff \with {
           suggestAccidentals = ##t
   } {
           c'8
           d'8
           e'8
           f'8
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Staff \\with {\n\tsuggestAccidentals = ##t\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_accidental_interface_suggest_accidentals_02( ):
   '''Format inline before leaves.'''

   t = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   t[1].accidental.suggest_accidentals = True
   
   r'''
   \new Staff {
           c'8
           \set suggestAccidentals = ##t
           d'8
           e'8
           f'8
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\tc'8\n\t\\set suggestAccidentals = ##t\n\td'8\n\te'8\n\tf'8\n}"
