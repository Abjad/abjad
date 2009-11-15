from abjad.core.abjadcore import _Abjad


class Function(_Abjad):
   '''Wrapper for names of Scheme functions known to LilyPond.
   '''

   def __init__(self, name = '', *args):
      '''Initialize function name.'''
      self.name = name
      self.args = [ ]
      self.args.extend(args)

   ## PUBLIC ATTRIBUTES ##
   
   @property
   def format(self):
      '''LilyPond input representation of function.'''
      if len(self.args) == 0:
         return self.name
      elif len(self.args) == 1:
         if isinstance(self.args[0], (int, float, long)):
            return "(%s %s)" % (self.name, self.args[0])
         elif isinstance(self.args[0], str):
            return "(%s '%s)" % (self.name, self.args[0])
      ## TODO: Generalize for many arguments + parsing ##
      elif 1 < len(args):
         raise ValueError('multiple scheme arguments not yet implemented.')
