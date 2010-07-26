from abjad.exceptions import MissingSpannerError
from abjad.tools.tietools.is_tie_chain import is_tie_chain


def get_tie_chain_preprolated_duration(tie_chain):
   '''Get sum of preprolated duration of all leaves in `tie_chain`.
   
   .. todo:: write ``tietools.get_tie_chain_preprolated_duration( )`` tests.

   .. versionchanged:: 1.1.2
      renamed ``tietools.get_duration_preprolated( )`` to
      ``tietools.get_tie_chain_preprolated_duration( )``.

   .. versionchanged:: 1.1.2
      renamed ``tietools.get_tie_chain_duration_preprolated( )`` to
      ``tietools.get_tie_chain_preprolated_duration( )``.
   '''

   assert is_tie_chain(tie_chain)

   try:
      return tie_chain[0].tie.spanner.duration.preprolated
   except MissingSpannerError:
      return tie_chain[0].duration.preprolated
