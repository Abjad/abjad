from abjad.core.interface import _Interface


class InterfaceAggregator(_Interface):
   '''Aggregate information about all format-contributing interfaces.'''

   def __init__(self, client):
      '''Bind to client. Note that private contributors list is not
      populate in this class. Rather, each class inheriting from format
      contributor is reponsible for registering itself and adding
      its class to the private contributors list initialized here.'''
      _Interface.__init__(self, client)
      self._contributors = [ ]
      self._contributors_sorted = False

   ## PUBLIC ATTRIBUTES ##

   @property
   def after(self):
      '''Ordered list of format-time contributions for after format slot.'''
      result = [ ]
      for contributor in self.contributors:
         result.extend(getattr(contributor, '_after', [ ]))
      return result

   @property
   def before(self):
      '''Ordered list of format-time contributions for before format slot.'''
      result = [ ]
      for contributor in self.contributors:
         result.extend(getattr(contributor, '_before', [ ]))
      return result

   @property
   def closing(self):
      '''Ordered list of format-time contributions for closing format slot.'''
      result = [ ]
      for contributor in self.contributors:
         result.extend(getattr(contributor, '_closing', [ ]))
      return result

#   @property
#   def contributors(self):
#      '''Return alphabetized list of interface format contributors.
#         Does not include spanner format contributors.'''
#      from abjad.core.formatcontributor import _FormatContributor
#      result = [ ]
#      client = self._client
#      for value in vars(client).values( ):
#         if isinstance(value, _Interface) and \
#            isinstance(value, _FormatContributor):
#            result.append(value)
#      result.sort(lambda x, y: 
#         cmp(x.__class__.__name__, y.__class__.__name__))
#      return result

   @property
   def contributors(self):
      from abjad.chord import Chord
      from abjad.notehead import NoteHead
      if not self._contributors_sorted:
         self._contributors.sort(lambda x, y:
            cmp(x.__class__.__name__, y.__class__.__name__))
         self._contributors_sorted = True
      ## TODO: Remove client-testing hack. ##
      if isinstance(self._client, Chord):
         notehead = [x for x in self._contributors if isinstance(x, NoteHead)]
         if notehead:
            notehead = notehead[0]
            self._contributors.remove(notehead) 
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
         result.extend(getattr(contributor, '_left', [ ]))
      return result

   @property
   def opening(self):
      '''Ordered list of format-time contributions for opening format slot.'''
      result = [ ]
      for contributor in self.contributors:
         result.extend(getattr(contributor, '_opening', [ ]))
      return result

   ## OPTIMIZATION: Maybe better to derive at attr assignment time. ##

   @property
   def overrides(self):
      '''Ordered data structure of format-time grob overrides.'''
      result = [ ]
      for contributor in self.contributors:
         #print contributor.__repr__( ), getattr(contributor, '_overrides', [ ])
         result.extend(getattr(contributor, '_overrides', [ ]))
      return result

   ## OPTIMIZATION: Maybe better to derive at attr assignment time. ##

   @property
   def reverts(self):
      '''Ordered data structure of format-time grob reverts.'''
      result = [ ]
      for contributor in self.contributors:
         result.extend(getattr(contributor, '_reverts', [ ]))
      return result

   @property
   def right(self):
      '''Ordered list of format-time contributions for right format slot.'''
      result = [ ]
      for contributor in self.contributors:
         result.extend(getattr(contributor, '_right', [ ]))
      return result

   @property
   def settings(self):
      '''Ordered data structure of format-time context settings.'''
      result = [ ]
      for contributor in self.contributors:
         result.extend(getattr(contributor, 'settings', [ ]))
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
