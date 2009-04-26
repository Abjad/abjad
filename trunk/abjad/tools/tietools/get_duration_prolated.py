from abjad.exceptions.exceptions import MissingSpannerError
from abjad.tools.tietools.is_chain import is_chain as tietools_is_chain


## TODO: Write tests ##

def get_duration_prolated(tie_chain):
   '''Return sum of prolated duration of all leaves in chain.'''

   assert tietools_is_chain(tie_chain)

   try:
      return tie_chain[0].tie.spanner.duration.prolated
   except MissingSpannerError:
      return tie_chain[0].duration.prolated
