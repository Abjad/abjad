from abjad.helpers.assert_components import assert_components
from abjad.helpers.get_parent_and_indices import get_parent_and_indices
from abjad.helpers.in_terms_of import _in_terms_of
from abjad.measure.measure import _Measure
from abjad.meter.meter import Meter


def measure_trim_by_count(components):
   '''Remove components in 'components' from parent measure.
      Adjust meter of containing measure as necessary.

      abjad> t = RigidMeasure((3, 8), scale(3))
      abjad> measure_trim_by_count(t[:2])
      abjad> t
      RigidMeasure(1/8, [e'8])'''

   assert_components(components, contiguity = 'strict', share = 'parent')
   parent, start, stop = get_parent_and_indices(components)
   assert isinstance(parent, _Measure) 

   try:
      old_denominator = parent.meter.forced.denominator
   except AttributeError:
      pass

   del(parent[start:stop+1])

   try:
      naive_meter = parent.duration.preprolated
      better_meter = _in_terms_of(naive_meter, old_denominator)
      parent.meter.forced = Meter(better_meter)
   except (AttributeError, UnboundLocalError):
      pass
