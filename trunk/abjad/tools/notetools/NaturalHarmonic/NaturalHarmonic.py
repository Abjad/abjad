from abjad.components.Note import Note
from abjad.tools.notetools._Harmonic._Harmonic import _Harmonic


class NaturalHarmonic(Note, _Harmonic):
   '''Natural harmonic.
   '''

   def __init__(self, *args):
      Note.__init__(self, *args)
      self.override.note_head.style = 'harmonic'
         
   ## OVERLOADS ##

   def __repr__(self):
      return '%s(%s, %s)' % (self.__class__.__name__, self.pitch, self.duration)
