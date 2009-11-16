from abjad.tools import check
from abjad.tools import iterate


def extract_meter_list(components):
   '''Extract ordered list of meter pairs from ``components``.

   Example::

      abjad> t = Staff([RigidMeasure((2, 8), construct.scale(2)),
         RigidMeasure((3, 8), construct.scale(3)),
         RigidMeasure((4, 8), construct.scale(4))])

      abjad> metertools.extract_meter_list(t[:])
      [(2, 8), (3, 8), (4, 8)]

   Useful as input to some rhythmic transforms.
   '''

   ## make sure components is a Python list of Abjad components
   check.assert_components(components)

   ## create empty list to hold result
   result = [ ]

   ## iterate measures and store meter pairs
   for measure in iterate.measures_forward_in(components):
      meter = measure.meter.effective
      pair = (meter.numerator, meter.denominator)
      result.append(pair)

   ## return result
   return result
