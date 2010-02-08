from abjad.leaf import _Leaf
from abjad.markup import Markup
from abjad.note import Note
from abjad.tools import iterate
from abjad.tools import pitchtools
from abjad.tools.tonalharmony.is_unlikely_melodic_diatonic_interval_in_chorale \
   import is_unlikely_melodic_diatonic_interval_in_chorale


def mark_unlikely_melodic_intervals_in_chorale(expr, direction = 'below'):
   '''.. versionadded:: 1.1.2

   Mark unlikely melodic intervals in chorale. ::

      abjad> note_entry_string = "b'4 d''2 c'4 b'4 a'2 g'2"
      abjad> soprano = lilytools.parse_note_entry_string(note_entry_string)
      abjad> tonalharmony.mark_unlikely_melodic_intervals_in_chorale(soprano, 'above')
      abjad> f(soprano)
      {
              b'4
              d''2
              \once \override NoteHead #'color = #red
              c'4 ^ \markup { \with-color #red { -M9 } }
              \once \override NoteHead #'color = #red
              b'4 ^ \markup { \with-color #red { +M7 } }
              a'2
              g'2
      }
   '''

   result = True
   for note in iterate.naive_forward_in(expr, Note):
      is_cadence = getattr(note.history, 'cadence', None)
      if is_cadence:
         continue
      thread_iterator = iterate.thread_forward_from(note, _Leaf)
      try:
         thread_iterator.next( )
         next_leaf = thread_iterator.next( )
         if isinstance(next_leaf, Note): 
            mdi = pitchtools.melodic_diatonic_interval_from_to(
               note, next_leaf)
            if is_unlikely_melodic_diatonic_interval_in_chorale(mdi):
               next_leaf.note_head.color = 'red'
               markup = Markup(r'\with-color #red { %s }' % mdi)
               if direction == 'above':
                  next_leaf.markup.up.append(markup)
               elif direction == 'below':
                  next_leaf.markup.down.append(markup)
               else:
                  raise ValueError("must be 'above' or 'below'.")
               result = False
      except StopIteration:
         pass
   return result
