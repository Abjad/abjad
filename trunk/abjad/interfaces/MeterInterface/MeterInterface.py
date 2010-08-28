from abjad.interfaces._Interface import _Interface


class MeterInterface(_Interface):

   __slots__ = ('_client')

   ## PUBLIC ATTRIBUTES ##

   @property
   def effective(self):
      from abjad.tools.marktools.get_effective_time_signature import get_effective_time_signature
      explicit_meter = getattr(self._client, '_explicit_meter', None)
      if explicit_meter is not None:
         return explicit_meter
      else:
         return get_effective_time_signature(self._client)
