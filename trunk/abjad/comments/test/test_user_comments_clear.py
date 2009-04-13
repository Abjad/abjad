from abjad import *


def test_comments_clear_01( ):
   '''Clear context comments.'''

   t = Voice(construct.scale(4))
   beam = Beam(t[:])
   beam.thickness = 3
   t.comments.before.append('Comments before.')
   t.comments.opening.append('Comments opening.')
   t.comments.right.append('Unacknowledged comments right.')
   t.comments.closing.append('Comments closing.')
   t.comments.after.append('Comments after.')

   r'''% Comments before.
   \new Voice {
           % Comments opening.
           \override Beam #'thickness = #3
           c'8 [
           d'8
           e'8
           f'8 ]
           \revert Beam #'thickness
           % Comments closing.
   }
   % Comments after.'''

   t.comments.clear( )

   r'''\new Voice {
           \override Beam #'thickness = #3
           c'8 [
           d'8
           e'8
           f'8 ]
           \revert Beam #'thickness
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\t\\override Beam #'thickness = #3\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n\t\\revert Beam #'thickness\n}"


def test_comments_clear_02( ):
   '''Clear leaf comments.'''

   t = Note(0, (1, 8))
   t.beam.thickness = 3
   t.comments.before.append('Comments before.')
   t.comments.opening.append('Comments opening.')
   t.comments.right.append('Comments right.')
   t.comments.closing.append('Comments closing.')
   t.comments.after.append('Comments after.')

   r'''% Comments before.
   \once \override Beam #'thickness = #3
   % Comments opening.
   c'8 % Comments right.
   % Comments closing.
   % Comments after.'''

   t.comments.clear( )

   r'''\once \override Beam #'thickness = #3
   c'8'''

   assert check.wf(t)
   assert t.format == "\\once \\override Beam #'thickness = #3\nc'8"
