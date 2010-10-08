from abjad.components.Chord import Chord
from abjad.components.Note import Note
from abjad.tools import pitchtools


def color_chord_note_heads_by_numeric_pitch_class(chord, color_map):
   r'''.. versionadded:: 1.1.2

   Color note_heads in `chord` according to `color_map`.

   Return `chord`. ::

      abjad> pitches = [[-12, -10, 4], [-2, 8, 11, 17], [19, 27, 30, 33, 37]]   
      abjad> colors = ['red', 'blue', 'green']   
      abjad> color_map = pitchtools.NumberedChromaticPitchClassColorMap(pitches, colors)

   ::

      abjad> chord = Chord([12, 14, 18, 21, 23], (1, 4))
      abjad> chordtools.color_chord_note_heads_by_numeric_pitch_class(chord, color_map)
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
      abjad> chordtools.color_chord_note_heads_by_numeric_pitch_class(note, color_map)
      Note(c', 4)
      abjad> f(note)
      \once \override NoteHead #'color = #red
      c'4

   In the case that `chord` is neither a chord nor note,
   simply return input unaltered. ::

      abjad> staff = Staff([ ])
      abjad> chordtools.color_chord_note_heads_by_numeric_pitch_class(staff, color_map)
      Staff{ }

   .. versionchanged:: 1.1.2
      renamed ``chordtools.color_note_heads_by_pc( )`` to
      ``chordtools.color_chord_note_heads_by_numeric_pitch_class( )``.
   '''

   assert isinstance(color_map, pitchtools.NumberedChromaticPitchClassColorMap)
   
   if isinstance(chord, Chord):
      for note_head in chord:
         pc = note_head.pitch.numeric_pitch_class
         color = color_map.get(pc, None)
         if color is not None:
            note_head.tweak.color = color
   elif isinstance(chord, Note):
      note = chord
      note_head = note.note_head
      pc = note_head.pitch.numeric_pitch_class
      color = color_map.get(pc, None)
      if color is not None:
         note.override.note_head.color = color

   return chord
