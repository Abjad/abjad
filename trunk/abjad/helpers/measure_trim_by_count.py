from abjad.helpers.assert_components import assert_components
from abjad.helpers.get_parent_and_indices import get_parent_and_indices
from abjad.helpers.in_terms_of import _in_terms_of
from abjad.measure.measure import _Measure


#def old_measure_trim_by_count(measure, start, stop = 'unused'):
#   '''When 'stop' is 'unusued', delete component at index 'start'.
#      When 'stop' is set, delete components from 'start' to 'stop'.
#      Measure may be anonymous, dynamic, rigid, etc.
#      When 'measure' is rigid, change meter as appropriate.'''
#
#   if not isinstance(measure, _Measure):
#      raise TypeError('must be Abjad measure.')
#
#   try:
#      old_denominator = measure.meter.forced.denominator
#   except AttributeError:
#      pass
#
#   if stop != 'unused':
#      assert not (start == 0 and (stop is None or stop >= len(measure)))
#   if stop == 'unused':
#      del(measure[start])
#   else:
#      del(measure[start : stop])
#
#   try:
#      naive_meter = measure.duration.preprolated
#      better_meter = _in_terms_of(naive_meter, old_denominator)
#      measure.meter = better_meter
#   except (AttributeError, UnboundLocalError):
#      pass


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
      parent.meter = better_meter
   except (AttributeError, UnboundLocalError):
      pass
