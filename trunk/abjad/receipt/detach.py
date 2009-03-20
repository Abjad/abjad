from abjad.core.abjadcore import _Abjad


class _DetachReceipt(_Abjad):
   '''Well structured references attaching to some Abjad component.
      Hand over after entire subtree detaches from score.

      TODO: Implement dictionary of children and their spanners.'''

   def __init__(self, component, parentage, spanners):
      self._component = component
      self._parentage = parentage
      self._spanners = spanners

   ## PRIVATE METHODS ##

   def _empty(self):
      self._component = None
      self._parentage = None
      self._spanners = None
