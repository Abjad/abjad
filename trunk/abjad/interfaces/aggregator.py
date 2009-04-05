from abjad.core.interface import _Interface


class _InterfaceAggregator(_Interface):

   def __init__(self, client):
      _Interface.__init__(self, client)

   ## PUBLIC ATTRIBUTES ##

   @property
   def after(self):
      '''Ordered list of format-time contributions for after format slot.'''
      result = [ ]
      for contributor in self.contributors:
         result.extend(getattr(contributor, 'after', [ ]))
      return result

   @property
   def before(self):
      '''Ordered list of format-time contributions for before format slot.'''
      result = [ ]
      for contributor in self.contributors:
         result.extend(getattr(contributor, 'before', [ ]))
      return result

   @property
   def closing(self):
      '''Ordered list of format-time contributions for closing format slot.'''
      result = [ ]
      for contributor in self.contributors:
         result.extend(getattr(contributor, 'closing', [ ]))
      return result

   @property
   def contributors(self):
      '''Return alphabetized list of interface format contributors.
         Does not include spanner format contributors.'''
      from abjad.core.formatcontributor import _FormatContributor
      result = [ ]
      client = self._client
      for value in client.__dict__.values( ):
         if isinstance(value, _Interface) and \
            isinstance(value, _FormatContributor):
            result.append(value)
      result.sort(lambda x, y: 
         cmp(x.__class__.__name__, y.__class__.__name__))
      return result

   @property
   def contributions(self):
      '''Returns an ordered list of contribution triples.'''
      result = [ ]
      locations = self._client.formatter._knownFormatLocations
      for contributor in self.contributors:
         for location in locations:
            contributions = getattr(contributor, location, None)
            if contributions:
               result.append((contributor, location, contributions))
      return result
   
   @property
   def left(self):
      '''Ordered list of format-time contributions for left format slot.'''
      result = [ ]
      for contributor in self.contributors:
         result.extend(getattr(contributor, 'left', [ ]))
      return result

   @property
   def opening(self):
      '''Ordered list of format-time contributions for opening format slot.'''
      result = [ ]
      for contributor in self.contributors:
         result.extend(getattr(contributor, 'opening', [ ]))
      return result

   @property
   def overrides(self):
      '''Ordered data structure of format-time grob overrides.'''
      result = [ ]
      for contributor in self.contributors:
         result.extend(getattr(contributor, 'overrides', [ ]))
      return result

   @property
   def reverts(self):
      '''Ordered data structure of format-time grob reverts.'''
      result = [ ]
      for contributor in self.contributors:
         result.extend(getattr(contributor, 'reverts', [ ]))
      return result

   @property
   def right(self):
      '''Ordered list of format-time contributions for right format slot.'''
      result = [ ]
      for contributor in self.contributors:
         result.extend(getattr(contributor, 'right', [ ]))
      return result

   ## PUBLIC METHODS ##

   def report(self, delivery = 'screen'):
      '''Docs.'''
      pass
