from abjad.helpers.instances import instances
from abjad.wf.tools import _report


def check_beamed_quarters(expr, report = True, ret = 'violators'):
   violators = [ ]
   leaves = instances(expr, '_Leaf')
   for leaf in leaves:
      if hasattr(leaf, 'beam'):
         if leaf.beam.spanned:
            beam = leaf.beam.spanner
            if not beam.__class__.__name__ == 'ComplexBeam':
               if leaf.beam._flags < 1:
                  violators.append(leaf)
   bad = len(violators)
   total = len(leaves)
   msg = 'quarter (or greater) durations in beam.'
   return _report(report, ret, violators, total, msg)
