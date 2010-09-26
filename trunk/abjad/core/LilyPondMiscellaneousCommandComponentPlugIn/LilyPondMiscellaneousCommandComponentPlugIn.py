from abjad.tools import stringtools


class LilyPondMiscellaneousCommandComponentPlugIn(object):

   def __init__(self):
      pass

   _known_lilypond_miscellaneous_commands = {
      'bar': (r'\bar "%s"', 'closing'),
      'flageolet': (r'\flageolet', 'right'),
      'set_accidental_style': (r"#(set-accidental-style '%s)", 'opening'),
      'voice_one': (r'\voiceOne', 'opening'),
      'voice_two': (r'\voiceTwo', 'opening'),
      'voice_three': (r'\voiceThree', 'opening'),
      'voice_four': (r'\voiceFour', 'opening'),
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
         vars(self)[name] = value

   ## PRIVATE METHODS ##

   def _get_formatted_commands_for_target_slot(self, target_slot):
      result = [ ]
      for command_name, command_value in vars(self).iteritems( ):
         ## known LilyPond command with known formatting and slot
         try:
            format_string, command_slot = \
               type(self)._known_lilypond_miscellaneous_commands[command_name]
            if command_slot == target_slot:
               if command_value is None:
                  result.append(format_string)
               else:
                  result.append(format_string % command_value)
         ## unknown LilyPond command
         except KeyError:
            ## put unkonwn command in opening slot
            if target_slot == 'opening':
               formatted_command = \
                  stringtools.underscore_delimited_lowercase_to_lowercamelcase(command_name)
               result.append(r'\%s' % formatted_command)
      return result
