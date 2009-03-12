from abjad.core.abjadcore import _Abjad


class _SpannerReceipt(_Abjad):
   '''Class to encapsulate pairs describing the spanners
      that used to attach to an Abjad component.'''

   def __init__(self, component):
      self._component = component
      self._pairs = set([ ])

   ## PRIVATE METHODS ##

   def _empty(self):
      self._component = None
      self._pairs.clear( )
