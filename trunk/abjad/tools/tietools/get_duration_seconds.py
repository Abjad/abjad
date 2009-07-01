from abjad.exceptions import MissingSpannerError
from abjad.tools.tietools.is_chain import is_chain as tietools_is_chain


def duration_seconds(tie_chain):
   '''Return sum of seconds duration of all leaves in chain.

   .. todo:: Write tietools.get_duration_seconds( ) tests.
   '''

   assert tietools_is_chain(tie_chain)

   try:
      return tie_chain[0].tie.spanner.duration.seconds
   except MissingSpannerError:
      return tie_chain[0].duration.seconds
