from abjad.tools.contexttools.Mark import Mark


class StaffChangeMark(Mark):
   '''.. versionadded:: 1.1.2
   '''

   _format_slot = 'opening'

   def __init__(self, staff, target_context = None):
      from abjad.components import Staff
      Mark.__init__(self, target_context = target_context)
      if self.target_context is None:
         self._target_context = Staff
      self._staff = staff
      self._contents_repr_string = repr(staff)

   ## OVERLOADS ##

   def __copy__(self, *args):
      return type(self)(self.staff, target_context = self.target_context)

   def __eq__(self, arg):
      if isinstance(arg, type(self)):
         return self.staff is arg.staff
      return False

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self):
      return r'\change Staff = %s' % self.staff.name

   @property
   def staff(self):
      return self._staff
