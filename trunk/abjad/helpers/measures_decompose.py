from abjad.helpers.in_terms_of import _in_terms_of
from abjad.helpers.iterate import iterate
from abjad.helpers.splice_after import splice_after
from abjad.measure.rigid.measure import RigidMeasure


def measures_decompose(expr):
   '''Decompose all measures in expr.'''

   result = [ ]

   # manifest list to avoid change-while-iterate recursion problem
   for measure in list(iterate(expr, '_Measure')):
      result.append(_measure_decompose(measure))
   return tuple(result)


def _measure_decompose(measure):
   '''Decompose measure.'''

   parent = measure.parentage.parent
   denominator = measure.meter.effective.denominator

   new_measures = [ ]
   for element in measure[:]:
      meter = element.duration.prolated
      meter = _in_terms_of(meter, denominator)
      element.parentage.detach( )
      new = RigidMeasure(meter, [element])
      new_measures.append(new)
   splice_after(measure, new_measures)
   measure.detach( )
   measure[:] = [ ]
   return new_measures
