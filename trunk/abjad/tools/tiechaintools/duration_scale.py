from abjad.rational.rational import Rational
from abjad.tools.tiechaintools.is_tie_chain import is_tie_chain
from abjad.tools.tiechaintools.duration_change import duration_change
from abjad.tools.tiechaintools.duration_written import duration_written


def duration_scale(tie_chain, multiplier):
   '''Scale tie chain by multiplier.
      Wraps tie_chain_duration_change.
      Returns tie chain.'''

   # find new tie chain written duration
   new_written_duration = multiplier * duration_written(tie_chain)

   # assign new tie chain written duration and return tie chain
   return duration_change(tie_chain, new_written_duration)
