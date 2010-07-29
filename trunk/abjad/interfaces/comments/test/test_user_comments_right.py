from abjad import *


def test_user_comments_right_01( ):
   '''Context comments right.'''

   t = Voice(macros.scale(4))
   beam = Beam(t[:])
   beam.thickness = 3
   t.comments.right.append('Voice right comments here.')
   t.comments.right.append('More voice right comments.')

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


def test_user_comments_right_02( ):
   '''Leaf comments right.'''

   t = Note(0, (1, 8))
   t.beam.thickness = 3
   t.comments.right.append('Leaf comments right here.')
   t.comments.right.append('More comments right.')
   
   r'''
   \once \override Beam #'thickness = #3
   c'8 % Leaf comments right here. % More comments right.'''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\once \\override Beam #'thickness = #3\nc'8 % Leaf comments right here. % More comments right."
