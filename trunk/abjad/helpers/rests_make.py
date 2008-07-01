from abjad.rest.rest import Rest
from abjad.helpers.duration_token_decompose import _duration_token_decompose

def rests_make(dur, pitch=None):
   '''Make rest(s) by splitting dur if necessary.
   Ties are automatically added.
   Returns a list of Notes.'''
   result = [ ]
   for wd in _duration_token_decompose(dur):
      rest =  Rest(wd)
      rest.pitch = pitch
      result.append( rest )
   return result

