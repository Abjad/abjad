from abjad.tools.marktools.Mark import Mark


class DynamicMark(Mark):
   '''.. versionadded:: 1.1.2

   Dynamic mark.
   '''

   _format_slot = 'right'

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self):
      return r'\%s' % self.value
