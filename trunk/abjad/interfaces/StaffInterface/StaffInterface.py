from abjad.interfaces._Interface import _Interface


class StaffInterface(_Interface):

   @property
   def effective(self):
      from abjad.tools import marktools
      return marktools.get_effective_staff(self._client)
