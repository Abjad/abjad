from abjad.exceptions import MissingSpannerError
from abjad.tools.tietools.is_tie_chain import is_tie_chain


def get_written_tie_chain_duration(tie_chain):
   '''Return sum of written duration of all leaves in chain.'''

   assert is_tie_chain(tie_chain)

   try:
      return tie_chain[0].tie.spanner.duration.written
   except MissingSpannerError:
      return tie_chain[0].duration.written
