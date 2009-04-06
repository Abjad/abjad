from abjad.core.interface import _Interface


class _BracketsInterface(_Interface):

   ## PUBLIC ATTRIBUTES ##

   @property
   def close(self):
      '''Close bracket symbol.'''
      if self.container.parallel:
         return '>>'
      else:
         return '}'

   @property
   def container(self):
      '''Container to which this interface serves information.'''
      return self._client

   @property
   def open(self):
      '''Open bracket symbol.'''
      if self.container.parallel:
         return '<<'
      else:
         return '{'
