from abjad.tools.marktools.StaffChangeMark import StaffChangeMark
from abjad.tools.marktools.get_effective_mark import get_effective_mark


def get_effective_staff(component):
   '''.. versionadded:: 1.1.2
   '''
   from abjad.components import Staff
   from abjad.tools import componenttools
   
   staff_change_mark = get_effective_mark(component, StaffChangeMark)
   if staff_change_mark is not None:
      return staff_change_mark.staff

   return componenttools.get_first_instance_of_klass_in_improper_parentage_of_component(
      component, Staff)
