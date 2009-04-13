from abjad.leaf.leaf import _Leaf
from abjad.measure.measure import _Measure
from abjad.tools import iterate
from abjad.tools import tietools
from abjad.tools import tuplettools
from abjad.tuplet.fd.tuplet import FixedDurationTuplet


def contents_scale(container, multiplier):
   '''Change all leaves in measure by multiplier.
      Return measure.'''

   for expr in iterate.chained_contents(container[:]):
      if tietools.is_chain(expr):
         tietools.duration_scale(expr, multiplier)
      elif isinstance(expr, FixedDurationTuplet):
         tuplettools.contents_scale(expr, multiplier)
      elif isinstance(expr, _Measure):
         ## TODO: Move import to higher level of scope? ##
         from abjad.tools import measuretools
         measuretools.scale(expr, multiplier)
      else:
         raise Exception(NotImplemented)
