from abjad.leaf import _Leaf
from abjad.note import Note
from abjad.tools import iterate


def melodic_chromatic_interval_classes(expr):
   r""".. versionadded:: 1.1.2

   Label the melodic chromatic interval class of every leaf in `expr`. ::

      abjad> staff = Staff(leaftools.make_notes([0, 25, 11, -4, -14, -13, 9, 10, 6, 5], [Rational(1, 8)]))
      abjad> label.melodic_chromatic_interval_classes(staff)
      abjad> f(staff)
      \new Staff {
              c'8 ^ \markup { +1 }
              cs'''8 ^ \markup { -2 }
              b'8 ^ \markup { -2 }
              af8 ^ \markup { -10 }
              bf,8 ^ \markup { +1 }
              b,8 ^ \markup { +10 }
              a'8 ^ \markup { +1 }
              bf'8 ^ \markup { -4 }
              fs'8 ^ \markup { -1 }
              f'8
      }
   """

   for note in iterate.naive_forward_in(expr, Note):
      thread_iterator = iterate.thread_forward_from(note, _Leaf)
      try:
         thread_iterator.next( )
         next_leaf = thread_iterator.next( )
         if isinstance(next_leaf, Note):
            mdi = note.pitch - next_leaf.pitch
            mci = mdi.melodic_chromatic_interval
            mcic = mci.interval_class
            note.markup.up.append(mcic)
      except StopIteration:
         pass
