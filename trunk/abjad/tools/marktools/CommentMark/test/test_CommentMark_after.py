from abjad import *


def test_CommentMark_after_01( ):
   '''Test context comments after.'''

   t = Voice(macros.scale(4))
   beam = spannertools.BeamSpanner(t[:])
   beam.override.beam.thickness = 3
   #t.comments.after.append('Voice after comments here.')
   #t.comments.after.append('More voice after comments.')
   marktools.CommentMark('Voice after comments here.', 'after')(t)
   marktools.CommentMark('More voice after comments.', 'after')(t)

   r'''
   \new Voice {
           \override Beam #'thickness = #3
           c'8 [
           d'8
           e'8
           f'8 ]
           \revert Beam #'thickness
   }
   % Voice after comments here.
   % More voice after comments.'''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Voice {\n\t\\override Beam #'thickness = #3\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n\t\\revert Beam #'thickness\n}\n% Voice after comments here.\n% More voice after comments."


def test_CommentMark_after_02( ):
   '''Leaf comments after.'''

   t = Note(0, (1, 8))
   t.override.beam.thickness = 3
   #t.comments.after.append('Leaf comments after here.')
   #t.comments.after.append('More comments after.')
   marktools.CommentMark('Leaf comments after here.', 'after')(t)
   marktools.CommentMark('More comments after.', 'after')(t)

   r'''
   \once \override Beam #'thickness = #3
   c'8
   % Leaf comments after here.
   % More comments after.'''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\once \\override Beam #'thickness = #3\nc'8\n% Leaf comments after here.\n% More comments after." 
