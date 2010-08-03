from abjad.components._Leaf import _Leaf
from abjad.tools.iterate.timeline_forward_in_expr import timeline_forward_in_expr


def timeline_forward_from_component(expr, klass = _Leaf):
   r'''.. versionadded:: 1.1.2

   Yield `klass` instances in root of `expr`
   sorted forward by prolated offset start time,
   starting from `expr`. ::

      abjad> score = Score([ ])
      abjad> score.append(Staff(leaftools.make_repeated_notes(4, Rational(1, 4))))
      abjad> score.append(Staff(leaftools.make_repeated_notes(4)))
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
      abjad> for leaf in iterate.timeline_forward_from_component(score[1][2]):
      ...     leaf
      ... 
      Note(b', 8)
      Note(c'', 8)
      Note(e', 4)
      Note(f', 4)

   .. todo:: optimize to avoid behind-the-scenes full-score traversal.

   .. versionchanged:: 1.1.2
      renamed ``iterate.timeline_forward_from( )`` to
      ``iterate.timeline_forward_from_component( )``.
   '''

   root = expr.parentage.root
   component_generator = timeline_forward_in_expr(root, klass = klass)

   yielded_expr = False
   for component in component_generator:
      if yielded_expr:
         yield component
      elif component is expr:
         yield component
         yielded_expr = True
