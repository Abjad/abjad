from abjad.rest.rest import Rest
from abjad.helpers.duration_token_decompose import _duration_token_decompose

def rests_make(dur, pitch=None):
   '''Make (pitched) rest(s) by splitting dur if necessary.
   Returns a list of Rests.'''
   result = [ ]
   for wd in _duration_token_decompose(dur):
      rest =  Rest(wd)
      rest.pitch = pitch
      result.append( rest )
   return result

