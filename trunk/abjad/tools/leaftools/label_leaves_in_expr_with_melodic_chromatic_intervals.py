from abjad.components._Leaf import _Leaf
from abjad.components.Note import Note
from abjad.tools import componenttools
from abjad.tools import markuptools
from abjad.tools import threadtools


def label_leaves_in_expr_with_melodic_chromatic_intervals(expr, markup_direction = 'up'):
   r""".. versionadded:: 1.1.2

   Label the melodic chromatic interval of every leaf in `expr`. ::

      abjad> staff = Staff(notetools.make_notes([0, 25, 11, -4, -14, -13, 9, 10, 6, 5], [Fraction(1, 8)]))
      abjad> leaftools.label_leaves_in_expr_with_melodic_chromatic_intervals(staff)
      abjad> f(staff)
      \new Staff {
              c'8 ^ \markup { +25 }
              cs'''8 ^ \markup { -14 }
              b'8 ^ \markup { -15 }
              af8 ^ \markup { -10 }
              bf,8 ^ \markup { +1 }
              b,8 ^ \markup { +22 }
              a'8 ^ \markup { +1 }
              bf'8 ^ \markup { -4 }
              fs'8 ^ \markup { -1 }
              f'8
      }
   """ 
   from abjad.tools import pitchtools

   for note in componenttools.iterate_components_forward_in_expr(expr, Note):
      thread_iterator = threadtools.iterate_thread_forward_from_component(note, _Leaf)
      try:
         thread_iterator.next( )
         next_leaf = thread_iterator.next( )
         if isinstance(next_leaf, Note):
            mci = pitchtools.calculate_melodic_chromatic_interval_from_pitch_to_pitch(
               note, next_leaf)
            markuptools.Markup(mci, markup_direction)(note)
      except StopIteration:
         pass
