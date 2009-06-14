from abjad.measure.rigid.measure import RigidMeasure
#from abjad.skip.skip import Skip
from abjad.skip import Skip


def _rational_to_whitespace_measure_string(duration):
   '''Turn rational into whitespace measure string.'''

   ## make measure with hidden staff and hidden time signature
   measure = RigidMeasure(duration, [Skip((1, 1))])
   measure[0].duration.multiplier = duration
   measure.meter.stencil = False
   measure.meter.promote('stencil', 'Staff')
   measure.staff.hide = True

   ## return measure string
   return measure.format
