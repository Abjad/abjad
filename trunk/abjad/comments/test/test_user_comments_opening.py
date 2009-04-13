from abjad import *


def test_comments_opening_01( ):
   '''Opening comments in container.'''

   t = Voice(construct.scale(4))
   Beam(t[:])
   t.comments.opening.append('Voice opening comments here.')
   t.comments.opening.append('More voice opening comments.')

   r'''\new Voice {
           % Voice opening comments here.
           % More voice opening comments.
           c'8 [
           d'8
           e'8
           f'8 ]
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\t% Voice opening comments here.\n\t% More voice opening comments.\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"


def test_comments_opening_02( ):
   '''Opening comments on leaf.'''

   t = Note(0, (1, 8))
   t.beam.thickness = 3
   t.comments.opening.append('Leaf opening comments here.')
   t.comments.opening.append('More leaf opening comments.')

   r'''\once \override Beam #'thickness = #3
   % Leaf opening comments here.
   % More leaf opening comments.
   c'8'''

   assert check.wf(t)
   assert t.format == "\\once \\override Beam #'thickness = #3\n% Leaf opening comments here.\n% More leaf opening comments.\nc'8"
