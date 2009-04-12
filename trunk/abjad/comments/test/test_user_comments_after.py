from abjad import *


def test_comments_after_01( ):
   '''Test context comments after.'''

   t = Voice(scale(4))
   beam = Beam(t[:])
   beam.thickness = 3
   t.comments.after.append('Voice after comments here.')
   t.comments.after.append('More voice after comments.')

   r'''\new Voice {
           \override Beam #'thickness = #3
           c'8 [
           d'8
           e'8
           f'8 ]
           \revert Beam #'thickness
   }
   % Voice after comments here.
   % More voice after comments.'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\t\\override Beam #'thickness = #3\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n\t\\revert Beam #'thickness\n}\n% Voice after comments here.\n% More voice after comments."


def test_comments_after_02( ):
   '''Leaf comments after.'''

   t = Note(0, (1, 8))
   t.beam.thickness = 3
   t.comments.after.append('Leaf comments after here.')
   t.comments.after.append('More comments after.')
   
   r'''\once \override Beam #'thickness = #3
   c'8
   % Leaf comments after here.
   % More comments after.'''

   assert check.wf(t)
   assert t.format == "\\once \\override Beam #'thickness = #3\nc'8\n% Leaf comments after here.\n% More comments after." 
