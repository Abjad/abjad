from abjad.core.interface import _Interface


class _UserDirectivesInterface(_Interface):

   def __init__(self, client):
      self._client = client
      self.before = [ ]
      self.opening = [ ]
      self.left = [ ]
      self.right = [ ]
      self.closing = [ ]
      self.after = [ ]

   ## PUBLIC METHODS ##

   def report(self, delivery = 'screen'):
      '''Report format-time contributions.
         Order contributions first by location.'''
      result = '\n%s\n' % self
      locations = self._client.formatter._knownFormatLocations
      for location in locations:
         contribution = getattr(self, location.strip('_'), [ ])
         if contribution:
            result += '\t%s\n' % location
            for directive in contribution:
               result += '\t\t%s\n' % directive
      if delivery == 'screen':
         print result
      else:
         return result
