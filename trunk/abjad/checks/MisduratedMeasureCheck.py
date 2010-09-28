from abjad.checks._Check import _Check


class MisduratedMeasureCheck(_Check):
   '''Does the (pre)prolated duration of the measure match its meter?'''

   def _run(self, expr):
      from abjad.tools import contexttools
      from abjad.tools import measuretools
      violators = [ ]
      total, bad = 0, 0
      for t in measuretools.iterate_measures_forward_in_expr(expr):
         if contexttools.get_effective_time_signature(t) is not None:
            if t.duration.preprolated != contexttools.get_effective_time_signature(t).duration:
               violators.append(t)
               bad += 1
         total += 1
      return violators, total
