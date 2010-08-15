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
         raise AttributeError("unkown LilyPond command '%s'." % name)

   ## PRIVATE METHODS ##

   def _get_formatted_commands_for_target_slot(self, target_slot):
      result = [ ]
      for command_name, command_value in vars(self).iteritems( ):
         format_string, command_slot = \
            type(self)._known_lilypond_miscellaneous_commands[command_name]
         if command_slot == target_slot:
            result.append(format_string % command_value)
      return result
