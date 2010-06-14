from abjad.leaf import _Leaf
from abjad.note import Note
from abjad.tools import iterate


def melodic_diatonic_interval_classes(expr):
   r""".. versionadded:: 1.1.2

   Label the melodic diatonic interval class of every leaf in `expr`. ::

      abjad> staff = Staff(leaftools.make_notes([0, 25, 11, -4, -14, -13, 9, 10, 6, 5], [Rational(1, 8)]))
      abjad> label.melodic_diatonic_interval_classes(staff)
      abjad> f(staff)
      \new Staff {
              c'8 ^ \markup { +aug8 }
              cs'''8 ^ \markup { -M2 }
              b'8 ^ \markup { -aug2 }
              af8 ^ \markup { -m7 }
              bf,8 ^ \markup { aug1 }
              b,8 ^ \markup { +m7 }
              a'8 ^ \markup { +m2 }
              bf'8 ^ \markup { -dim4 }
              fs'8 ^ \markup { aug1 }
              f'8
      }
   """ 
   from abjad.tools import pitchtools

   for note in iterate.naive_forward_in(expr, Note):
      thread_iterator = iterate.thread_forward_from(note, _Leaf)
      try:
         thread_iterator.next( )
         next_leaf = thread_iterator.next( )
         if isinstance(next_leaf, Note):
            mdi = pitchtools.melodic_diatonic_interval_from_to(note, next_leaf)
            mdic = mdi.interval_class
            note.markup.up.append(mdic)
      except StopIteration:
         pass
