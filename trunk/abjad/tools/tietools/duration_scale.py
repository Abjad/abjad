from abjad.rational.rational import Rational
from abjad.tools.tietools.is_chain import is_chain
from abjad.tools.tietools.duration_change import duration_change as \
   tietools_duration_change
from abjad.tools.tietools.duration_written import duration_written as \
   tietools_duration_written


def duration_scale(tie_chain, multiplier):
   '''Scale tie chain by multiplier.
      Wraps tie_chain_duration_change.
      Returns tie chain.'''

   ## find new tie chain written duration
   new_written_duration = multiplier * tietools_duration_written(tie_chain)

   ## assign new tie chain written duration and return tie chain
   return tietools_duration_change(tie_chain, new_written_duration)
