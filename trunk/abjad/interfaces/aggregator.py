from abjad.core.interface import _Interface


class _InterfaceAggregator(_Interface):

   def __init__(self, client):
      _Interface.__init__(self, client)

   ## PUBLIC ATTRIBUTES ##

   @property
   def contributions(self):
      '''Ordered data structure of format-time contributions.'''
      result = [ ]
      carriers = self._client.formatter._getFormatCarriers( )
      for carrier in carriers:
         result.extend(getattr(carrier, '_grobOverrides', [ ]))
      return result

   ## PUBLIC METHODS ##

   def report(self, delivery = 'screen'):
      '''Docs.'''
      pass
