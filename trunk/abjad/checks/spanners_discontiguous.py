from abjad.checks.check import _Check


class SpannersDiscontiguous(_Check):
   '''Spanner leaves must be contiguous.'''

   def _run(self, expr):
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
      return violators, total
