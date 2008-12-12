from abjad.core.abjadcore import _Abjad
import abjad.pitch.initializers as initializers


class _PitchInitializer(_Abjad):
   
   def __init__(self): 
      self.initializers = [ ]
      for value in initializers.__dict__.itervalues( ):
         if hasattr(value, 'matchSignature'):
            self.initializers.append(value( ))

   def initialize(self, client, *args):
      for i in self.initializers:
         if i.matchSignature(*args):
            i.initialize(client, *args)
            return True
      raise ValueError('can not initialize pitch.')
