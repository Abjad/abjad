from abjad.interfaces._Interface import _Interface


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
      result.sort( )
      return result

   @property
   def before(self):
      '''Ordered list of format-time contributions for before format slot.'''
      result = [ ]
      for contributor in self.contributors:
         result.extend(getattr(contributor, '_before', [ ]))
      result.sort( )
      return result

   @property
   def closing(self):
      '''Ordered list of format-time contributions for closing format slot.'''
      result = [ ]
      for contributor in self.contributors:
         result.extend(getattr(contributor, '_closing', [ ]))
      result.sort( )
      return result

   @property
   def contributors(self):
      from abjad.components.Chord import Chord
      from abjad.components.NoteHead import NoteHead
      if not self._contributors_sorted:
         self._contributors.sort(lambda x, y:
            cmp(x.__class__.__name__, y.__class__.__name__))
         self._contributors_sorted = True
      ## TODO: Remove client-testing hack. ##
      if isinstance(self._client, Chord):
         note_head = [x for x in self._contributors if isinstance(x, NoteHead)]
         if note_head:
            note_head = note_head[0]
            self._contributors.remove(note_head) 
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
      '''Ordered list of format-time contributions for left format slot.
      '''
      result = [ ]
      for contributor in self.contributors:
         result.extend(getattr(contributor, '_left', [ ]))
      result.sort( )
      return result

   @property
   def opening(self):
      '''Ordered list of format-time contributions for opening format slot.
      '''
      result = [ ]
      for contributor in self.contributors:
         result.extend(getattr(contributor, '_opening', [ ]))
      result.sort( )
      return result

   ## OPTIMIZATION: Maybe better to derive at attr assignment time. ##

   @property
   def overrides(self):
      '''Ordered data structure of format-time grob overrides.
      '''
      result = [ ]
      for contributor in self.contributors:
         #print contributor.__repr__( ), getattr(contributor, '_overrides', [ ])
         result.extend(getattr(contributor, '_overrides', [ ]))
      result.extend(self._client.override._overrides)
      ## guarantee predictable order of override statements
      result.sort( )
      return result

   ## OPTIMIZATION: Maybe better to derive at attr assignment time. ##

   @property
   def reverts(self):
      '''Ordered data structure of format-time grob reverts.
      '''
      result = [ ]
      for contributor in self.contributors:
         result.extend(getattr(contributor, '_reverts', [ ]))
      ## guarantee predictable order of revert statements
      result.sort( )
      return result

   @property
   def right(self):
      '''Ordered list of format-time contributions for right format slot.
      '''
      result = [ ]
      for contributor in self.contributors:
         result.extend(getattr(contributor, '_right', [ ]))
      result.sort( )
      return result

   @property
   def settings(self):
      '''Ordered data structure of format-time context settings.
      '''
      result = [ ]
      for contributor in self.contributors:
         result.extend(getattr(contributor, 'settings', [ ]))
      from abjad.components._Leaf import _Leaf
      from abjad.tools.lilyfiletools._format_lilypond_context_setting_inline import \
         _format_lilypond_context_setting_inline
      from abjad.tools.lilyfiletools._format_lilypond_context_setting_in_with_block import \
         _format_lilypond_context_setting_in_with_block
      if isinstance(self._client, _Leaf):
         for item in vars(self._client.set).iteritems( ):
            result.append(_format_lilypond_context_setting_inline(*item))
      else:
         for item in vars(self._client.set).iteritems( ):
            result.append(_format_lilypond_context_setting_in_with_block(*item))
      result.sort( )
      return result

   ## PUBLIC METHODS ##

   def report(self, output = 'screen'):
      '''Deliver report of format-time contributions.
      Order by interface, location, contribution.
      '''
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
