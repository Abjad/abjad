from abjad.tie import Tie
from abjad.tools import durtools

def _construct_tied_leaf(kind, dur, direction='big-endian', pitches=None, 
   tied=True):
   '''Return list of leaves to fill the given duration ``dur``. 
      Leaves returned are Tie-spanned.

      `dur`
         must be of the form m / 2**n for any m integer.

      `direction`
          may be 'big-endian' or 'little-endian'.
          'big-endian' returns a list of notes of decreasing duration.
          'little-endian' returns a list of notes of increasing duration.

      `pitches` 
         a pitch or list of pitch tokens.

      `tied`
         True to return tied leaves, False otherwise. Defaults to True.'''

   result = [ ]
   for wd in durtools.token_decompose(dur):
      if not pitches is None:
         args = (pitches, wd)
      else:
         args = (wd, )
      result.append( kind(*args) )
   if len(result) > 1:
      if direction == 'little-endian':
         result.reverse( )
      if tied:
         Tie(result)
   return result
