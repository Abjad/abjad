from abjad.exceptions import InputError
from abjad.tools.mathtools.is_integer_equivalent_number import is_integer_equivalent_number


def integer_equivalent_number_to_integer(number):
   '''.. versionadded:: 1.1.2
   
   Change integer-equivalent `number` to integer.

   Docs.
   '''

   if not is_integer_equivalent_number(number):
      raise InputError('"%s" must be integer-equivalent number.' % str(number))

   return int(number)
