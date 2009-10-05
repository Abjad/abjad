from abjad.chord import Chord
from abjad.note import Note


def color_noteheads_by_pc(chord, color_map):
   r'''.. versionadded:: 1.1.2

   Color noteheads in `chord` according to `color_map`.

   Return `chord`. ::

      abjad> color_map = {
         -12: 'red',
         -10: 'red',
           4: 'red',
          -2: 'blue',
           8: 'blue',
          11: 'blue',
          17: 'blue',
          19: 'green',
          27: 'green',
          30: 'green',
          33: 'green',
          37: 'green' }
   
   ::

      abjad> chord = Chord([12, 14, 18, 21, 23], (1, 4))
      abjad> chordtools.color_noteheads_by_pc(chord, color_map)
      Chord(c'' d'' fs'' a'' b'', 4)
      abjad> f(chord)
      <
              \tweak #'color #red
              c''
              \tweak #'color #red
              d''
              \tweak #'color #green
              fs''
              \tweak #'color #green
              a''
              \tweak #'color #blue
              b''
      >4

   Also works on notes. ::

      abjad> note = Note(0, (1, 4))
      abjad> chordtools.color_noteheads_by_pc(note, color_map)
      Note(c', 4)
      abjad> f(note)
      \once \override NoteHead #'color = #red
      c'4

   In the case that `chord` is neither a chord nor note,
   simply return input unaltered. ::

      abjad> staff = Staff([ ])
      abjad> chordtools.color_noteheads_by_pc(staff, color_map)
      Staff{ }
   '''

   normalized_color_map = dict([(x % 12, y) for (x, y) in color_map.items( )])
   
   if isinstance(chord, Chord):
      for notehead in chord:
         pc = notehead.pitch.pc
         color = normalized_color_map.get(pc, None)
         if color is not None:
            notehead.color = color
   elif isinstance(chord, Note):
      notehead = chord.notehead
      pc = notehead.pitch.pc
      color = normalized_color_map.get(pc, None)
      if color is not None:
         notehead.color = color 

   return chord
