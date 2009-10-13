from abjad.interfaces.interface.interface import _Interface


class BracketsInterface(_Interface):

   ## PUBLIC ATTRIBUTES ##

   @property
   def close(self):
      '''Format contribution list with close bracket symbol.'''
      if self.container.parallel:
         return ['>>']
      else:
         return ['}']

   @property
   def container(self):
      '''Container to which this interface serves information.'''
      return self._client

   @property
   def open(self):
      '''Format contribution list with open bracket symbol.'''
      if self.container.parallel:
         return ['<<']
      else:
         return ['{']
