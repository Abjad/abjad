from fractions import Fraction
from abjad.tools import mathtools
from abjad.tools.mathtools.weight import weight


def repeat_sequence_to_weight(l, total_weight, remainder = 'chop'):
   '''Repeat `l` until ``mathtools.weight(result)`` compares
   correctly to `total_weight` as specified by `remainder`.

   When ``remainder = 'chop'`` chop last number in output list
   to ensure that ``mathtools.weight(result)`` equals `weight` exactly. ::

      abjad> l = [5, 5, 5]
      abjad> seqtools.repeat_sequence_to_weight(l, 23)
      [5, 5, 5, 5, 3]

   When ``remainder = 'less'`` allow ``mathtools.weight(result)``
   to be less than or equal to `weight`. ::

      abjad> l = [5, 5, 5]
      abjad> repeat_sequence_to_weight(l, 23, remainder = 'less')
      [5, 5, 5, 5]

   When ``remainder = 'more'`` allow ``mathtools.weight(result)``
   to be greater than or equal to `total_weight`. ::

      abjad> l = [5, 5, 5]
      abjad> seqtools.repeat_sequence_to_weight(l, 23, remainder = 'more')
      [5, 5, 5, 5, 5]

   Because ``mathtools.weight(l)`` equals the sum of the absolute 
   value of the elements in `l`, negative numbers in `l` 
   cyclically repeat in the output of this function. ::

      abjad> l = [-5, -5, 5]
      abjad> seqtools.repeat_sequence_to_weight(l, 23)
      [-5, -5, 5, -5, -3]

   .. versionchanged:: 1.1.2
      renamed ``seqtools.repeat_list_to_weight( )`` to
      ``seqtools.repeat_sequence_to_weight( )``.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.repeat_iterable_to_weight( )`` to
      ``seqtools.repeat_sequence_to_weight( )``.
   '''

   assert isinstance(total_weight, (int, float, long, Fraction))
   assert 0 <= total_weight

   result = [ ]

   result.append(l[0])
   i = 1
   while weight(result) < total_weight:
      result.append(l[i % len(l)])
      i += 1
   if total_weight < weight(result):
      if remainder == 'less':
         result = result[:-1]
      elif remainder == 'chop':
         result = result[:-1] + [mathtools.sign(result[-1]) * \
            (total_weight - weight(result[:-1]))]
      elif remainder == 'more':
         pass

   #return result
   return type(l)(result)
