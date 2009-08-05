from abjad.core.abjadcore import _Abjad


class Function(_Abjad):
   '''Wrapper for names of *Scheme* functions known to *LilyPond*.'''

   def __init__(self, name = '', *args):
      '''Initialize function name.'''
      self.name = name
      self.args = [ ]
      self.args.extend(args)

   ## PUBLIC ATTRIBUTES ##
   
   @property
   def format(self):
      '''*LilyPond* input representation of function.'''
      if not self.args:
         return self.name
      else:
         ## TODO: Generalize for many arguments + parsing ##
         return "(%s '%s)" % (self.name, self.args[0])
