from abjad.components._Measure import RigidMeasure
from abjad.components.Skip import Skip
from abjad.tools import measuretools
from abjad.tools import overridetools


def _rational_to_whitespace_measure_string(duration):
   '''Turn rational into whitespace measure string.'''

   ## make measure with hidden staff and hidden time signature
   measure = measuretools.make_rigid_measures_with_full_measure_spacer_skips([duration])[0]
   measure.meter.stencil = False
   overridetools.promote_attribute_to_context_on_grob_handler(measure.meter, 'stencil', 'Staff')
   measure.staff.hide = True

   ## return measure string
   return measure.format
