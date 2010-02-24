from abjad.core.abjadcore import _Abjad


class SchemeFunction(_Abjad):
   '''Wrapper for names of Scheme functions known to LilyPond.'''

   def __init__(self, name = '', *args):
      self.name = name
      self.args = [ ]
      self.args.extend(args)

   ## PUBLIC ATTRIBUTES ##
   
   @property
   def format(self):
      '''LilyPond input representation of function.'''
      if len(self.args) == 0:
         body = self.name
      elif len(self.args) == 1:
         if isinstance(self.args[0], (int, float, long)):
            body = "(%s %s)" % (self.name, self.args[0])
         elif isinstance(self.args[0], str):
            body = "(%s '%s)" % (self.name, self.args[0])
         else:
            raise ValueError
      ## TODO: Generalize for many arguments + parsing ##
      else:
         raise ValueError('multiple scheme arguments not yet implemented.')
      return '#' + body
