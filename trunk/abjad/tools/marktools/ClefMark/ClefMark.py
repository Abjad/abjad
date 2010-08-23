from abjad.tools.marktools.Mark import Mark


class ClefMark(Mark):
   '''.. versionadded:: 1.1.2

   Clef mark.
   '''

   _format_slot = 'opening'

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self): 
      return r'\clef "%s"' % self.value
