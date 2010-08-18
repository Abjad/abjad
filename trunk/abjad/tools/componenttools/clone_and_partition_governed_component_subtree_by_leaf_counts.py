from abjad.components.Container import Container
from abjad.tools import listtools


## TODO: Implement in-place containertools.partition_by_lengths( ) that doesn't climb to governor ##

def clone_and_partition_governed_component_subtree_by_leaf_counts(container, leaf_counts):
   r'''Clone `container` and partition clone according to `leaf_counts`. ::

      abjad> voice = Voice(tuplettools.FixedDurationTuplet((2, 8), notetools.make_repeated_notes(3)) * 2)
      abjad> spannertools.BeamSpanner(voice[0].leaves)
      abjad> spannertools.BeamSpanner(voice[1].leaves)
      abjad> macros.diatonicize(voice)
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
      
      abjad> first, second, third = componenttools.clone_and_partition_governed_component_subtree_by_leaf_counts(voice, [1, 2, 3])
      
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

   .. versionchanged:: 1.1.2
      renamed ``clonewp.by_leaf_counts_with_parentage( )`` to
      ``componenttools.clone_and_partition_governed_component_subtree_by_leaf_counts( )``.
   '''
   from abjad.tools.componenttools.clone_governed_component_subtree_by_leaf_range import \
      clone_governed_component_subtree_by_leaf_range
   
   assert isinstance(container, Container)
   assert all([isinstance(x, int) for x in leaf_counts])

   result = [ ]
   sums = listtools.cumulative_sums_zero(leaf_counts)
   for start, stop in listtools.pairwise(sums):
      result.append(
         clone_governed_component_subtree_by_leaf_range(container, start, stop))

   return result
