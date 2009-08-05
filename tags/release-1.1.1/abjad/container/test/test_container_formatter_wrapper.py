from abjad import *


def test_container_formatter_wrapper_01( ):
   '''Context formatter wrapper.'''

   t = Voice(construct.scale(4))
   t.comments.before.append('Example voice')
   t.notehead.color = 'red'
   t.accidental.style = 'forget'
   beam = Beam(t[:])
   beam.thickness = 3

   r'''
   % Example voice
   \new Voice \with {
           \override NoteHead #'color = #red
   } {
           #(set-accidental-style 'forget)
           \override Beam #'thickness = #3
           c'8 [
           d'8
           e'8
           f'8 ]
           \revert Beam #'thickness
   }
   '''

   #result = t.formatter.wrapper
   result = formattools.wrapper(t)

   r'''
   % Example voice
   \new Voice \with {
           \override NoteHead #'color = #red
   } {
           #(set-accidental-style 'forget)

           %%% 4 components omitted %%%

   }
   '''

   assert result == "% Example voice\n\\new Voice \\with {\n\t\\override NoteHead #'color = #red\n} {\n\t#(set-accidental-style 'forget)\n\n\t%%% 4 components omitted %%%\n\n}"


def test_container_formatter_wrapper_02( ):
   '''Tuplet formatter wrapper.'''

   t = FixedDurationTuplet((2, 8), construct.scale(3))
   t.comments.before.append('Example tuplet')
   t.notehead.color = 'red'
   t.accidental.style = 'forget'
   beam = Beam(t[:])
   beam.thickness = 3

   r'''
   % Example tuplet
   \override NoteHead #'color = #red
   \times 2/3 {
           #(set-accidental-style 'forget)
           \override Beam #'thickness = #3
           c'8 [
           d'8
           e'8 ]
           \revert Beam #'thickness
   }
   \revert NoteHead #'color
   '''

   #result = t.formatter.wrapper
   result = formattools.wrapper(t)

   r'''
   % Example tuplet
   \override NoteHead #'color = #red
   \times 2/3 {
           #(set-accidental-style 'forget)

           %%% 3 components omitted %%%

   }
   \revert NoteHead #'color
   '''

   assert result == "% Example tuplet\n\\override NoteHead #'color = #red\n\\times 2/3 {\n\t#(set-accidental-style 'forget)\n\n\t%%% 3 components omitted %%%\n\n}\n\\revert NoteHead #'color"
