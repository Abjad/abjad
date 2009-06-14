from abjad.exceptions import MissingSpannerError
from abjad.tools.tietools.is_chain import is_chain as tietools_is_chain


def get_duration_written(tie_chain):
   '''Return sum of written duration of all leaves in chain.'''

   assert tietools_is_chain(tie_chain)

   try:
      return tie_chain[0].tie.spanner.duration.written
   except MissingSpannerError:
      return tie_chain[0].duration.written
