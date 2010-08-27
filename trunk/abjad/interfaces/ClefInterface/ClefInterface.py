from abjad.interfaces._Interface import _Interface


class ClefInterface(_Interface):

   @property
   def effective(self):
      from abjad.tools.marktools.get_effective_clef import get_effective_clef
      return get_effective_clef(self._client)
