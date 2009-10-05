from abjad import *


def test_chordtools_color_noteheads_by_pc_01( ):
   '''Works on chords.'''

   color_map = {
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
       37: 'green'
   }

   chord = Chord([12, 14, 18, 21, 23], (1, 4))
   chordtools.color_noteheads_by_pc(chord, color_map)

   r'''
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
   '''

   assert check.wf(chord)
   assert chord.format == "<\n\t\\tweak #'color #red\n\tc''\n\t\\tweak #'color #red\n\td''\n\t\\tweak #'color #green\n\tfs''\n\t\\tweak #'color #green\n\ta''\n\t\\tweak #'color #blue\n\tb''\n>4"


def test_chordtools_color_noteheads_by_pc_02( ):
   '''Works on notes.'''

   color_map = {
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
       37: 'green'
   }

   note = Note(0, (1, 4))
   chordtools.color_noteheads_by_pc(note, color_map)

   r'''
   \once \override NoteHead #'color = #red
   c'4
   '''

   assert check.wf(note)
   assert note.format == "\\once \\override NoteHead #'color = #red\nc'4"
