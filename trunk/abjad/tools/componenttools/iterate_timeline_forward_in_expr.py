from abjad.components._Leaf import _Leaf
from abjad.tools.componenttools.iterate_components_forward_in_expr import iterate_components_forward_in_expr


def iterate_timeline_forward_in_expr(expr, klass = _Leaf):
   r'''.. versionadded:: 1.1.2

   Yield `klass` instances in `expr` 
   sorted forward by prolated offset start time. ::

      abjad> score = Score([ ])
      abjad> score.append(Staff(leaftools.make_repeated_notes(4, Rational(1, 4))))
      abjad> score.append(Staff(leaftools.make_repeated_notes(4)))
      abjad> pitchtools.set_ascending_diatonic_pitches_on_nontied_pitched_components_in_expr(score)
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
      abjad> for leaf in componenttools.iterate_timeline_forward_in_expr(score):
      ...     leaf
      ... 
      Note(c', 4)
      Note(g', 8)
      Note(a', 8)
      Note(d', 4)
      Note(b', 8)
      Note(c'', 8)
      Note(e', 4)
      Note(f', 4)

   .. todo:: optimize to avoid behind-the-scenes full-score traversal.

   .. versionchanged:: 1.1.2
      renamed ``iterate.timeline_forward_in( )`` to
      ``componenttools.iterate_timeline_forward_in_expr( )``.

   .. versionchanged:: 1.1.2
      renamed ``iterate.timeline_forward_in_expr( )`` to
      ``componenttools.iterate_timeline_forward_in_expr( )``.
   '''

   component_generator = iterate_components_forward_in_expr(expr, klass = klass)
   components = list(component_generator)
   
   def _sort_helper(component_1, component_2):
      result = cmp(component_1.offset.prolated.start, 
         component_2.offset.prolated.start)
      if result == 0:
         return cmp(component_1.score.index, component_2.score.index)
      else:
         return result

   components.sort(_sort_helper)

   for component in components:
      yield component
