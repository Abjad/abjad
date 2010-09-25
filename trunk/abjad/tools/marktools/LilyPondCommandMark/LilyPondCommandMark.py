from abjad.tools import stringtools
from abjad.tools.marktools.Mark import Mark


class LilyPondCommandMark(Mark):
   r'''.. versionadded:: 1.1.2

   LilyPond command mark::

      abjad> staff = Staff(macros.scale(4))
      abjad> slur = spannertools.SlurSpanner(staff.leaves)
      abjad> lilypond_command = marktools.LilyPondCommandMark('slurDotted')(staff[0])
      abjad> f(staff)
      \new Staff {
         \slurDotted
         c'8 (
         d'8
         e'8
         f'8 )
      }

   .. todo:: allow LilyPondCommandMark objects to attach to spanners.
   '''

   #_format_slot = 'opening'

   def __init__(self, command_name_string, format_slot = 'opening', target_context = None):
      Mark.__init__(self, target_context = target_context)
      if self.target_context is None:
         self._is_cosmetic_mark = True
      self._command_name_string = command_name_string
      self._contents_repr_string = "'%s'" % command_name_string
      self._format_slot = format_slot

   ## OVERLOADS ##
   
   def __copy__(self, *args):
      return type(self)(self._command_name_string, target_context = self.target_context)

   __deepcopy__ = __copy__

   def __eq__(self, arg):
      if isinstance(arg, type(self)):
         return self._command_name_string == arg._command_name_string
      return False

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self):
      '''Format-time contribution of LilyPondCommandMark:

      ::

         abjad> note = Note(0, (1, 4))
         abjad> lilypond_command = marktools.LilyPondCommandMark('slurDotted')(note)
         abjad> lilypond_command.format
         '\\slurDotted'
      '''
      command = stringtools.underscore_delimited_lowercase_to_lowercamelcase(
         self._command_name_string)
      return r'\%s' % command
