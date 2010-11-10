from abjad.checks._Check import _Check
from abjad.tools import durtools


class BeamedQuarterNoteCheck(_Check):

   def _run(self, expr):
      from abjad.tools import beamtools
      from abjad.tools import leaftools
      from abjad.tools.spannertools import DuratedComplexBeamSpanner
      violators = [ ]
      total = 0
      for leaf in leaftools.iterate_leaves_forward_in_expr(expr):
         total += 1
         if hasattr(leaf, 'beam'):
            #if leaf.beam.spanned:
            if beamtools.is_component_with_beam_spanner_attached(leaf):
               #beam = leaf.beam.spanner
               beam = beamtools.get_beam_spanner_attached_to_component(leaf)
               #if not beam.__class__.__name__ == 'DuratedComplexBeam':
               if not isinstance(beam, DuratedComplexBeamSpanner):
                  flag_count = durtools.rational_to_flag_count(leaf.duration.written)
                  if flag_count < 1:
                     violators.append(leaf)
      return violators, total
