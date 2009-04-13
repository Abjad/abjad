from abjad.measure.measure import _Measure
from abjad.measure.rigid.measure import RigidMeasure
from abjad.tools import componenttools
from abjad.tools import durtools
from abjad.tools import iterate


def decompose(expr):
   '''Decompose all measures in expr.'''

   result = [ ]

   # manifest list to avoid change-while-iterate recursion problem
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
      meter = durtools.in_terms_of(meter, denominator)
      element.parentage._cut( )
      new = RigidMeasure(meter, [element])
      new_measures.append(new)
   measure.splice(new_measures)
   componenttools.detach([measure])
   measure[:] = [ ]
   return new_measures
