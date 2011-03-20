from abjad.tools.marktools.Mark import Mark


## TODO: extend LilyPond command marks to attach to spanners.
class LilyPondCommandMark(Mark):
   r'''.. versionadded:: 1.1.2

   LilyPond command mark::

      abjad> staff = Staff(macros.scale(4))
      abjad> slur = spannertools.SlurSpanner(staff.leaves)

   ::

      abjad> lilypond_command = marktools.LilyPondCommandMark('slurDotted')(staff[0])

   ::

      abjad> f(staff)
      \new Staff {
         \slurDotted
         c'8 (
         d'8
         e'8
         f'8 )
      }

   LilyPond command marks are immutable.
   '''

   __slots__ = ('_command_name_string', '_format_slot', )

   def __init__(self, command_name_string, format_slot = 'opening'):
      Mark.__init__(self)
      self._command_name_string = command_name_string
      self._format_slot = format_slot

   ## OVERLOADS ##
   
   def __copy__(self, *args):
      return type(self)(self._command_name_string)

   __deepcopy__ = __copy__

   def __eq__(self, arg):
      if isinstance(arg, type(self)):
         return self._command_name_string == arg._command_name_string
      return False

   ## PRIVATE ATTRIBUTES ##

   @property
   def _contents_repr_string(self):
      return repr(self.command_name_string)

   ## PUBLIC ATTRIBUTES ##

   @property
   def command_name_string(self):
      '''Read-only command name string of LilyPond command mark:

      ::

         abjad> command_mark = marktools.LilyPondCommandMark('slurDotted')
         abjad> command_mark.command_name_string
         'slurDotted'
      '''
      return self._command_name_string

   @property
   def format(self):
      '''Read-only LilyPond input format of LilyPond command mark:

      ::

         abjad> note = Note(0, (1, 4))
         abjad> lilypond_command = marktools.LilyPondCommandMark('slurDotted')(note)
         abjad> lilypond_command.format
         '\\slurDotted'
      '''
      from abjad.tools import iotools
      command = self._command_name_string
      if command.startswith('#'):
         return command
      else:
         return '\\' + iotools.underscore_delimited_lowercase_to_lowercamelcase(command)
