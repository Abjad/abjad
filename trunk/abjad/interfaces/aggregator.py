from abjad.core.interface import _Interface


class _InterfaceAggregator(_Interface):

   def __init__(self, client):
      _Interface.__init__(self, client)

   ## PUBLIC ATTRIBUTES ##

   @property
   def contributions(self):
      '''Ordered data structure of format-time contributions.'''
      result = [ ]
      for contributor in self.contributors:
         result.extend(getattr(contributor, '_grobOverrides', [ ]))
      return result

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

   ## PUBLIC METHODS ##

   def report(self, delivery = 'screen'):
      '''Docs.'''
      pass
