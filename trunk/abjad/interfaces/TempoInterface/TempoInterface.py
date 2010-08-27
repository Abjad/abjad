from abjad.interfaces._Interface import _Interface


class TempoInterface(_Interface):

   @property
   def effective(self):
      from abjad.tools.marktools.get_effective_tempo import get_effective_tempo
      return get_effective_tempo(self._client)
