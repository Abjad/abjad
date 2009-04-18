from abjad.layout.systemindicator import FixedSystemIndicator
from abjad.measure.measure import _Measure
from abjad.tools import iterate


def fixed_systems_apply(expr, system_indicator, klass = _Measure):
   '''Apply fixed system distances to expr.
      Expr must already be marked with line breaks.'''

   if not isinstance(system_indicator, FixedSystemIndicator):
      raise TypeError

   yOffsetTuple = system_indicator.yOffsetTuple
   systems_per_page = len(yOffsetTuple)

   line_breaks_found = 0
   prev = None
   for cur in iterate.naive(expr, klass):
      if prev is None or prev.breaks.line:
         system_on_page = (line_breaks_found + 
            system_indicator.startingSystem) % \
            systems_per_page
         yOffset = yOffsetTuple[system_on_page]
         cur.breaks.y = yOffset
         line_breaks_found += 1
         if system_on_page == 0:
            if prev is not None:
               prev.breaks.page = True
      prev = cur
