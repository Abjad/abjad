from abjad.core.abjadcore import _Abjad


class _FormatContributor(_Abjad):

   def __init__(self):
      self._register_as_format_contributor( )

   ## PRIVATE METHODS ##

   def _register_as_format_contributor(self):
      from abjad.interfaces._Interface import _Interface
      if isinstance(self, _Interface):
         client = getattr(self, '_client', None)
         if client is not None:
            self._client._interfaces._contributors.append(self)
