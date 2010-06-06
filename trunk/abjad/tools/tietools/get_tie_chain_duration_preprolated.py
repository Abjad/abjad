from abjad.exceptions import MissingSpannerError
from abjad.tools.tietools.is_chain import is_chain as tietools_is_chain


def get_tie_chain_duration_preprolated(tie_chain):
   '''Get sum of preprolated duration of all leaves in `tie_chain`.
   
   .. todo:: write ``tietools.get_tie_chain_duration_preprolated( )`` tests.

   .. versionchanged:: 1.1.2
      renamed ``tietools.get_duration_preprolated( )`` to
      ``tietools.get_tie_chain_duration_preprolated( )``.
   '''

   assert tietools_is_chain(tie_chain)

   try:
      return tie_chain[0].tie.spanner.duration.preprolated
   except MissingSpannerError:
      return tie_chain[0].duration.preprolated
