from abjad import *


def test_MeterInterface_grob_handling_01( ):
   '''Transparent meter on staff.'''

   t = Staff(macros.scale(4))
   t.override.time_signature.transparent = True

   r'''
   \new Staff \with {
           \override TimeSignature #'transparent = ##t
   } {
           c'8
           d'8
           e'8
           f'8
   }
   '''

   assert t.format == "\\new Staff \\with {\n\t\\override TimeSignature #'transparent = ##t\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_MeterInterface_grob_handling_02( ):
   '''(Nonpromoted) transparent meter on measure.'''

   t = Measure((4, 8), macros.scale(4))
   t.override.time_signature.transparent = True

   r'''
   {
           \override TimeSignature #'transparent = ##t
           \time 4/8
           c'8
           d'8
           e'8
           f'8
           \revert TimeSignature #'transparent
   }
   '''

   assert t.format == "{\n\t\\override TimeSignature #'transparent = ##t\n\t\\time 4/8\n\tc'8\n\td'8\n\te'8\n\tf'8\n\t\\revert TimeSignature #'transparent\n}"


def test_MeterInterface_grob_handling_03( ):
   '''Promoted transarent meter on measure.'''

   t = Measure((4, 8), macros.scale(4))
   t.override.staff.time_signature.transparent = True

   r'''
   {
           \override Staff.TimeSignature #'transparent = ##t
           \time 4/8
           c'8
           d'8
           e'8
           f'8
           \revert Staff.TimeSignature #'transparent
   }
   '''

   assert t.format == "{\n\t\\override Staff.TimeSignature #'transparent = ##t\n\t\\time 4/8\n\tc'8\n\td'8\n\te'8\n\tf'8\n\t\\revert Staff.TimeSignature #'transparent\n}"


def test_MeterInterface_grob_handling_04( ):
   '''Clear all meter overrides.'''

   t = Note(0, (1, 4))
   t.override.time_signature.color = 'red'
   t.override.time_signature.transparent = True
   del(t.override.time_signature)

   assert t.format == "c'4"
