from abjad import *


def test_CommentMark_right_01( ):
   '''Context comments right.'''

   t = Voice(macros.scale(4))
   beam = spannertools.BeamSpanner(t[:])
   beam.override.beam.thickness = 3
   marktools.CommentMark('Voice right comments here.', 'right')(t)
   marktools.CommentMark('More voice right comments.', 'right')(t)

   "Container slots interfaces do not collect contributions to right."

   r'''
   \new Voice {
           \override Beam #'thickness = #3
           c'8 [
           d'8
           e'8
           f'8 ]
           \revert Beam #'thickness
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Voice {\n\t\\override Beam #'thickness = #3\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n\t\\revert Beam #'thickness\n}"


def test_CommentMark_right_02( ):
   '''Leaf comments right.'''

   t = Note(0, (1, 8))
   t.override.beam.thickness = 3
   marktools.CommentMark('Leaf comments right here.', 'right')(t)
   marktools.CommentMark('More comments right.', 'right')(t)

   r'''
   \once \override Beam #'thickness = #3
   c'8 % Leaf comments right here. % More comments right.
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\once \\override Beam #'thickness = #3\nc'8 % Leaf comments right here. % More comments right."
