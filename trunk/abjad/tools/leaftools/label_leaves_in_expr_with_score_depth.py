from abjad.tools import iterate


def label_leaves_in_expr_with_score_depth(expr):
   r'''Label the depth of every leaf in `expr`.

   ::

      abjad> staff = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(5))
      abjad> FixedDurationTuplet((2, 8), staff[-3:])
      abjad> leaftools.label_leaves_in_expr_with_score_depth(staff)
      \new Staff {
              c'8 _ \markup { \small 1 }
              d'8 _ \markup { \small 1 }
              \times 2/3 {
                      e'8 _ \markup { \small 2 }
                      f'8 _ \markup { \small 2 }
                      g'8 _ \markup { \small 2 }
              }
      }

   .. versionchanged:: 1.1.2
      renamed ``label.leaf_depth( )`` to
      ``leaftools.label_leaves_in_expr_with_score_depth( )``.
   '''

   for leaf in iterate.leaves_forward_in_expr(expr):
      label = r'\small %s' % leaf.parentage.depth
      leaf.markup.down.append(label)
