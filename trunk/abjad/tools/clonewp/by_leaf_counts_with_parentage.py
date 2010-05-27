from abjad.container import Container
from abjad.tools import listtools
from abjad.tools.clonewp.by_leaf_range_with_parentage import \
   by_leaf_range_with_parentage


## TODO: Implement in-place containertools.partition_by_lengths( ) that doesn't climb to governor ##

def by_leaf_counts_with_parentage(container, leaf_counts):
   r'''Clone `container` and partition clone according to `leaf_counts`. ::

      abjad> voice = Voice(FixedDurationTuplet((2, 8), construct.run(3)) * 2)
      abjad> Beam(voice[0].leaves)
      abjad> Beam(voice[1].leaves)
      abjad> pitchtools.diatonicize(voice)
      abjad> f(voice)
      \new Voice {
        \times 2/3 {
                c'8 [
                d'8
                e'8 ]
        }
        \times 2/3 {
                f'8 [
                g'8
                a'8 ]
        }
      }
      
   ::
      
      abjad> first, second, third = clonewp.by_leaf_counts_with_parentage(voice, [1, 2, 3])
      
   ::
      
      abjad> f(first)
      \new Voice {
        \times 2/3 {
                c'8 [ ]
        }
      }
      
   ::
      
      abjad> f(second)
      \new Voice {
        \times 2/3 {
                d'8 [
                e'8 ]
        }
      }
      
   ::
      
      abjad> f(third)
      \new Voice {
        \times 2/3 {
                f'8 [
                g'8
                a'8 ]
        }
      }

   Set `leaf_counts` to an iterable of zero or more positive integers.

   Return a list of parts equal in length to that of `leaf_counts`.
   '''
   
   assert isinstance(container, Container)
   assert all([isinstance(x, int) for x in leaf_counts])

   result = [ ]
   sums = listtools.cumulative_sums_zero(leaf_counts)
   for start, stop in listtools.pairwise(sums):
      result.append(
         by_leaf_range_with_parentage(container, start, stop))

   return result
