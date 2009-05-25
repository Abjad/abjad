from abjad.core.abjadcore import _Abjad


class Function(_Abjad):
   '''Wrapper for names of *Scheme* functions known to *LilyPond*.'''

   def __init__(self, name = ''):
      '''Initialize function name.'''
      self.name = name

   ## PUBLIC ATTRIBUTES ##
   
   @property
   def format(self):
      '''*LilyPond* input representation of function.'''
      return self.name
