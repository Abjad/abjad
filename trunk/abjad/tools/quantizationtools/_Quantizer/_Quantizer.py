from abjad.core import _Immutable


class _Quantizer(_Immutable):

   ## OVERRIDES ##

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._format_string)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _format_string(self):
      return ' '

   ## PUBLIC METHODS ##

   def quantize_milliseconds(self, durations):
      raise Exception('Not implemented in %s' % (self.__class__.__name__))

   def quantize_rationals(self, durations, tempo):
      raise Exception('Not implemented in %s' % (self.__class__.__name__))
