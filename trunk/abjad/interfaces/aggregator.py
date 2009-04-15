from abjad.core.interface import _Interface


class _InterfaceAggregator(_Interface):
   '''Aggregate information about all format-contributing interfaces.'''

   def __init__(self, client):
      '''Bind to client.'''
      _Interface.__init__(self, client)
      self._contributors = [ ]
      self._contributors_sorted = False

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

#   @property
#   def contributors(self):
#      '''Return alphabetized list of interface format contributors.
#         Does not include spanner format contributors.'''
#      from abjad.core.formatcontributor import _FormatContributor
#      result = [ ]
#      client = self._client
#      for value in client.__dict__.values( ):
#         if isinstance(value, _Interface) and \
#            isinstance(value, _FormatContributor):
#            result.append(value)
#      result.sort(lambda x, y: 
#         cmp(x.__class__.__name__, y.__class__.__name__))
#      return result

   @property
   def contributors(self):
      if not self._contributors_sorted:
         self._contributors.sort(lambda x, y:
            cmp(x.__class__.__name__, y.__class__.__name__))
         self._contributors_sorted = True
      return self._contributors

   @property
   def contributions(self):
      '''Returns an ordered list of contribution triples.'''
      result = [ ]
      locations = ('before', 'overrides', 'opening', 'left', 
         'right', 'closing', 'reverts', 'after')
      for contributor in self.contributors:
         for location in locations:
            contributions = getattr(contributor, location, None)
            if contributions:
               result.append(((contributor, location), contributions))
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

   ## OPTIMIZATION: Maybe better to derive at attr assignment time. ##

   @property
   def overrides(self):
      '''Ordered data structure of format-time grob overrides.'''
      result = [ ]
      for contributor in self.contributors:
         result.extend(getattr(contributor, 'overrides', [ ]))
      return result

   ## OPTIMIZATION: Maybe better to derive at attr assignment time. ##

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

   def report(self, output = 'screen'):
      '''Deliver report of format-time contributions.
         Order by interface, location, contribution.'''
      result = ''
      for ((contributor, location), contributions) in self.contributions:
         result += '%s\n' % contributor.__class__.__name__
         result += '\t%s\n' % location
         for contribution in contributions:
            result += '\t\t%s\n' % contribution
      if output == 'screen':
         print result
      else:
         return result
