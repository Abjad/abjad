from abjad.core.interface import _Interface
from abjad.component.slots import _ComponentFormatterSlotsInterface


class _ComponentFormatter(_Interface):

   ## The 'number' attribute causes only leaf numbering but attaches
   ## to _ComponentFormatter so that containers can number leaves.
   def __init__(self, client):
      _Interface.__init__(self, client)
      self._slots = _ComponentFormatterSlotsInterface(self)
      #self.number = False

   ## PRIVATE ATTRIBUTES ##
   
   @property
   def _knownFormatLocations(self):
      '''Output-ordered list of known format locations.'''
      result = [
         'grace', 'before', 'opening', 'agrace_opening', 
         'left', 'body', 'right',
         'agrace', 'closing', 'after']
      return result

   ## PRIVATE METHODS ##

   def _collectLocationVerbose(self, location):
      '''Collect all format contributions as (interface, strings) pairs.'''
      result = [ ]
      for contributor in self._client.interfaces.contributors:
         try:
            exec('result.append((contributor, contributor.%s))' % location)
         except AttributeError:
            pass
      try:
         exec(
            'result.append((self._client.spanners, self._client.spanners.%s))' 
            % location)
      except AttributeError:
         pass
      return result

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self):
      result = [ ]
      result.extend(self.slots.slot_1)
      result.extend(self.slots.slot_2)
      result.extend(self.slots.slot_3)
      result.extend(self.slots.slot_4)
      result.extend(self.slots.slot_5)
      result.extend(self.slots.slot_6)
      result.extend(self.slots.slot_7)
      result = '\n'.join(result)
      return result

   @property
   def slots(self):
      return self._slots

   ## PUBLIC METHODS ##

   def report(self, delivery = 'screen'):
      '''Deliver report of format-time contributions.
         Contributions order first by location and then by interface.'''
      result = '%s\n' % self
      locations = self._knownFormatLocations
      for location in locations:
         contributions = self._collectLocationVerbose(location)
         contributions = [x for x in contributions if x[1]]
         if contributions:
            result += '\t%s\n' % location
            for contribution in contributions:
               interface, directives = contribution
               result += '\t\t%s\n' % interface 
               for directive in directives:
                  result += '\t\t\t%s\n' % directive
      if delivery == 'screen':
         print result
      else:
         return result
