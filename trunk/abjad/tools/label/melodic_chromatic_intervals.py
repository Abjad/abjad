from abjad.leaf import _Leaf
from abjad.note import Note
from abjad.tools import iterate


def melodic_chromatic_intervals(expr):
   r'''.. versionadded:: 1.1.2

   Label the melodic chromatic interval of every leaf in `expr`. ::

      abjad> staff = Staff(construct.notes([0, 13, 11, 8, 2, 3, 9, 10, 6, 5], [Rational(1, 8)]))
      abjad> label.melodic_chromatic_intervals(staff)
      abjad> f(staff)
      \new Staff {
              c'8 ^ \markup { 13 }
              cs''8 ^ \markup { -2 }
              b'8 ^ \markup { -2 }
              af'8 ^ \markup { -6 }
              d'8 ^ \markup { 1 }
              ef'8 ^ \markup { 6 }
              a'8 ^ \markup { 1 }
              bf'8 ^ \markup { -4 }
              fs'8 ^ \markup { -1 }
              f'8
      }
   '''

   for note in iterate.naive_forward_in(expr, Note):
      thread_iterator = iterate.thread_forward_from(note, _Leaf)
      try:
         thread_iterator.next( )
         next_leaf = thread_iterator.next( )
         if isinstance(next_leaf, Note):
            mdi = note.pitch - next_leaf.pitch
            mchi = mdi.melodic_chromatic_interval
            note.markup.up.append(mchi.number)
      except StopIteration:
         pass
