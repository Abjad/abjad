from abjad.tools.marktools.Mark import Mark


class ClefMark(Mark):
   '''.. versionadded:: 1.1.2

   Clef mark.
   '''

   _format_slot = 'opening'

   def __init__(self, clef_name):
      Mark.__init__(self, clef_name)
      self._contents_repr_string = "'%s'" % clef_name

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self): 
      return r'\clef "%s"' % self.value
