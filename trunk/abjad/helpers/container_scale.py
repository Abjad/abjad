from abjad.tools import tiechaintools
from abjad.tools import iterate
from abjad.tools import iterate
from abjad.helpers.leaf_duration_scale import leaf_duration_scale
from abjad.tools import tiechaintools
from abjad.helpers.tuplet_scale import tuplet_scale
from abjad.leaf.leaf import _Leaf
from abjad.measure.measure import _Measure
from abjad.tuplet.fd.tuplet import FixedDurationTuplet


def container_scale(container, multiplier):
   '''Change all leaves in measure by multiplier.
      Return measure.'''

   for expr in iterate.chained_contents(container[:]):
      if tiechaintools.is_tie_chain(expr):
         tiechaintools.duration_scale(expr, multiplier)
      elif isinstance(expr, FixedDurationTuplet):
         tuplet_scale(expr, multiplier)
      elif isinstance(expr, _Measure):
         from abjad.helpers.measures_scale import measures_scale
         measures_scale(expr, multiplier)
      else:
         raise Exception(NotImplemented)
