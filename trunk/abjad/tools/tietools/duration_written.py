from abjad.exceptions.exceptions import MissingSpannerError
from abjad.tools.tietools.is_tie_chain import is_tie_chain


def duration_written(tie_chain):
   assert is_tie_chain(tie_chain)
   try:
      return tie_chain[0].tie.spanner.duration.written
   except MissingSpannerError:
      return tie_chain[0].duration.written
