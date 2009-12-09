from abjad.tools import mathtools
from abjad.tools.pitchtools._CounterpointIntervalClass import \
   _CounterpointIntervalClass
from abjad.tools.pitchtools._MelodicIntervalClass import \
   _MelodicIntervalClass


class MelodicCounterpointIntervalClass(_CounterpointIntervalClass,
   _MelodicIntervalClass):
   '''.. versionadded:: 1.1.2

   Melodic counterpoint interval class.
   '''

   def __init__(self, token):
      from abjad.tools.pitchtools._CounterpointInterval import \
         _CounterpointInterval
      if isinstance(token, int):
         number = token
      elif isinstance(token, _CounterpointInterval):
         number = token.number
      if number == 0:
         raise ValueError('must be nonzero.')
      if abs(number) == 1:
         self._number = 1
      else:
         sign = mathtools.sign(number)
         number = abs(number) % 7
         if number == 0:
            number = 7
         elif number == 1:
            number = 8
         number *= sign
         self._number = number

   ## OVERLOADS ##

   def __eq__(self, arg):
      if isinstance(arg, MelodicCounterpointIntervalClass):
         if self.number == arg.number:
            return True
      return False
         
   def __ne__(self, arg):
      return not self == arg
