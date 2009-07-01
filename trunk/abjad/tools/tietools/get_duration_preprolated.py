from abjad.exceptions import MissingSpannerError
from abjad.tools.tietools.is_chain import is_chain as tietools_is_chain


def get_duration_preprolated(tie_chain):
   '''Return sum of preprolated duration of all leaves in chain.
   
   .. todo:: Write tietools.get_duration_preprolated( ) tests.
   '''

   assert tietools_is_chain(tie_chain)

   try:
      return tie_chain[0].tie.spanner.duration.preprolated
   except MissingSpannerError:
      return tie_chain[0].duration.preprolated
