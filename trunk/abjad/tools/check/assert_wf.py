from abjad.exceptions import WellFormednessError
from abjad.tools.check.wf import wf


def assert_wf(expr):
   '''Return none when `expr` is well-formed. ::

      abjad> staff = Staff(construct.scale(4))
      abjad> check.assert_wf(staff) is None
      True      

   Report violators and raise well-formedness error
   when `expr` is not well-formed. ::

      abjad> staff = Staff(construct.scale(4))
      abjad> Beam(staff[:])
      abjad> staff._music.pop( )
      abjad> check.assert_wf(staff)
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
      WellFormednessError
   '''

   if not wf(expr):
      wf(expr, delivery = 'report') 
      raise WellFormednessError
