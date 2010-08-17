from abjad import *


def test_CommentsInterface_contributions_01( ):
   '''Context comments contributions.'''

   t = Voice(macros.scale(4))
   beam = BeamSpanner(t[:])
   beam.thickness = 3
   t.comments.before.append('Comments before.')
   t.comments.opening.append('Comments opening.')
   t.comments.right.append('Unacknowledged comments right.')
   t.comments.closing.append('Comments closing.')
   t.comments.after.append('Comments after.')

   r'''
   % Comments before.
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

   assert componenttools.is_well_formed_component(t)
   assert result == (('before', ('Comments before.',)), ('opening', ('Comments opening.',)), ('right', ('Unacknowledged comments right.',)), ('closing', ('Comments closing.',)), ('after', ('Comments after.',)))


def test_CommentsInterface_contributions_02( ):
   '''Leaf comments contributions.'''

   t = Note(0, (1, 8))
   t.override.beam.thickness = 3
   t.comments.before.append('Comments before.')
   t.comments.opening.append('Comments opening.')
   t.comments.right.append('Comments right.')
   t.comments.closing.append('Comments closing.')
   t.comments.after.append('Comments after.')

   r'''
   % Comments before.
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

   assert componenttools.is_well_formed_component(t)
   assert result == (('before', ('Comments before.',)), ('opening', ('Comments opening.',)), ('right', ('Comments right.',)), ('closing', ('Comments closing.',)), ('after', ('Comments after.',)))


def test_CommentsInterface_contributions_03( ):
   '''Tuplet comments contributions.'''

   t = FixedDurationTuplet((2, 8), macros.scale(3))
   beam = BeamSpanner(t[:])
   beam.thickness = 3
   t.comments.before.append('Comments before.')
   t.comments.opening.append('Comments opening.')
   t.comments.right.append('Unacknowledged comments right.')
   t.comments.closing.append('Comments closing.')
   t.comments.after.append('Comments after.')

   r'''
   % Comments before.
   \times 2/3 {
           % Comments opening.
           \override Beam #'thickness = #3
           c'8 [
           d'8
           e'8 ]
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

   assert result == (('before', ('Comments before.',)), ('opening', ('Comments opening.',)), ('right', ('Unacknowledged comments right.',)), ('closing', ('Comments closing.',)), ('after', ('Comments after.',)))


def test_CommentsInterface_contributions_04( ):
   '''Measure comments contributions.'''

   t = RigidMeasure((3, 8), macros.scale(3))
   beam = BeamSpanner(t[:])
   beam.thickness = 3
   t.comments.before.append('Comments before.')
   t.comments.opening.append('Comments opening.')
   t.comments.right.append('Unacknowledged comments right.')
   t.comments.closing.append('Comments closing.')
   t.comments.after.append('Comments after.')

   r'''
   % Comments before.
           % Comments opening.
           \time 3/8
           \override Beam #'thickness = #3
           c'8 [
           d'8
           e'8 ]
           \revert Beam #'thickness
           % Comments closing.
   % Comments after.'''

   result = t.comments.contributions

   (('before', ('Comments before.',)),
    ('opening', ('Comments opening.',)),
    ('right', ('Unacknowledged comments right.',)),
    ('closing', ('Comments closing.',)),
    ('after', ('Comments after.',)))

   assert result == (('before', ('Comments before.',)), ('opening', ('Comments opening.',)), ('right', ('Unacknowledged comments right.',)), ('closing', ('Comments closing.',)), ('after', ('Comments after.',)))
