from abjad.exceptions import MissingSpannerError
from abjad.tools.tietools.is_tie_chain import is_tie_chain


def get_prolated_tie_chain_duration(tie_chain):
   '''Return sum of prolated duration of all leaves in chain.

   .. todo:: Write tietools.get_prolated_tie_chain_duration( ) tests.

   .. versionchanged:: 1.1.2
      renamed ``tietools.get_duration_prolated( )`` to
      ``tietools.get_prolated_tie_chain_duration( )``.

   .. versionchanged:: 1.1.2
      renamed ``tietools.get_tie_chain_prolated_duration( )`` to
      ``tietools.get_prolated_tie_chain_duration( )``.
   '''

   assert is_tie_chain(tie_chain)

   try:
      return tie_chain[0].tie.spanner.duration.prolated
   except MissingSpannerError:
      return tie_chain[0].duration.prolated
