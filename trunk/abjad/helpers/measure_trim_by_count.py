from abjad.measure.measure import _Measure
from abjad.meter.meter import Meter
from abjad.tools import check
from abjad.tools import durtools
from abjad.tools import parenttools


def measure_trim_by_count(components):
   '''Remove components in 'components' from parent measure.
      Adjust meter of containing measure as necessary.

      abjad> t = RigidMeasure((3, 8), scale(3))
      abjad> measure_trim_by_count(t[:2])
      abjad> t
      RigidMeasure(1/8, [e'8])'''

   check.assert_components(components, contiguity = 'strict', share = 'parent')
   parent, start, stop = parenttools.get_with_indices(components)
   assert isinstance(parent, _Measure) 

   try:
      old_denominator = parent.meter.forced.denominator
   except AttributeError:
      pass

   del(parent[start:stop+1])

   try:
      naive_meter = parent.duration.preprolated
      better_meter = durtools.in_terms_of(naive_meter, old_denominator)
      parent.meter.forced = Meter(better_meter)
   except (AttributeError, UnboundLocalError):
      pass
