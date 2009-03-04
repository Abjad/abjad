from abjad.exceptions.exceptions import TieChainError
from abjad.helpers.is_tie_chain import _is_tie_chain


def _get_tie_chain_written(tie_chain):
   '''Return sum of written duration of all leaves in tie chain.'''

   if not _is_tie_chain(tie_chain):
      raise TieChainError('input must be tie chain.')

   return sum([x.duration.written for x in tie_chain])
