from abjad.wf.tools import _report


def check_spanner_contiguity(expr, report = True, ret = 'violators'):
   violators = [ ]
   total, bad = 0, 0
   ### TODO - remove 'interface' from spanners.get ###
   spanners = expr.spanners.get( )
   for spanner in spanners:
      contiguousLeaves = True
      for i, leaf in enumerate(spanner[:-1]):
         if leaf.next != spanner[i + 1]:
            contiguousLeaves = False
      if not contiguousLeaves:
         violators.append(spanner)
      total += 1
   msg = 'spanners with noncontiguous leaves.'
   return _report(report, ret, violators, total, msg)
