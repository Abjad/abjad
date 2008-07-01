from abjad.note.note import Note
from abjad.helpers.duration_token_decompose import _duration_token_decompose

def notes_make(pitch, dur):
   '''Make note(s) by splitting dur if necessary. 
   Ties are automatically added.
   Returns a list of Notes.'''
   result = [ ]
   for wd in _duration_token_decompose(dur):
      result.append( Note(pitch, wd))
   ### tie notes
   for n in result[0:-1]:
      n.tie = True
   return result

