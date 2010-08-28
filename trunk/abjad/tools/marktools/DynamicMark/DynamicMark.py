from abjad.tools.marktools.Mark import Mark


class DynamicMark(Mark):
   '''.. versionadded:: 1.1.2
   '''

   _format_slot = 'right'

   def __init__(self, dynamic_name_string, target_context = None):
      from abjad.components import Staff
      Mark.__init__(self, target_context = target_context)
      if self.target_context is None:
         self._target_context = Staff
      self._dynamic_name_string = dynamic_name_string
      self._contents_repr_string = "'%s'" % dynamic_name_string

   ## OVERLOADS ##

   def __copy__(self, *args):
      return type(self)(self._dynamic_name_string, target_contex = self.target_context)

   def __eq__(self, arg):
      if isinstance(arg, type(self)):
         return self._dynamic_name_string == arg._dynamic_name_string
      return False

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self):
      return r'\%s' % self._dynamic_name_string
