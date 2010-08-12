from abjad.tools.leaftools._label_leaves_in_expr_with_leaf_durations import \
   _label_leaves_in_expr_with_leaf_durations


def label_tie_chains_in_expr_with_written_tie_chain_duration(expr):
   r'''Label tie chains in `expr` with written tie chain duration.::

      abjad> staff = Staff(notetools.make_repeated_notes(4))
      abjad> FixedDurationTuplet((2, 8), staff[:3])
      abjad> Tie(staff.leaves[:2])
      abjad> Tie(staff.leaves[2:])
      abjad> tietools.label_tie_chains_in_expr_with_written_tie_chain_duration(staff)
      abjad> f(staff)
      \new Staff {
         \times 2/3 {
            c'8 _ \markup { \small 1/4 } ~
            c'8
            c'8 _ \markup { \small 1/4 } ~
         }
         c'8
      }

   Return none.
   '''

   show = ['written']
   return _label_leaves_in_expr_with_leaf_durations(expr, show = show, ties = 'together')
