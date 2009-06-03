from abjad.rational.rational import Rational
from abjad.tools import mathtools
from abjad.tools.listtools.weight import weight as listtools_weight


def repeat_to_weight(l, weight, remainder = 'chop'):
   '''Repeat ``l`` until ``listtools.weight(result)`` compares \
      correctly to ``weight`` as specified by ``remainder``.

   When ``remainder = 'chop'`` chop last number in output list
   to ensure that ``listtools.weight(result)`` equals ``weight`` exactly.

   ::

      abjad> l = [5, 5, 5]
      abjad> listtools.repeat_to_weight(l, 23)
      [5, 5, 5, 5, 3]

   When ``remainder = 'less'`` allow ``listtools.weight(result)`` \
   to be less than or equal to ``weight``.

   ::

      abjad> l = [5, 5, 5]
      abjad> repeat_to_weight(l, 23, remainder = 'less')
      [5, 5, 5, 5]

   When ``remainder = 'more'`` allow ``listtools.weight(result)`` \
   to be greater than or equal to ``weight``.

   ::

      abjad> l = [5, 5, 5]
      abjad> listtools.repeat_to_weight(l, 23, remainder = 'more')
      [5, 5, 5, 5, 5]

   Because ``listtools.weight(l)`` equals the sum of the absolute \
   value of the elements in ``l``, negative numbers in ``l`` \
   cyclically repeat in the output of ``listtools.repeat_to_weight( )``.

   ::

      abjad> l = [-5, -5, 5]
      abjad> listtools.repeat_to_weight(l, 23)
      [-5, -5, 5, -5, -3]'''

   assert isinstance(weight, (int, float, long, Rational))
   assert 0 <= weight

   result = [ ]

   result.append(l[0])
   i = 1
   while listtools_weight(result) < weight:
      result.append(l[i % len(l)])
      i += 1
   if weight < listtools_weight(result):
      if remainder == 'less':
         result = result[:-1]
      elif remainder == 'chop':
         result = result[:-1] + [mathtools.sign(result[-1]) * \
            (weight - listtools_weight(result[:-1]))]
      elif remainder == 'more':
         pass

   return result
