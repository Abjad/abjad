from abjad.leaf import _Leaf
from abjad.note import Note
from abjad.tools import iterate


def label_leaves_in_expr_with_melodic_counterpoint_interval_classes(expr):
   r""".. versionadded:: 1.1.2

   Label the melodic counterpoint interval class between 
   every leaf in `expr`. ::

      abjad> staff = Staff(leaftools.make_notes([0, 25, 11, -4, -14, -13, 9, 10, 6, 5], [Rational(1, 8)]))
      abjad> leaftools.label_leaves_in_expr_with_melodic_counterpoint_interval_classes(staff)
      abjad> f(staff)
      \new Staff {
              c'8 ^ \markup { +8 }
              cs'''8 ^ \markup { -2 }
              b'8 ^ \markup { -2 }
              af8 ^ \markup { -7 }
              bf,8 ^ \markup { +1 }
              b,8 ^ \markup { +7 }
              a'8 ^ \markup { +2 }
              bf'8 ^ \markup { -4 }
              fs'8 ^ \markup { +1 }
              f'8
      }
   """
   from abjad.tools import pitchtools
   
   for note in iterate.naive_forward_in_expr(expr, Note):
      thread_iterator = iterate.thread_forward_from_component(note, _Leaf)
      try:
         thread_iterator.next( )
         next_leaf = thread_iterator.next( )
         if isinstance(next_leaf, Note):
            cpi = pitchtools.melodic_counterpoint_interval_from_to(
               note, next_leaf)
            note.markup.up.append(cpi.interval_class)
      except StopIteration:
         pass
