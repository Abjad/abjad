from abjad.exceptions import WellFormednessError
from abjad.tools.check.wf import wf as check_wf


def assert_wf(expr):
   '''Check `expr` for well-formedness.
   
   If `expr` is not well-formed, report violators
   and raise :exc:`WellFormednessError`. ::

      abjad> t = Staff(construct.scale(4))
      abjad> Beam(t[:])
      abjad> t._music.pop( )
   
   ::

      abjad> check.assert_wf(t)
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

   If `expr` is well-formed, return ``None``. ::

      abjad> t = Staff(construct.scale(4))
      abjad> Beam(t[:])
      abjad> t.pop( )

   ::

      abjad> check.assert_wf(t)
   '''

   if not check_wf(expr):
      check_wf(expr, delivery = 'report') 
      raise WellFormednessError
