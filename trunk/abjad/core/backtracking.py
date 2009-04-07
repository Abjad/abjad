from abjad.core.abjadcore import _Abjad


class _BacktrackingInterface(_Abjad):

   def __init__(self, _watched_attr):
      self._watched_attr = _watched_attr

   @property
   def change(self):
      '''True when _watched_attr changes here, otherwise False.'''
      if getattr(self.client, 'prev', None):
         interface, attr = self._watched_attr.split('.')
         prev = getattr(self.client.prev, interface)
         prev = getattr(prev, attr)
         cur = getattr(self, attr)
         return not prev == cur
      return False
