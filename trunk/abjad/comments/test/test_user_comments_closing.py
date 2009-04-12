from abjad import *


def test_comments_closing_01( ):
   '''Test container comments closing.'''

   t = Voice(scale(4))
   Beam(t[:])
   t.comments.closing.append('Voice closing comments here.')
   t.comments.closing.append('More voice closing comments.')

   r'''\new Voice {
           c'8 [
           d'8
           e'8
           f'8 ]
           % Voice closing comments here.
           % More voice closing comments.
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n\t% Voice closing comments here.\n\t% More voice closing comments.\n}"


def test_comments_closing_02( ):
   '''Test leaf comments closing.'''

   t = Note(0, (1, 8))
   t.beam.thickness = 3
   t.comments.closing.append('Leaf closing comments here.')
   t.comments.closing.append('More leaf closing comments.')

   r'''\once \override Beam #'thickness = #3
   c'8
   % Leaf closing comments here.
   % More leaf closing comments.'''

   assert check.wf(t)
   assert t.format == "\\once \\override Beam #'thickness = #3\nc'8\n% Leaf closing comments here.\n% More leaf closing comments."
