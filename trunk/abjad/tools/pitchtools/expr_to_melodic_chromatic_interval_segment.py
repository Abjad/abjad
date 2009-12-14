from abjad.tools import listtools
from abjad.tools.pitchtools.MelodicChromaticIntervalSegment import \
   MelodicChromaticIntervalSegment
from abjad.tools.pitchtools.get_pitches import get_pitches
from abjad.tools.pitchtools.melodic_chromatic_interval_from_to import \
   melodic_chromatic_interval_from_to


def expr_to_melodic_chromatic_interval_segment(expr):
   '''.. versionadded:: 1.1.2

   Return melodic chromatic interval segment corresponding to
   arbitrary input `expr`.  ::

      abjad> staff = Staff(construct.scale(8))
      abjad> pitchtools.expr_to_melodic_chromatic_interval_segment(staff)
      MelodicChromaticIntervalSegment(+2, +2, +1, +2, +2, +2, +1)
   '''

   pitches = get_pitches(expr)
   mcis = [ ]
   for left, right in listtools.pairwise(pitches):
      mci = melodic_chromatic_interval_from_to(left, right)
      mcis.append(mci)

   return MelodicChromaticIntervalSegment(mcis)
