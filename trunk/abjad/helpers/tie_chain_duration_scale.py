from abjad.helpers.is_tie_chain import _is_tie_chain
from abjad.helpers.tie_chain_duration_change import tie_chain_duration_change
from abjad.helpers.tie_chain_written import tie_chain_written
from abjad.rational.rational import Rational


def tie_chain_duration_scale(tie_chain, multiplier):
   '''Scale tie chain by multiplier.
      Wraps tie_chain_duration_change.
      Returns tie chain.'''

   # find new tie chain written duration
   new_written_duration = multiplier * tie_chain_written(tie_chain)

   # assign new tie chain written duration and return tie chain
   return tie_chain_duration_change(tie_chain, new_written_duration)
