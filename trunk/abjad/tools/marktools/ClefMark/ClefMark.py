from abjad.tools.marktools.Mark import Mark


class ClefMark(Mark):
   '''.. versionadded:: 1.1.2
   '''

   _format_slot = 'opening'
   #default_target_context = Staff

   def __init__(self, clef_name_string, target_context = None):
      from abjad.components import Staff
      Mark.__init__(self, target_context = target_context)
      if self.target_context is None:
         self._target_context = Staff
      self._clef_name_string = clef_name_string
      self._contents_repr_string = "'%s'" % clef_name_string

   ## OVERLOADS ##

   def __copy__(self, *args):
      return type(self)(self._clef_name_string, target_context = self.target_context)

   __deepcopy__ = __copy__

   def __eq__(self, arg):
      if isinstance(arg, type(self)):
         return self._clef_name_string == arg._clef_name_string
      return False

   ## PRIVATE ATTRIBUTES ##

   _clef_name_to_middle_c_position = { 'treble': -6, 'alto': 0, 'tenor': 2, 'bass': 6, }

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self): 
      return r'\clef "%s"' % self._clef_name_string

   @property
   def middle_c_position(self):
      return self._clef_name_to_middle_c_position[self._clef_name_string]
