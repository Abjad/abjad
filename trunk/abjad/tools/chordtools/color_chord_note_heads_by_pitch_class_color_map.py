from abjad.tools.chordtools.Chord import Chord
from abjad.tools import pitchtools


def color_chord_note_heads_by_pitch_class_color_map(chord, color_map):
   r'''.. versionadded:: 1.1.2

   Color `chord` note heads by pitch-class `color_map`::

      abjad> chord = Chord([12, 14, 18, 21, 23], (1, 4))

   ::

      abjad> pitches = [[-12, -10, 4], [-2, 8, 11, 17], [19, 27, 30, 33, 37]]   
      abjad> colors = ['red', 'blue', 'green']   
      abjad> color_map = pitchtools.NumberedChromaticPitchClassColorMap(pitches, colors)

   ::

      abjad> chordtools.color_chord_note_heads_by_pitch_class_color_map(chord, color_map)
      Chord("<c'' d'' fs'' a'' b''>4")

   ::

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

   Also works on notes::

      abjad> note = Note("c'4")

   ::

      abjad> chordtools.color_chord_note_heads_by_pitch_class_color_map(note, color_map)
      Note("c'4")

   ::

      abjad> f(note)
      \once \override NoteHead #'color = #red
      c'4

   When `chord` is neither a chord nor note return `chord` unchanged::

      abjad> staff = Staff([ ])

   ::

      abjad> chordtools.color_chord_note_heads_by_pitch_class_color_map(staff, color_map)
      Staff{ }

   Return `chord`.

   .. versionchanged:: 1.1.2
      renamed ``chordtools.color_note_heads_by_pc( )`` to
      ``chordtools.color_chord_note_heads_by_pitch_class_color_map( )``.
   '''
   from abjad.tools import notetools

   assert isinstance(color_map, pitchtools.NumberedChromaticPitchClassColorMap)
   
   if isinstance(chord, Chord):
      for note_head in chord:
         pc = note_head.pitch.numbered_chromatic_pitch_class
         color = color_map.get(pc, None)
         if color is not None:
            note_head.tweak.color = color
   elif isinstance(chord, notetools.Note):
      note = chord
      note_head = note.note_head
      pc = note_head.pitch.numbered_chromatic_pitch_class
      color = color_map.get(pc, None)
      if color is not None:
         note.override.note_head.color = color

   return chord
