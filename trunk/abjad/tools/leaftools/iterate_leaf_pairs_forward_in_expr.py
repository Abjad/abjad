from abjad.tools import seqtools
from abjad.tools.verticalitytools.iterate_vertical_moments_forward_in_expr import iterate_vertical_moments_forward_in_expr


def iterate_leaf_pairs_forward_in_expr(expr):
   r'''.. versionadded:: 1.1.2

   Iterate left-to-right, top-to-bottom leaf pairs in `expr`. ::

      abjad> score = Score([ ])
      abjad> notes = macros.scale(4) + [Note(7, (1, 4))]
      abjad> score.append(Staff(notes))
      abjad> notes = [Note(x, (1, 4)) for x in [-12, -15, -17]]
      abjad> score.append(Staff(notes))
      abjad> contexttools.ClefMark('bass')(score[1])

   ::

      abjad> f(score)
      \new Score <<
              \new Staff {
                      c'8
                      d'8
                      e'8
                      f'8
                      g'4
              }
              \new Staff {
                      \clef "bass"
                      c4
                      a,4
                      g,4
              }
      >>

   ::

      abjad> for pair in leaftools.iterate_leaf_pairs_forward_in_expr(score):
      ...      pair
      (Note(c', 8), Note(c, 4))
      (Note(c', 8), Note(d', 8))
      (Note(c, 4), Note(d', 8))
      (Note(d', 8), Note(e', 8))
      (Note(d', 8), Note(a,, 4))
      (Note(c, 4), Note(e', 8))
      (Note(c, 4), Note(a,, 4))
      (Note(e', 8), Note(a,, 4))
      (Note(e', 8), Note(f', 8))
      (Note(a,, 4), Note(f', 8))
      (Note(f', 8), Note(g', 4))
      (Note(f', 8), Note(g,, 4))
      (Note(a,, 4), Note(g', 4))
      (Note(a,, 4), Note(g,, 4))
      (Note(g', 4), Note(g,, 4))

   .. versionchanged:: 1.1.2
      renamed ``iterate.leaf_pairs_forward_in( )`` to
      ``leaftools.iterate_leaf_pairs_forward_in_expr( )``.

   .. versionchanged:: 1.1.2
      renamed ``iterate.leaf_pairs_forward_in_expr( )`` to
      ``leaftools.iterate_leaf_pairs_forward_in_expr( )``.
   '''

   vertical_moments = iterate_vertical_moments_forward_in_expr(expr)
   for moment_1, moment_2 in seqtools.iterate_sequence_pairwise_strict(vertical_moments):
      for pair in seqtools.yield_all_unordered_pairs_in_sequence(moment_1.start_leaves):
         yield pair
      pairs = seqtools.pairs_from_to(moment_1.leaves, moment_2.start_leaves)
      for pair in pairs: 
         yield pair
   else:
      for pair in seqtools.yield_all_unordered_pairs_in_sequence(moment_2.start_leaves):
         yield pair
