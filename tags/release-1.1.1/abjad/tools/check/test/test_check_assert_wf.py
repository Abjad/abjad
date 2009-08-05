from abjad import *
import py.test


def test_tools_check_assert_wf_01( ):
   '''Report violators and raise WellFormednessError
   when not well formed.'''

   t = Staff(construct.scale(4))
   Beam(t[:])
   t._music.pop( )

   '''
   0 /    1 beams overlapping
   0 /    1 containers empty
   0 /    3 flags misrepresented
   0 /    0 glissandi overlapping
   0 /    0 hairpins intermarked
   0 /    0 hairpins short
   0 /    4 ids duplicated
   0 /    0 measures improperly filled
   0 /    0 measures misdurated
   0 /    0 measures nested
   0 /    0 octavations overlapping
   0 /    4 parents missing
   0 /    3 quarters beamed
   1 /    1 spanners discontiguous
   0 /    3 ties mispitched
   '''

   assert py.test.raises(WellFormednessError, 'check.assert_wf(t)')


def test_tools_check_assert_wf_02( ):
   '''Pass silently when well formed.'''

   t = Staff(construct.scale(4))
   Beam(t[:])
   t.pop( )

   assert check.assert_wf(t) is None
