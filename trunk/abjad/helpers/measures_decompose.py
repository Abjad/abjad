from abjad.tools import mathtools
from abjad.tools import iterate
from abjad.measure.rigid.measure import RigidMeasure


def measures_decompose(expr):
   '''Decompose all measures in expr.'''

   result = [ ]

   # manifest list to avoid change-while-iterate recursion problem
   from abjad.measure.measure import _Measure
   for measure in list(iterate.naive(expr, _Measure)):
      result.append(_measure_decompose(measure))
   return tuple(result)


def _measure_decompose(measure):
   '''Decompose measure.'''

   parent = measure.parentage.parent
   denominator = measure.meter.effective.denominator

   new_measures = [ ]
   for element in measure[:]:
      meter = element.duration.prolated
      meter = mathtools.in_terms_of(meter, denominator)
      element.parentage._cut( )
      new = RigidMeasure(meter, [element])
      new_measures.append(new)
   measure.splice(new_measures)
   measure.detach( )
   measure[:] = [ ]
   return new_measures
