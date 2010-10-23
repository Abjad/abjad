from abjad.tools.mathtools.is_power_of_two import is_power_of_two


def all_are_powers_of_two(expr):
   '''.. versionadded:: 1.1.2

   True when all elements in `expr` are powers of two:

      abjad> listtools.all_are_powers_of_two([1, 1, 2, 4, 8, 16, 32, 32, 32, 64])
      True

   Otherwise false:

      abjad> listtools.all_are_powers_of_two([1, 1, 3, 9, 27, 27])
      False
   '''

   return all([is_power_of_two(element) for element in expr])
