from abjad.core import _Immutable


class _Quantizer(_Immutable):

   ## OVERRIDES ##

   def __call__(self, timepoints):
      return self.quantize_timepoints(timepoints)

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._format_string)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _format_string(self):
      return ' '

   ## PUBLIC METHODS ##

   def quantize_ms_to_tempo(self, timepoints):
      raise Exception('Not implemented in %s' % (self.__class__.__name__))

   def quantize_tempo_to_tempo(self, timepoints, tempo):
      raise Exception('Not implemented in %s' % (self.__class__.__name__))
