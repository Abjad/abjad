from abjad.exceptions.exceptions import MissingSpannerError
from abjad.helpers.is_tie_chain import _is_tie_chain


def tie_chain_written(tie_chain):
   assert _is_tie_chain(tie_chain)
   try:
      return tie_chain[0].tie.spanner.duration.written
   except MissingSpannerError:
      return tie_chain[0].duration.written
