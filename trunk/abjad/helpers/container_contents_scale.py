from abjad.helpers.is_tie_chain import _is_tie_chain
from abjad.helpers.iterate import iterate
from abjad.helpers.iterate_chained_contents import iterate_chained_contents
from abjad.helpers.leaf_duration_scale import leaf_duration_scale
from abjad.helpers.tie_chain_duration_scale import tie_chain_duration_scale
from abjad.helpers.tuplet_scale import tuplet_scale
from abjad.leaf.leaf import _Leaf
from abjad.tuplet.fd.tuplet import FixedDurationTuplet


def container_contents_scale(container, multiplier):
   '''Change all leaves in measure by multiplier.
      Return measure.

      TODO: generalize this helper to work on tuplets, too.
      TODO: generalize to work with rigid measures, too.'''

   for expr in iterate_chained_contents(container[:]):
      if _is_tie_chain(expr):
         tie_chain_duration_scale(expr, multiplier)
      elif isinstance(expr, FixedDurationTuplet):
         tuplet_scale(expr, multiplier)
      else:
         raise Exception(NotImplemented)
