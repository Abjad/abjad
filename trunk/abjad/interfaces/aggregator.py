from abjad.core.interface import _Interface


class _InterfaceAggregator(_Interface):

   def __init__(self, client):
      _Interface.__init__(self, client)

   ## PUBLIC ATTRIBUTES ##

   @property
   def contributors(self):
      '''Return alphabetized list of interface format contributors.
         Does not include spanner format contributors.'''
      from abjad.core.formatcarrier import _FormatCarrier
      result = [ ]
      client = self._client
      for value in client.__dict__.values( ):
         if isinstance(value, _Interface) and \
            isinstance(value, _FormatCarrier):
            result.append(value)
      result.sort(lambda x, y: 
         cmp(x.__class__.__name__, y.__class__.__name__))
      return result

   @property
   def overrides(self):
      '''Ordered data structure of format-time grob overrides.'''
      result = [ ]
      for contributor in self.contributors:
         result.extend(getattr(contributor, '_grobOverrides', [ ]))
      return result

   @property
   def reverts(self):
      '''Ordered data structure of format-time grob reverts.'''
      result = [ ]
      for contributor in self.contributors:
         result.extend(getattr(contributor, '_grobReverts', [ ]))
      return result

   ## PUBLIC METHODS ##

   def report(self, delivery = 'screen'):
      '''Docs.'''
      pass
