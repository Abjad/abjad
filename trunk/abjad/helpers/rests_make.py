from abjad.helpers.duration_token_decompose import _duration_token_decompose
from abjad.rest.rest import Rest
from abjad.tie.spanner import Tie


def rests_make(dur, pitch=None):
   '''Make (pitched) rest(s) by splitting dur if necessary.
   Returns a list of Rests.'''
   result = [ ]
   for wd in _duration_token_decompose(dur):
      rest =  Rest(wd)
      rest.pitch = pitch
      result.append( rest )
   if len(result) > 1:
      Tie(result)
   return result
