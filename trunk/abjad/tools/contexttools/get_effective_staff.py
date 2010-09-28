from abjad.tools.contexttools.StaffChangeMark import StaffChangeMark
from abjad.tools.contexttools.get_effective_mark import get_effective_mark


def get_effective_staff(component):
   '''.. versionadded:: 1.1.2

   .. versionchanged:: 1.1.2
      renamed ``marktools.get_effective_staff( )`` to
      ``contexttools.get_effective_staff( )``.
   '''
   from abjad.components import Staff
   from abjad.tools import componenttools
   
   staff_change_mark = get_effective_mark(component, StaffChangeMark)
   if staff_change_mark is not None:
      return staff_change_mark.staff

   return componenttools.get_first_instance_of_klass_in_improper_parentage_of_component(
      component, Staff)
