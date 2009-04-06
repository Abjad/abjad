from abjad import *


def test_comments_contributions_01( ):
   '''context comments contributions.'''

   t = Voice(scale(4))
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

   result = t.comments.contributions

   (('before', ('Comments before.',)),
    ('opening', ('Comments opening.',)),
    ('right', ('Unacknowledged comments right.',)),
    ('closing', ('Comments closing.',)),
    ('after', ('Comments after.',)))

   assert check(t)
   assert result == (('before', ('Comments before.',)), ('opening', ('Comments opening.',)), ('right', ('Unacknowledged comments right.',)), ('closing', ('Comments closing.',)), ('after', ('Comments after.',)))


def test_comments_contributions_02( ):
   '''Leaf comments contributions.'''

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

   result = t.comments.contributions

   (('before', ('Comments before.',)),
    ('opening', ('Comments opening.',)),
    ('right', ('Comments right.',)),
    ('closing', ('Comments closing.',)),
    ('after', ('Comments after.',)))

   assert check(t)
   assert result == (('before', ('Comments before.',)), ('opening', ('Comments opening.',)), ('right', ('Comments right.',)), ('closing', ('Comments closing.',)), ('after', ('Comments after.',)))
