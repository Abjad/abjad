from abjad import *


def test_SchemeFunction___init____01( ):
   '''Scheme function with only a name and no arguments.'''

   t = Staff(macros.scale(4))
   t.meter.break_visibility = schemetools.SchemeFunction(
      'end-of-line-invisible')

   r'''
   \new Staff \with {
      \override TimeSignature #'break-visibility = #end-of-line-invisible
   } {
      c'8
      d'8
      e'8
      f'8
   }
   '''

   assert t.format == "\\new Staff \\with {\n\t\\override TimeSignature #'break-visibility = #end-of-line-invisible\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_SchemeFunction___init____02( ):
   '''Scheme function with a name and a single numeric argument.'''

   staff = Staff(macros.scale(4))
   staff.staff.staff_space = schemetools.SchemeFunction('magstep', -3)
   staff.staff.thickness = schemetools.SchemeFunction('magstep', -3)

   r'''
   \new Staff \with {
           \override StaffSymbol #'staff-space = #(magstep -3)
           \override StaffSymbol #'thickness = #(magstep -3)
   } {
           c'8
           d'8
           e'8
           f'8
   }
   '''

   assert componenttools.is_well_formed_component(staff)
   assert staff.format == "\\new Staff \\with {\n\t\\override StaffSymbol #'staff-space = #(magstep -3)\n\t\\override StaffSymbol #'thickness = #(magstep -3)\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"
