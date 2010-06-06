from abjad.exceptions import MissingSpannerError
from abjad.tools.tietools.is_chain import is_chain


def get_duration_prolated(tie_chain):
   '''Return sum of prolated duration of all leaves in chain.

   .. todo:: Write tietools.get_duration_prolated( ) tests.
   '''

   assert is_chain(tie_chain)

   try:
      return tie_chain[0].tie.spanner.duration.prolated
   except MissingSpannerError:
      return tie_chain[0].duration.prolated
