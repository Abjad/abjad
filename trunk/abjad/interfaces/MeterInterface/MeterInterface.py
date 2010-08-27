from abjad.interfaces._Interface import _Interface


class MeterInterface(_Interface):

   __slots__ = ('_client')

   ## PUBLIC ATTRIBUTES ##

   @property
   def effective(self):
      from abjad.tools.marktools.get_effective_time_signature import get_effective_time_signature
      from abjad.components.Measure._Measure import _Measure
      from abjad.tools import measuretools
      explicit_meter = getattr(self._client, '_explicit_meter', None)
      if explicit_meter is not None:
         return explicit_meter
      else:
         return get_effective_time_signature(self._client)
#      if isinstance(self._client, _Measure):
#         if isinstance(self._client, measuretools.DynamicMeasure):
#            self._client._update_explicit_meter( )
#         return self._client._explicit_meter
#      else:
#         return get_effective_time_signature(self._client)
