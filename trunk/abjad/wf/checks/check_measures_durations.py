from abjad.duration.rational import Rational
from abjad.helpers.instances import instances
from abjad.wf.tools import _report


def check_measures_durations(expr, report = True, ret = 'violators'):
   '''Does the prolated duration of the measure match its meter?'''
   violators = [ ]
   total, bad = 0, 0
   for t in instances(expr, 'Measure'):
      if t.meter is not None:
         if t.duration != t.meter.duration:
            violators.append(t)
            bad += 1
      total += 1
   return _report(report, ret, violators, total, 
         'measures with incongruent meter/duration.')
