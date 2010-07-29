from abjad.tools import iterate


def remove_markup_from_leaves_in_expr(expr):
   r'''Remove markup from all leaves in `expr`.

   ::

      abjad> staff = Staff(macros.scale(4))
      abjad> leaftools.label_leaves_in_expr_with_pitch_class_numbers(staff)
      \new Staff {
              c'8 _ \markup { \small 0 }
              d'8 _ \markup { \small 2 }
              e'8 _ \markup { \small 4 }
              f'8 _ \markup { \small 5 }
      }

   ::

      abjad> leaftools.remove_markup_from_leaves_in_expr(staff)
      abjad> f(staff)
      \new Staff {
              c'8
              d'8
              e'8
              f'8
      }

   .. versionchanged:: 1.1.2
      renamed ``label.clear_leaves( )`` to
      ``leaftools.remove_markup_from_leaves_in_expr( )``.
   '''

   for leaf in iterate.leaves_forward_in_expr(expr):
      leaf.markup.up = [ ]
      leaf.markup.down = [ ]   
