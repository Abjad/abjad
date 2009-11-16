from abjad.leaf import _Leaf
from abjad.tools.iterate.naive_forward_in import naive_forward_in \
   as iterate_naive_forward_in


def timeline_backward_in(expr, klass = _Leaf):
   r'''.. versionadded:: 1.1.2

   Yield `klass` instances in `expr` sorted backward by score
   offset stop time. ::

      abjad> score = Score([ ])
      abjad> score.append(Staff(construct.run(4, Rational(1, 4))))
      abjad> score.append(Staff(construct.run(4)))
      abjad> pitchtools.diatonicize(score)
      abjad> f(score)
      \new Score <<
              \new Staff {
                      c'4
                      d'4
                      e'4
                      f'4
              }
              \new Staff {
                      g'8
                      a'8
                      b'8
                      c''8
              }
      >>
      abjad> for leaf in iterate.timeline_backward_in(score):
      ...     leaf
      ... 
      Note(f', 4)
      Note(e', 4)
      Note(d', 4)
      Note(c'', 8)
      Note(b', 8)
      Note(c', 4)
      Note(a', 8)
      Note(g', 8)

   .. todo:: optimize to avoid behind-the-scenes full-score traversal.
   '''

   component_generator = iterate_naive_forward_in(expr, klass = klass)
   components = list(component_generator)
   
   def sort_helper(component_1, component_2):
      result = cmp(component_1.offset.prolated.stop, 
         component_2.offset.prolated.stop)
      if result == 0:
         return cmp(component_1.score.index, component_2.score.index)
      else:
         ## note negative result of cmp( ) is returned 
         ## for backward time sort
         return -result

   components.sort(sort_helper)

   for component in components:
      yield component
