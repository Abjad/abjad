from abjad import *


def test_user_comments_before_01( ):
   '''Test context comments before.'''

   t = Voice(construct.scale(4))
   beam = Beam(t[:])
   beam.thickness = 3
   t.comments.before.append('Voice before comments here.')
   t.comments.before.append('More voice before comments.')

   r'''% Voice before comments here.
   % More voice before comments.
   \new Voice {
           \override Beam #'thickness = #3
           c'8 [
           d'8
           e'8
           f'8 ]
           \revert Beam #'thickness
   }'''

   assert check.wf(t)
   assert t.format == "% Voice before comments here.\n% More voice before comments.\n\\new Voice {\n\t\\override Beam #'thickness = #3\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n\t\\revert Beam #'thickness\n}"


def test_user_comments_before_02( ):
   '''Leaf comments before.'''

   t = Note(0, (1, 8))
   t.beam.thickness = 3
   t.comments.before.append('Leaf comments before here.')
   t.comments.before.append('More comments before.')
   
   r'''% Leaf comments before here.
   % More comments before.
   \once \override Beam #'thickness = #3
   c'8'''

   assert check.wf(t)
   assert t.format == "% Leaf comments before here.\n% More comments before.\n\\once \\override Beam #'thickness = #3\nc'8"

