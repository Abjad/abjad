from abjad.exceptions import MissingSpannerError
from abjad.tools import spannertools
from abjad.tools.tietools.is_tie_chain import is_tie_chain


def get_preprolated_tie_chain_duration(tie_chain):
   '''Get sum of preprolated duration of all leaves in `tie_chain`.
   
   .. todo:: write ``tietools.get_preprolated_tie_chain_duration( )`` tests.

   .. versionchanged:: 1.1.2
      renamed ``tietools.get_duration_preprolated( )`` to
      ``tietools.get_preprolated_tie_chain_duration( )``.

   .. versionchanged:: 1.1.2
      renamed ``tietools.get_tie_chain_duration_preprolated( )`` to
      ``tietools.get_preprolated_tie_chain_duration( )``.

   .. versionchanged:: 1.1.2
      renamed ``tietools.get_tie_chain_preprolated_duration( )`` to
      ``tietools.get_preprolated_tie_chain_duration( )``.
   '''

   assert is_tie_chain(tie_chain)

   try:
      #return tie_chain[0].tie.spanner.duration.preprolated
      tie_spanner = spannertools.get_the_only_spanner_attached_to_component(
         tie_chain[0], spannertools.TieSpanner)
      return tie_spanner.duration.preprolated
   except MissingSpannerError:
      return tie_chain[0].duration.preprolated
