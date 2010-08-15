from abjad import *


def test_AccidentalInterface_suggest_accidentals_01( ):
   '''AccidentalInterface.suggest_accidentals interfaces with
   LilyPond suggestAccidentals context setting. Formats with-block
   of contexts like staff.
   '''

   t = Staff(macros.scale(4))
   t.set.suggest_accidentals = True

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

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Staff \\with {\n\tsuggestAccidentals = ##t\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_AccidentalInterface_suggest_accidentals_02( ):
   '''Format inline before leaves.'''

   t = Staff(macros.scale(4))
   t[1].set.suggest_accidentals = True
   
   r'''
   \new Staff {
           c'8
           \set suggestAccidentals = ##t
           d'8
           e'8
           f'8
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Staff {\n\tc'8\n\t\\set suggestAccidentals = ##t\n\td'8\n\te'8\n\tf'8\n}"
