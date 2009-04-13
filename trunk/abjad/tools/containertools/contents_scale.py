from abjad.helpers.leaf_duration_scale import leaf_duration_scale
from abjad.helpers.tuplet_scale import tuplet_scale
from abjad.leaf.leaf import _Leaf
from abjad.measure.measure import _Measure
from abjad.tools import iterate
from abjad.tools import tietools
from abjad.tuplet.fd.tuplet import FixedDurationTuplet


def contents_scale(container, multiplier):
   '''Change all leaves in measure by multiplier.
      Return measure.'''

   for expr in iterate.chained_contents(container[:]):
      if tietools.is_chain(expr):
         tietools.duration_scale(expr, multiplier)
      elif isinstance(expr, FixedDurationTuplet):
         tuplet_scale(expr, multiplier)
      elif isinstance(expr, _Measure):
         ## TODO: Move import to higher level of scope? ##
         from abjad.helpers.measures_scale import measures_scale
         measures_scale(expr, multiplier)
      else:
         raise Exception(NotImplemented)
