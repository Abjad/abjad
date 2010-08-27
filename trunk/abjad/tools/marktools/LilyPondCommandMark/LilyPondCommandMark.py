from abjad.tools import stringtools
from abjad.tools.marktools.Mark import Mark


class LilyPondCommandMark(Mark):
   '''.. versionadded:: 1.1.2
   '''

   _format_slot = 'opening'

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self):
      command = stringtools.underscore_delimited_lowercase_to_lowercamelcase(self.value)
      return r'\%s' % command
