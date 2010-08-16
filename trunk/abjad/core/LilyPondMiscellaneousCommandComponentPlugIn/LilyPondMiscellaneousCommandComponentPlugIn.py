class LilyPondMiscellaneousCommandComponentPlugIn(object):

   def __init__(self):
      pass

   _known_lilypond_miscellaneous_commands = {
      'bar': (r'\bar "%s"', 'closing'),
      'set_accidental_style': (r"#(set-accidental-style '%s)", 'opening'),
   }

   ## OVERLOADS ##

   def __repr__(self):
      return '%s( )' % self.__class__.__name__

   def __setattr__(self, name, value):
      if name.startswith('_'):
         vars(self)[name] = value
      elif name in type(self)._known_lilypond_miscellaneous_commands.keys( ):
         vars(self)[name] = value
      else:
         #raise AttributeError("unkown LilyPond command '%s'." % name)
         vars(self)[name] = value

   ## PRIVATE METHODS ##

   def _get_formatted_commands_for_target_slot(self, target_slot):
      from abjad.tools.lilyfiletools._underscore_delimited_lowercase_to_lowercamelcase import \
         _underscore_delimited_lowercase_to_lowercamelcase
      result = [ ]
      for command_name, command_value in vars(self).iteritems( ):
         ## known LilyPond command with known formatting and slot
         try:
            format_string, command_slot = \
               type(self)._known_lilypond_miscellaneous_commands[command_name]
            if command_slot == target_slot:
               result.append(format_string % command_value)
         ## unknown LilyPond command
         except KeyError:
            ## put unkonwn command in opening slot
            if target_slot == 'opening':
               formatted_command = _underscore_delimited_lowercase_to_lowercamelcase(command_name)
               result.append(r'\%s' % formatted_command)
      return result
