from abjad import *


def test_meter_interface_grob_handling_01( ):
   '''Transparent meter on staff.'''

   t = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   t.meter.transparent = True

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


def test_meter_interface_grob_handling_02( ):
   '''(Nonpromoted) transparent meter on measure.'''

   t = RigidMeasure((4, 8), leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   t.meter.transparent = True

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


def test_meter_interface_grob_handling_03( ):
   '''Promoted transarent meter on measure.'''

   t = RigidMeasure((4, 8), leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   t.meter.transparent = True
   #t.meter.promote('transparent', 'Staff')
   overridetools.promote_attribute_to_context_on_grob_handler(t.meter, 'transparent', 'Staff')

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


def test_meter_interface_grob_handling_04( ):
   '''Clear all meter overrides.'''

   t = Note(0, (1, 4))
   t.meter.color = 'red'
   t.meter.transparent = True
   overridetools.clear_all_overrides_on_grob_handler(t.meter)

   assert t.format == "c'4"
