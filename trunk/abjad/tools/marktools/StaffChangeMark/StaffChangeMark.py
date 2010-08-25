from abjad.tools.marktools.Mark import Mark


class StaffChangeMark(Mark):
   '''.. versionadded:: 1.1.2
   '''

   _format_slot = 'opening'

   def __init__(self, staff):
      Mark.__init__(self)
      self._staff = staff
      self._contents_repr_string = repr(staff)

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self):
      return r'\change Staff = %s' % self.staff.name

   @property
   def staff(self):
      return self._staff
